"""
MenuServisi — günün menüsü ve haftalık menü iş mantığı.
Toplam kalori toplama, role göre fiyat seçimi burada; Controller bilmez.
"""


class MenuServisi:
    def __init__(self, menu_depo):
        self._menu = menu_depo

    def gunluk(self, yemekhane_id: int, tarih: str, ogun_id: int):
        satirlar = self._menu.gunluk_yemekler(yemekhane_id, tarih, ogun_id)
        if not satirlar:
            return None
        ilk = satirlar[0]
        yemekler = [{
            "ad": s["yemek"],
            "kategori": s["kategori"],
            "kalori": s["kalori"],
            "vejetaryen": bool(s["vejetaryen"]),
            "alerjenler": s["alerjenler"],          # "Gluten, Süt" gibi ya da None
        } for s in satirlar]
        return {
            "menu_id": ilk["menu_id"],
            "tarih": str(ilk["tarih"]),
            "yemekhane": ilk["yemekhane"],
            "ogun": ilk["ogun"],
            "ogrenci_fiyati": float(ilk["ogrenci_fiyati"]),
            "personel_fiyati": float(ilk["personel_fiyati"]),
            "rezervasyon_son": str(ilk["rezervasyon_son"]),
            "toplam_kalori": sum(s["kalori"] for s in satirlar),
            "hepsi_vejetaryen": all(bool(s["vejetaryen"]) for s in satirlar),
            "yemekler": yemekler,
        }

    def haftalik(self, yemekhane_id: int, rol: str):
        satirlar = self._menu.haftalik_doluluk(yemekhane_id)
        sonuc = []
        for s in satirlar:
            fiyat = s["ogrenci_fiyati"] if rol == "ogrenci" else s["personel_fiyati"]
            sonuc.append({
                "menu_id": s["menu_id"],
                "tarih": str(s["tarih"]),
                "ogun": s["ogun"],
                "yemekhane": s["yemekhane"],
                "kapasite": s["kapasite"],
                "rezerve": s["rezerve"],
                "bos_yer": s["bos_yer"],
                "rezervasyon_son": str(s["rezervasyon_son"]),
                "gecti": bool(s["gecti"]),       # son saat geçti mi -> buton pasif
                "fiyat": float(fiyat),           # kullanıcının rolüne göre
            })
        return sonuc
