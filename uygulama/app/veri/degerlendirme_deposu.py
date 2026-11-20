"""DegerlendirmeDeposu — kullanılmış menüleri listeler ve oy ekler."""
from .temel_depo import TemelDepo


class DegerlendirmeDeposu(TemelDepo):

    def bekleyenler(self, kullanici_id: int):
        """Kullanılmış ama henüz değerlendirilmemiş menüler."""
        return self.oku_liste(
            """
            SELECT m.id AS menu_id, m.tarih, o.ad AS ogun, yh.ad AS yemekhane
              FROM rezervasyonlar r
              JOIN menuler m       ON m.id = r.menu_id
              JOIN ogunler o       ON o.id = m.ogun_id
              JOIN yemekhaneler yh ON yh.id = m.yemekhane_id
             WHERE r.kullanici_id = %s AND r.durum = 'kullanildi'
               AND NOT EXISTS (
                   SELECT 1 FROM degerlendirmeler d
                    WHERE d.kullanici_id = r.kullanici_id AND d.menu_id = m.id)
             ORDER BY m.tarih DESC
            """,
            (kullanici_id,),
        )

    def kullanilmis_mi(self, kullanici_id: int, menu_id: int) -> bool:
        satir = self.oku_tek(
            "SELECT 1 AS v FROM rezervasyonlar "
            "WHERE kullanici_id = %s AND menu_id = %s AND durum = 'kullanildi'",
            (kullanici_id, menu_id),
        )
        return satir is not None

    def oy_var_mi(self, kullanici_id: int, menu_id: int) -> bool:
        satir = self.oku_tek(
            "SELECT 1 AS v FROM degerlendirmeler "
            "WHERE kullanici_id = %s AND menu_id = %s",
            (kullanici_id, menu_id),
        )
        return satir is not None

    def ekle(self, kullanici_id: int, menu_id: int, puan: int, yorum):
        return self.yaz(
            "INSERT INTO degerlendirmeler (kullanici_id, menu_id, puan, yorum) "
            "VALUES (%s, %s, %s, %s)",
            (kullanici_id, menu_id, puan, yorum),
        )
