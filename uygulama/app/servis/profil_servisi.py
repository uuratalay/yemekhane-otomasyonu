"""ProfilServisi — kullanıcının alerjen tercihleri (Aşama 4)."""


class ProfilServisi:
    def __init__(self, kullanici_depo, katalog_depo):
        self._kullanici = kullanici_depo
        self._katalog = katalog_depo

    def alerjenler(self, kullanici_id: int):
        return {
            "tum": self._katalog.alerjenler(),
            "secili": self._kullanici.alerjen_idleri(kullanici_id),
        }

    def alerjenleri_kaydet(self, kullanici_id: int, alerjen_idler):
        # Yinelenenleri ayıkla
        temiz = sorted(set(int(a) for a in (alerjen_idler or [])))
        self._kullanici.alerjenleri_guncelle(kullanici_id, temiz)
        return {"mesaj": "Alerjen tercihleriniz kaydedildi.", "secili": temiz}
