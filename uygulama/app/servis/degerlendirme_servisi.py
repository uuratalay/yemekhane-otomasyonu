"""
DegerlendirmeServisi — kullanılmış menüye 1–5 puan ve yorum.
"Yalnızca kullanılmış menü değerlendirilir" kuralı uygulamaya aittir (şema değil).
"""
from ..core.hatalar import UygulamaHatasi


class DegerlendirmeServisi:
    def __init__(self, degerlendirme_depo):
        self._d = degerlendirme_depo

    def listele(self, kullanici_id: int):
        satirlar = self._d.bekleyenler(kullanici_id)
        for s in satirlar:
            s["tarih"] = str(s["tarih"])
        return satirlar

    def ekle(self, kullanici_id: int, menu_id: int, puan: int, yorum):
        if puan is None or puan < 1 or puan > 5:
            raise UygulamaHatasi("Puan 1 ile 5 arasında olmalıdır.")
        if not self._d.kullanilmis_mi(kullanici_id, menu_id):
            raise UygulamaHatasi("Yalnızca kullandığınız menüleri değerlendirebilirsiniz.")
        if self._d.oy_var_mi(kullanici_id, menu_id):
            raise UygulamaHatasi("Bu menüyü zaten değerlendirdiniz.")
        self._d.ekle(kullanici_id, menu_id, puan, (yorum or "").strip() or None)
        return {"mesaj": "Değerlendirmeniz kaydedildi."}
