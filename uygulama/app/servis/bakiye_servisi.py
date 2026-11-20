"""
BakiyeServisi — bakiye yükleme ve özet.
yukle: KAYNAK yordamından dönen bakiyeyi verir (anlık).
ozet:  bakiye SAYFASI için REPLİKA'dan okur (eşzamansız; rapora açıklama konusu).
"""


class BakiyeServisi:
    def __init__(self, bakiye_depo):
        self._b = bakiye_depo

    def yukle(self, kullanici_id: int, tutar):
        s = self._b.yukle(kullanici_id, tutar)
        return {
            "hareket_id": s["hareket_id"],
            "bakiye": float(s["bakiye"]),
            "mesaj": "Bakiye yüklendi.",
        }

    def ozet(self, kullanici_id: int):
        bak = self._b.guncel_bakiye(kullanici_id)
        hareketler = self._b.hareketler(kullanici_id)
        for h in hareketler:
            h["tutar"] = float(h["tutar"])
            h["olusturma"] = str(h["olusturma"])
        return {
            "bakiye": float(bak["bakiye"]) if bak else 0.0,
            "hareketler": hareketler,
        }
