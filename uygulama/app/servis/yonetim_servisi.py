"""YonetimServisi — yönetici menü oluşturma/güncelleme ve menü özeti."""
from ..core.hatalar import UygulamaHatasi


class YonetimServisi:
    def __init__(self, yonetim_depo):
        self._y = yonetim_depo

    def menu_olustur(self, istek):
        if not istek.yemek_idler:
            raise UygulamaHatasi("Menüde en az bir yemek olmalıdır.")
        menu_id = self._y.menu_olustur(
            istek.yemekhane_id, istek.tarih, istek.ogun_id,
            istek.ogrenci_fiyati, istek.personel_fiyati, istek.yemek_idler,
        )
        return {"menu_id": menu_id, "mesaj": "Menü oluşturuldu."}

    def menu_guncelle(self, menu_id: int, istek):
        if not istek.yemek_idler:
            raise UygulamaHatasi("Menüde en az bir yemek olmalıdır.")
        self._y.menu_guncelle(
            menu_id, istek.ogrenci_fiyati, istek.personel_fiyati, istek.yemek_idler,
        )
        return {"menu_id": menu_id, "mesaj": "Menü güncellendi."}

    def menu_listesi(self):
        satirlar = self._y.menu_listesi()
        for s in satirlar:
            s["tarih"] = str(s["tarih"])
            if s.get("ortalama_puan") is not None:
                s["ortalama_puan"] = float(s["ortalama_puan"])
        return satirlar

    def ozet(self, menu_id: int):
        s = self._y.ozet(menu_id)
        if not s:
            raise UygulamaHatasi("Menü bulunamadı.", kod=404)
        s["tarih"] = str(s["tarih"])
        if s.get("ortalama_puan") is not None:
            s["ortalama_puan"] = float(s["ortalama_puan"])
        s["ogrenci_fiyati"] = float(s["ogrenci_fiyati"])
        s["personel_fiyati"] = float(s["personel_fiyati"])
        s["yemek_idler"] = self._y.menu_yemek_idleri(menu_id)
        return s
