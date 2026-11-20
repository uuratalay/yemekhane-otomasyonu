"""
Ayar — tek yapılandırma kaynağı (SSOT).
Bağlantı bilgileri docker-compose.yml'deki ortam değişkenlerinden okunur;
kodun hiçbir yerinde host/şifre sabit yazılmaz.
"""
import os


class Ayar:
    # Veritabanı — yazma KAYNAĞA, okuma REPLİKAYA
    DB_YAZMA_HOST = os.environ.get("DB_YAZMA_HOST", "mysql-primary")
    DB_OKUMA_HOST = os.environ.get("DB_OKUMA_HOST", "mysql-replica")
    DB_PORT       = int(os.environ.get("DB_PORT", "3306"))
    DB_ADI        = os.environ.get("DB_ADI", "yemekhane")
    DB_KULLANICI  = os.environ.get("DB_KULLANICI", "yemekhane_app")
    DB_SIFRE      = os.environ.get("DB_SIFRE", "Uyg_2026")

    # Redis — oturum deposu (Aşama 2) ve menü önbelleği (Aşama 3)
    REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))

    # Oturum süresi: her istekte yenilenen 30 dakika
    OTURUM_SURE_SN = 30 * 60


ayar = Ayar()
