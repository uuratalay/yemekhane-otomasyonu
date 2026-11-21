"""
Composition root — bağımlılık enjeksiyonu (DIP).
Tüm depolar ve servisler burada BİR kez kurulur ve birbirine constructor ile
verilir. Controller'lar bu tekil servisleri ve FastAPI Depends ile kimlik
denetimini kullanır.
"""
from fastapi import Depends, Header

from ..core.veritabani import baglanti
from ..core.redis_istemci import istemci as redis_istemci
from ..core.hatalar import KimlikHatasi, YetkiHatasi

from ..veri.kullanici_deposu import KullaniciDeposu
from ..veri.menu_deposu import MenuDeposu
from ..veri.rezervasyon_deposu import RezervasyonDeposu
from ..veri.bakiye_deposu import BakiyeDeposu
from ..veri.degerlendirme_deposu import DegerlendirmeDeposu
from ..veri.katalog_deposu import KatalogDeposu
from ..veri.yonetim_deposu import YonetimDeposu

from ..onbellek.oturum_deposu import OturumDeposu
from ..onbellek.menu_onbellegi import MenuOnbellegi

from ..servis.kimlik_servisi import KimlikServisi
from ..servis.menu_servisi import MenuServisi
from ..servis.rezervasyon_servisi import RezervasyonServisi
from ..servis.bakiye_servisi import BakiyeServisi
from ..servis.degerlendirme_servisi import DegerlendirmeServisi
from ..servis.yonetim_servisi import YonetimServisi
from ..servis.profil_servisi import ProfilServisi

# ---- Depolar (veri katmanı) ---------------------------------------------
kullanici_depo     = KullaniciDeposu(baglanti)
menu_depo          = MenuDeposu(baglanti)
rezervasyon_depo   = RezervasyonDeposu(baglanti)
bakiye_depo        = BakiyeDeposu(baglanti)
degerlendirme_depo = DegerlendirmeDeposu(baglanti)
katalog_depo       = KatalogDeposu(baglanti)
yonetim_depo       = YonetimDeposu(baglanti)

# ---- Önbellek / oturum ---------------------------------------------------
oturum_deposu = OturumDeposu(redis_istemci)
menu_onbellegi = MenuOnbellegi(redis_istemci)

# ---- Servisler (iş katmanı) ---------------------------------------------
kimlik_servisi        = KimlikServisi(kullanici_depo, oturum_deposu)
menu_servisi          = MenuServisi(menu_depo, menu_onbellegi, kullanici_depo, katalog_depo)
rezervasyon_servisi   = RezervasyonServisi(rezervasyon_depo)
bakiye_servisi        = BakiyeServisi(bakiye_depo)
degerlendirme_servisi = DegerlendirmeServisi(degerlendirme_depo)
yonetim_servisi       = YonetimServisi(yonetim_depo, menu_onbellegi)
profil_servisi        = ProfilServisi(kullanici_depo, katalog_depo)


# ---- Kimlik denetimi (request-scoped) -----------------------------------
def gelen_token(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise KimlikHatasi()
    return authorization.split(" ", 1)[1].strip()


def mevcut_kullanici(token: str = Depends(gelen_token)) -> dict:
    return kimlik_servisi.oturumdan_kullanici(token)


def yonetici(kullanici: dict = Depends(mevcut_kullanici)) -> dict:
    if kullanici.get("rol") != "yonetici":
        raise YetkiHatasi()
    return kullanici
