"""KullaniciDeposu — kullanıcı okuma işlemleri (kimlik ve profil)."""
from .temel_depo import TemelDepo


class KullaniciDeposu(TemelDepo):

    def eposta_ile_bul(self, eposta: str):
        return self.oku_tek(
            "SELECT id, ad, soyad, eposta, sifre_hash, rol, aktif "
            "FROM kullanicilar WHERE eposta = %s",
            (eposta,),
        )

    def id_ile_bul(self, kullanici_id: int):
        return self.oku_tek(
            "SELECT id, ad, soyad, eposta, rol, bakiye, aktif "
            "FROM kullanicilar WHERE id = %s",
            (kullanici_id,),
        )
