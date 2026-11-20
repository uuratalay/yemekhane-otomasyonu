"""
MenuDeposu — menü okuma işlemleri (REPLİKA, view'lar üzerinden).
Zaman karşılaştırmaları (son saat geçti mi) veritabanına bırakılır;
böylece saat dilimi (+03:00) tutarlı kalır.
"""
from .temel_depo import TemelDepo


class MenuDeposu(TemelDepo):

    def gunluk_yemekler(self, yemekhane_id: int, tarih: str, ogun_id: int):
        """v_menu_detay: menüdeki her yemek için bir satır (kategori sırasına göre)."""
        return self.oku_liste(
            """
            SELECT menu_id, tarih, yemekhane, ogun, ogrenci_fiyati, personel_fiyati,
                   rezervasyon_son, yemek, kategori, kategori_sira, kalori,
                   vejetaryen, alerjenler, alerjen_idler
              FROM v_menu_detay
             WHERE yemekhane_id = %s AND tarih = %s AND ogun_id = %s
             ORDER BY kategori_sira, yemek
            """,
            (yemekhane_id, tarih, ogun_id),
        )

    def haftalik_doluluk(self, yemekhane_id: int):
        """Bugünden 6 gün sonrasına kadar menüler + doluluk + fiyatlar."""
        return self.oku_liste(
            """
            SELECT d.menu_id, d.tarih, d.ogun_id, d.ogun, d.yemekhane,
                   d.kapasite, d.rezerve, d.bos_yer, d.doluluk_yuzde,
                   d.rezervasyon_son,
                   (d.rezervasyon_son <= NOW()) AS gecti,
                   m.ogrenci_fiyati, m.personel_fiyati
              FROM v_menu_doluluk d
              JOIN menuler m ON m.id = d.menu_id
             WHERE d.yemekhane_id = %s
               AND d.tarih BETWEEN CURDATE() AND CURDATE() + INTERVAL 6 DAY
             ORDER BY d.tarih, d.ogun_id
            """,
            (yemekhane_id,),
        )

    def baslik(self, menu_id: int):
        """Önbellek anahtarı kurmak için menünün yemekhane/tarih/öğün bilgisi."""
        return self.oku_tek(
            "SELECT id AS menu_id, yemekhane_id, tarih, ogun_id "
            "FROM menuler WHERE id = %s",
            (menu_id,),
        )
