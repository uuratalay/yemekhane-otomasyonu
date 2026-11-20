"""
BakiyeDeposu — bakiye yükleme (KAYNAK, yordam) ve özet/hareketler (REPLİKA).
Not: yüklemeden HEMEN sonra gösterilecek bakiye yordamın döndürdüğü
(KAYNAK) değerdir; bu depo ayrıca bakiye SAYFASI için replikadan listeler.
"""
from .temel_depo import TemelDepo


class BakiyeDeposu(TemelDepo):

    def yukle(self, kullanici_id: int, tutar):
        # sp_bakiye_yukle -> {hareket_id, bakiye}
        return self.yordam_cagir("sp_bakiye_yukle", (kullanici_id, tutar))

    def guncel_bakiye(self, kullanici_id: int):
        return self.oku_tek(
            "SELECT bakiye FROM kullanicilar WHERE id = %s", (kullanici_id,)
        )

    def hareketler(self, kullanici_id: int, limit: int = 50):
        return self.oku_liste(
            """
            SELECT tur, tutar, aciklama, olusturma
              FROM bakiye_hareketleri
             WHERE kullanici_id = %s
             ORDER BY olusturma DESC, id DESC
             LIMIT %s
            """,
            (kullanici_id, limit),
        )
