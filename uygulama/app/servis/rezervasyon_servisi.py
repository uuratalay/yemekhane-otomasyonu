"""
RezervasyonServisi — rezervasyon yap/iptal/listele.
Para mantığı yordamdadır; servis sonucu biçimler. yap/iptal sonrası dönen
'bakiye' KAYNAK'tan gelir (anlık, doğru değer).
"""


class RezervasyonServisi:
    def __init__(self, rezervasyon_depo):
        self._rez = rezervasyon_depo

    def yap(self, kullanici_id: int, menu_id: int):
        s = self._rez.yap(kullanici_id, menu_id)
        return {
            "rezervasyon_id": s["rezervasyon_id"],
            "ucret": float(s["ucret"]),
            "bakiye": float(s["bakiye"]),
            "mesaj": "Rezervasyon oluşturuldu.",
        }

    def iptal(self, kullanici_id: int, rezervasyon_id: int):
        s = self._rez.iptal(kullanici_id, rezervasyon_id)
        return {
            "rezervasyon_id": s["rezervasyon_id"],
            "iade": float(s["iade"]),
            "bakiye": float(s["bakiye"]),
            "mesaj": "Rezervasyon iptal edildi.",
        }

    def listem(self, kullanici_id: int):
        satirlar = self._rez.listele(kullanici_id)
        for s in satirlar:
            s["ucret"] = float(s["ucret"])
            s["tarih"] = str(s["tarih"])
            s["olusturma"] = str(s["olusturma"])
            s["rezervasyon_son"] = str(s["rezervasyon_son"])
            s["iptal_edilebilir"] = bool(s["iptal_edilebilir"])
        return satirlar
