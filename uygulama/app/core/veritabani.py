"""
BaglantiYoneticisi — ConnectionRouter deseni.

Tek sorumluluğu: doğru veritabanına bağlantı vermek.
  * yazma()  -> KAYNAK (mysql-primary): INSERT/UPDATE ve tüm stored procedure çağrıları
  * okuma()  -> REPLİKA (mysql-replica): listeleme ve raporlar

Read/write ayrımı TEK yerde toplanır. Kod içine serpiştirilmiş
"hangi host?" if'leri olmadığı için ileride bir değişiklik tek noktayı
etkiler (shotgun surgery önlenir). İki ayrı bağlantı havuzu kullanılır.
"""
from contextlib import contextmanager

import mysql.connector
from mysql.connector import pooling

from ..config import ayar


class BaglantiYoneticisi:
    def __init__(self):
        self._yazma_havuz = None
        self._okuma_havuz = None

    def _havuz_kur(self, host: str, ad: str) -> pooling.MySQLConnectionPool:
        return pooling.MySQLConnectionPool(
            pool_name=ad,
            pool_size=5,
            host=host,
            port=ayar.DB_PORT,
            database=ayar.DB_ADI,
            user=ayar.DB_KULLANICI,
            password=ayar.DB_SIFRE,
            charset="utf8mb4",
            autocommit=True,       # yordamlar kendi transaction'ını yönetir
            connection_timeout=10,
        )

    def _yazma_havuzu(self):
        if self._yazma_havuz is None:
            self._yazma_havuz = self._havuz_kur(ayar.DB_YAZMA_HOST, "yazma_havuz")
        return self._yazma_havuz

    def _okuma_havuzu(self):
        if self._okuma_havuz is None:
            self._okuma_havuz = self._havuz_kur(ayar.DB_OKUMA_HOST, "okuma_havuz")
        return self._okuma_havuz

    @contextmanager
    def yazma(self):
        """KAYNAK bağlantısı. Yazma ve CALL burada yapılır."""
        conn = self._yazma_havuzu().get_connection()
        try:
            yield conn
        finally:
            conn.close()   # bağlantıyı havuza geri verir

    @contextmanager
    def okuma(self):
        """REPLİKA bağlantısı. Okuma/listeleme/rapor burada yapılır."""
        conn = self._okuma_havuzu().get_connection()
        try:
            yield conn
        finally:
            conn.close()


# Tüm uygulamanın paylaştığı tek örnek (composition root'ta enjekte edilir)
baglanti = BaglantiYoneticisi()
