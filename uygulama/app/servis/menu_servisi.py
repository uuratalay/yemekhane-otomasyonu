"""
MenuServisi — günün menüsü (cache-aside) ve haftalık menü.

Günün menüsü önce Redis'ten denenir (HIT), yoksa replikadan okunup önbelleğe
yazılır (MISS). Önbellekteki kayıt kullanıcıdan BAĞIMSIZDIR (menü içeriği);
kişiye özel alerjen uyarısı önbellekten SONRA, her kullanıcı için eklenir
(Aşama 4). Böylece tek bir önbellek kaydı tüm kullanıcılara hizmet eder.
"""


class MenuServisi:
    def __init__(self, menu_depo, menu_onbellegi, kullanici_depo, katalog_depo):
        self._menu = menu_depo
        self._cache = menu_onbellegi
        self._kullanici = kullanici_depo
        self._katalog = katalog_depo
        self._alerjen_ad = None   # id -> ad (tembel yüklenir)

    def gunluk(self, yemekhane_id: int, tarih: str, ogun_id: int, kullanici_id: int):
        menu = self._cache.getir(yemekhane_id, tarih, ogun_id)
        if menu is not None:
            print(f"[ONBELLEK] HIT  menu:{yemekhane_id}:{tarih}:{ogun_id} -> redis", flush=True)
        else:
            print(f"[ONBELLEK] MISS menu:{yemekhane_id}:{tarih}:{ogun_id} -> replika", flush=True)
            menu = self._olustur(yemekhane_id, tarih, ogun_id)
            if menu is None:
                return None
            self._cache.koy(yemekhane_id, tarih, ogun_id, menu)
        # Kişiye özel alerjen uyarısı (önbelleğe yazılmaz)
        self._alerjen_uyarisi_ekle(menu, kullanici_id)
        return menu

    def _olustur(self, yemekhane_id: int, tarih: str, ogun_id: int):
        satirlar = self._menu.gunluk_yemekler(yemekhane_id, tarih, ogun_id)
        if not satirlar:
            return None
        ilk = satirlar[0]
        yemekler = []
        for s in satirlar:
            idler = [int(x) for x in str(s["alerjen_idler"] or "").split(",") if x.strip()]
            yemekler.append({
                "ad": s["yemek"],
                "kategori": s["kategori"],
                "kalori": s["kalori"],
                "vejetaryen": bool(s["vejetaryen"]),
                "alerjenler": s["alerjenler"],
                "alerjen_idler": idler,          # uyarı hesabı için
            })
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

    def _alerjen_haritasi(self):
        if self._alerjen_ad is None:
            self._alerjen_ad = {a["id"]: a["ad"] for a in self._katalog.alerjenler()}
        return self._alerjen_ad

    def _alerjen_uyarisi_ekle(self, menu, kullanici_id):
        kul = set(self._kullanici.alerjen_idleri(kullanici_id))
        harita = self._alerjen_haritasi() if kul else {}
        for y in menu["yemekler"]:
            y["uyari"] = [harita[i] for i in y.get("alerjen_idler", []) if i in kul]

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
