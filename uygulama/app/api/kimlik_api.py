"""Kimlik uçları: giriş, çıkış, oturumdaki kullanıcı."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .bagimliliklar import kimlik_servisi, mevcut_kullanici, gelen_token

router = APIRouter(prefix="/api")


class GirisIstegi(BaseModel):
    eposta: str
    sifre: str


@router.post("/giris")
def giris(istek: GirisIstegi):
    return kimlik_servisi.giris(istek.eposta, istek.sifre)


@router.post("/cikis")
def cikis(token: str = Depends(gelen_token)):
    kimlik_servisi.cikis(token)
    return {"mesaj": "Çıkış yapıldı."}


@router.get("/ben")
def ben(kullanici: dict = Depends(mevcut_kullanici)):
    return kullanici
