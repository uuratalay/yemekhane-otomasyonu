"""
OturumDeposu — Redis tabanlı oturum (Aşama 3'ün iki işinden biri).
Anahtar: oturum:{token}  ·  TTL: 30 dk, her istekte yenilenir  ·  çıkışta silinir.
Oturum uygulama belleğinde DEĞİL Redis'te tutulduğu için uygulama container'ı
yeniden başlasa da oturum düşmez.
"""
import json

from ..config import ayar


class OturumDeposu:
    ONEK = "oturum:"

    def __init__(self, redis_istemci):
        self._r = redis_istemci

    def olustur(self, token: str, veri: dict):
        self._r.setex(self.ONEK + token, ayar.OTURUM_SURE_SN, json.dumps(veri))

    def getir_ve_yenile(self, token: str):
        anahtar = self.ONEK + token
        ham = self._r.get(anahtar)
        if ham is None:
            return None
        self._r.expire(anahtar, ayar.OTURUM_SURE_SN)   # 30 dk'yı sıfırla
        return json.loads(ham)

    def sil(self, token: str):
        self._r.delete(self.ONEK + token)
