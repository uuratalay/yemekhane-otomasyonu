"""KimlikServisi — giriş (bcrypt doğrulama), çıkış ve oturumdan kullanıcı."""
from ..core.guvenlik import sifre_dogrula, token_uret
from ..core.hatalar import KimlikHatasi


class KimlikServisi:
    def __init__(self, kullanici_depo, oturum_deposu):
        self._kullanici = kullanici_depo
        self._oturum = oturum_deposu

    def giris(self, eposta: str, sifre: str):
        k = self._kullanici.eposta_ile_bul((eposta or "").strip())
        if not k or not k["aktif"] or not sifre_dogrula(sifre or "", k["sifre_hash"]):
            # Aynı mesaj: e-posta var mı yok mu sızdırılmaz
            raise KimlikHatasi("E-posta veya şifre hatalı.")
        token = token_uret()
        veri = {"id": k["id"], "ad": k["ad"], "soyad": k["soyad"], "rol": k["rol"]}
        self._oturum.olustur(token, veri)
        return {"token": token, "kullanici": veri}

    def cikis(self, token: str):
        self._oturum.sil(token)

    def oturumdan_kullanici(self, token: str):
        veri = self._oturum.getir_ve_yenile(token)
        if veri is None:
            raise KimlikHatasi()
        return veri
