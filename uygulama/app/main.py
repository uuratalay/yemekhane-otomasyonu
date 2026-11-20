"""
Uygulama girişi. Router'ları bağlar ve tek bir hata işleyici ile tüm
UygulamaHatasi türevlerini (iş kuralı, kimlik, yetki) {"hata": mesaj}
JSON'una çevirir. Stored procedure'den gelen Türkçe mesaj böylece
değiştirilmeden arayüze ulaşır.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .core.hatalar import UygulamaHatasi
from .api import (
    kimlik_api, katalog_api, menu_api, rezervasyon_api,
    bakiye_api, degerlendirme_api, yonetim_api,
)

app = FastAPI(title="Yemekhane Otomasyonu API", docs_url="/api/docs", openapi_url="/api/openapi.json")


@app.exception_handler(UygulamaHatasi)
async def uygulama_hatasi_isle(request: Request, exc: UygulamaHatasi):
    return JSONResponse(status_code=exc.kod, content={"hata": exc.mesaj})


for modul in (kimlik_api, katalog_api, menu_api, rezervasyon_api,
              bakiye_api, degerlendirme_api, yonetim_api):
    app.include_router(modul.router)


@app.get("/api/saglik")
def saglik():
    return {"durum": "ok"}
