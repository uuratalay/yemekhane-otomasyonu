"""
RezervasyonDeposu — rezervasyon işlemleri.
Para hareketi yapan yap/iptal KAYNAK'ta stored procedure ile; listeleme REPLİKA'dan.
"""
from .temel_depo import TemelDepo


class RezervasyonDeposu(TemelDepo):

    def yap(self, kullanici_id: int, menu_id: int):
        # sp_rezervasyon_yap -> {rezervasyon_id, ucret, bakiye}
        return self.yordam_cagir("sp_rezervasyon_yap", (kullanici_id, menu_id))

    def iptal(self, kullanici_id: int, rezervasyon_id: int):
        # sp_rezervasyon_iptal -> {rezervasyon_id, iade, bakiye}
        return self.yordam_cagir("sp_rezervasyon_iptal", (kullanici_id, rezervasyon_id))

    def listele(self, kullanici_id: int):
        return self.oku_liste(
            """
            SELECT r.id AS rezervasyon_id, r.durum, r.ucret, r.olusturma,
                   m.id AS menu_id, m.tarih, o.ad AS ogun, yh.ad AS yemekhane,
                   TIMESTAMP(m.tarih, o.son_saat) AS rezervasyon_son,
                   (r.durum = 'aktif'
                    AND TIMESTAMP(m.tarih, o.son_saat) > NOW()) AS iptal_edilebilir
              FROM rezervasyonlar r
              JOIN menuler m       ON m.id = r.menu_id
              JOIN ogunler o       ON o.id = m.ogun_id
              JOIN yemekhaneler yh ON yh.id = m.yemekhane_id
             WHERE r.kullanici_id = %s
             ORDER BY m.tarih DESC, o.sira
            """,
            (kullanici_id,),
        )
