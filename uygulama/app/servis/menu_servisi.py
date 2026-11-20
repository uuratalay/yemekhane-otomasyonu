"""
MenuServisi — günün menüsü (cache-aside) ve haftalık menü.
Günün menüsü önce Redis'ten denenir (HIT), yoksa replikadan okunup önbelleğe
yazılır (MISS). Haftalık liste doluluk içerdiği ve sık değiştiği için önbelleklenmez.
"""


class MenuServisi:
    def __init__(self, menu_depo, menu_onbellegi):
        self._menu = menu_depo
        self._cache = menu_onbellegi

    def gunluk(self, yemekhane_id: int, tarih: str, ogun_id: int):
        # 1) Önbellek
        onbellekli = self._cache.getir(yemekhane_id, tarih, ogun_id)
        if onbellekli is not None:
            print(f"[ONBELLEK] HIT  menu:{yemekhane_id}:{tarih}:{ogun_id} -> redis", flush=True)
            return onbellekli

        # 2) Replikadan oku
        print(f"[ONBELLEK] MISS menu:{yemekhane_id}:{tarih}:{ogun_id} -> replika", flush=True)
        satirlar = self._menu.gunluk_yemekler(yemekhane_id, tarih, ogun_id)
        if not satirlar:
            return None
        ilk = satirlar[0]
        yemekler = [{
            "ad": s["yemek"],
            "kategori": s["kategori"],
            "kalori": s["kalori"],
            "vejetaryen": bool(s["vejetaryen"]),
            "alerjenler": s["alerjenler"],
        } for s in satirlar]
        sonuc = {
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
        # 3) Önbelleğe yaz (gün sonuna kadar)
        self._cache.koy(yemekhane_id, tarih, ogun_id, sonuc)
        return sonuc

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
                "gecti": bool(s["gecti"]),
                "fiyat": float(fiyat),
            })
        return sonuc
