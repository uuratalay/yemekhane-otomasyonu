"""
KatalogDeposu — form ve seçimler için sabit/referans veriler (REPLİKA).
Yemekhaneler, öğünler, yemekler, alerjenler ve veritabanı günü.
"""
from .temel_depo import TemelDepo


class KatalogDeposu(TemelDepo):

    def yemekhaneler(self):
        return self.oku_liste(
            "SELECT id, ad, konum, kapasite FROM yemekhaneler ORDER BY id")

    def ogunler(self):
        return self.oku_liste(
            "SELECT id, ad, sira, son_saat FROM ogunler ORDER BY sira")

    def alerjenler(self):
        return self.oku_liste("SELECT id, ad FROM alerjenler ORDER BY ad")

    def yemekler(self):
        return self.oku_liste(
            """
            SELECT y.id, y.ad, y.kalori, y.vejetaryen,
                   k.id AS kategori_id, k.ad AS kategori, k.sira AS kategori_sira
              FROM yemekler y
              JOIN yemek_kategorileri k ON k.id = y.kategori_id
             ORDER BY k.sira, y.ad
            """
        )

    def bugun(self):
        satir = self.oku_tek("SELECT CURDATE() AS bugun")
        return str(satir["bugun"]) if satir else None
