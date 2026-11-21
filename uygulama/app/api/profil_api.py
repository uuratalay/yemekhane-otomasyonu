"""Profil uçları (Aşama 4): kullanıcının alerjen tercihleri."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .bagimliliklar import profil_servisi, mevcut_kullanici

router = APIRouter(prefix="/api")


class AlerjenIstegi(BaseModel):
    alerjen_idler: list[int]


@router.get("/profil/alerjenler")
def getir(kullanici: dict = Depends(mevcut_kullanici)):
    return profil_servisi.alerjenler(kullanici["id"])


@router.put("/profil/alerjenler")
def kaydet(istek: AlerjenIstegi, kullanici: dict = Depends(mevcut_kullanici)):
    return profil_servisi.alerjenleri_kaydet(kullanici["id"], istek.alerjen_idler)
