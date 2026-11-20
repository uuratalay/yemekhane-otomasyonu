"""
MenuOnbellegi — Redis'in ikinci işi: menü önbelleği (cache-aside).

Anahtar: menu:{yemekhane_id}:{tarih}:{ogun_id}
TTL    : o günün sonuna (23:59:59) kadar
Geçersizleştirme: yönetici o menüyü değiştirince sil() çağrılır.

Cache-aside mantığı tek sınıfta toplanır; get/set/invalidate başka yere
dağılmaz (Aşama 4'teki Redis temizliği de buradan yapılır).
"""
import json
from datetime import datetime


class MenuOnbellegi:
    ONEK = "menu:"

    def __init__(self, redis_istemci):
        self._r = redis_istemci

    def _anahtar(self, yemekhane_id, tarih, ogun_id) -> str:
        return f"{self.ONEK}{yemekhane_id}:{tarih}:{ogun_id}"

    def getir(self, yemekhane_id, tarih, ogun_id):
        ham = self._r.get(self._anahtar(yemekhane_id, tarih, ogun_id))
        return json.loads(ham) if ham else None

    def koy(self, yemekhane_id, tarih, ogun_id, veri):
        self._r.setex(
            self._anahtar(yemekhane_id, tarih, ogun_id),
            self._gun_sonu_ttl(tarih),
            json.dumps(veri, default=str),
        )

    def sil(self, yemekhane_id, tarih, ogun_id):
        self._r.delete(self._anahtar(yemekhane_id, tarih, ogun_id))

    def _gun_sonu_ttl(self, tarih) -> int:
        """O günün 23:59:59'una kadar kalan saniye (geçmişse kısa bir süre)."""
        try:
            g = datetime.strptime(str(tarih), "%Y-%m-%d").date()
        except ValueError:
            return 3600
        gun_sonu = datetime(g.year, g.month, g.day, 23, 59, 59)
        kalan = int((gun_sonu - datetime.now()).total_seconds())
        return kalan if kalan > 0 else 60
