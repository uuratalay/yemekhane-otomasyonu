"""KullaniciDeposu — kullanıcı okuma işlemleri ve (Aşama 4) alerjen tercihleri."""
import mysql.connector

from .temel_depo import TemelDepo


class KullaniciDeposu(TemelDepo):

    def eposta_ile_bul(self, eposta: str):
        return self.oku_tek(
            "SELECT id, ad, soyad, eposta, sifre_hash, rol, aktif "
            "FROM kullanicilar WHERE eposta = %s",
            (eposta,),
        )

    def id_ile_bul(self, kullanici_id: int):
        return self.oku_tek(
            "SELECT id, ad, soyad, eposta, rol, bakiye, aktif "
            "FROM kullanicilar WHERE id = %s",
            (kullanici_id,),
        )

    # ---- Aşama 4: alerjen tercihleri -----------------------------------
    def alerjen_idleri(self, kullanici_id: int):
        satirlar = self.oku_liste(
            "SELECT alerjen_id FROM kullanici_alerjenleri WHERE kullanici_id = %s",
            (kullanici_id,),
        )
        return [s["alerjen_id"] for s in satirlar]

    def alerjenleri_guncelle(self, kullanici_id: int, alerjen_idler):
        """Tercihleri tek transaction'da değiştir (önce sil, sonra ekle)."""
        with self._baglanti.yazma() as conn:
            conn.autocommit = False
            imlec = conn.cursor()
            try:
                imlec.execute(
                    "DELETE FROM kullanici_alerjenleri WHERE kullanici_id = %s",
                    (kullanici_id,))
                if alerjen_idler:
                    imlec.executemany(
                        "INSERT INTO kullanici_alerjenleri (kullanici_id, alerjen_id) "
                        "VALUES (%s, %s)",
                        [(kullanici_id, a) for a in alerjen_idler])
                conn.commit()
            except mysql.connector.Error as hata:
                conn.rollback()
                raise self._cevir(hata)
            finally:
                conn.autocommit = True
                imlec.close()
