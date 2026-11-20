"""
TemelDepo — tüm depoların ortak atası.

Asıl değeri: stored procedure çağrısını ve MySQL hata kodlarının alan
hatalarına çevrilmesini TEK yerde toplar. Her depo bu sınıftan türer ve
okuma/yazma/yordam yardımcılarını kullanır; böylece boilerplate tekrarı olmaz.

Hata kodları:
  1644 -> SIGNAL '45000' (iş kuralı)  -> IsKuraliHatasi (Türkçe mesaj aynen)
  1290 -> salt okunur kopyaya yazma    -> teknik hata
  1062 -> yinelenen benzersiz anahtar  -> çağıran katmanda anlamlandırılır
  3819 -> CHECK ihlali (programlama)   -> teknik hata
"""
import mysql.connector

from ..core.hatalar import IsKuraliHatasi, UygulamaHatasi

SP_IS_KURALI = 1644
SALT_OKUNUR  = 1290
YINELENEN    = 1062
CHECK_IHLALI = 3819


class YinelenenKayit(UygulamaHatasi):
    """1062 — benzersiz anahtar çakışması. Servis katmanı anlamlı mesaj verir."""
    def __init__(self, mesaj="Bu kayıt zaten mevcut."):
        super().__init__(mesaj, kod=409)


class TemelDepo:
    def __init__(self, baglanti):
        self._baglanti = baglanti

    # ---- Okuma (REPLİKA) ------------------------------------------------
    # buffered=True: sonuç anında tamamen belleğe okunur. Böylece bağlantıda
    # "okunmamış sonuç" kalmaz; havuza iade edilen bağlantı her zaman temizdir
    # (aksi halde bir sonraki istek "Unread result found" hatası alır).
    def oku_tek(self, sql: str, parametreler=()):
        with self._baglanti.okuma() as conn:
            imlec = conn.cursor(dictionary=True, buffered=True)
            try:
                imlec.execute(sql, parametreler)
                return imlec.fetchone()
            finally:
                imlec.close()

    def oku_liste(self, sql: str, parametreler=()):
        with self._baglanti.okuma() as conn:
            imlec = conn.cursor(dictionary=True, buffered=True)
            try:
                imlec.execute(sql, parametreler)
                return imlec.fetchall()
            finally:
                imlec.close()

    # ---- Yazma (KAYNAK) -------------------------------------------------
    def yaz(self, sql: str, parametreler=()):
        """Tek INSERT/UPDATE; eklenen satırın id'sini döner."""
        with self._baglanti.yazma() as conn:
            imlec = conn.cursor()
            try:
                imlec.execute(sql, parametreler)
                return imlec.lastrowid
            except mysql.connector.Error as hata:
                raise self._cevir(hata)
            finally:
                imlec.close()

    def yordam_cagir(self, yordam_adi: str, parametreler=()):
        """
        KAYNAK'ta stored procedure çağırır ve tek satırlık sonucu döner.
        callproc + stored_results kullanılır: CALL'ın arkasında kalan sonuç
        kümeleri düzgün tüketilir, bağlantı havuza temiz döner. SIGNAL '45000'
        (errno 1644) callproc tarafından istisna olarak fırlatılır.
        """
        with self._baglanti.yazma() as conn:
            imlec = conn.cursor(dictionary=True)
            try:
                imlec.callproc(yordam_adi, parametreler)
                for sonuc in imlec.stored_results():
                    satir = sonuc.fetchone()
                    if satir is not None:
                        return satir
                return None
            except mysql.connector.Error as hata:
                raise self._cevir(hata)
            finally:
                imlec.close()

    # ---- Hata çevirisi --------------------------------------------------
    def _cevir(self, hata: "mysql.connector.Error") -> UygulamaHatasi:
        if hata.errno == SP_IS_KURALI:
            return IsKuraliHatasi(hata.msg)          # Türkçe mesaj aynen
        if hata.errno == YINELENEN:
            return YinelenenKayit()
        if hata.errno == SALT_OKUNUR:
            return UygulamaHatasi("Bu işlem salt okunur kopyada yapılamaz.", kod=500)
        # 3819 ve beklenmeyen diğerleri: ham mesaj kullanıcıya gösterilmez
        return UygulamaHatasi("İşlem sırasında beklenmeyen bir hata oluştu.", kod=500)
