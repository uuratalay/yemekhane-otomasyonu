"""Rezervasyon uçları: yap (porsiyonlu), iptal, rezervasyonlarım."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .bagimliliklar import rezervasyon_servisi, mevcut_kullanici

router = APIRouter(prefix="/api")


class RezervasyonIstegi(BaseModel):
    menu_id: int
    porsiyon: str = "tam"     # 'tam' | 'yarim' (Aşama 4)


@router.post("/rezervasyon")
def yap(istek: RezervasyonIstegi, kullanici: dict = Depends(mevcut_kullanici)):
    return rezervasyon_servisi.yap(kullanici["id"], istek.menu_id, istek.porsiyon)


@router.post("/rezervasyon/{rezervasyon_id}/iptal")
def iptal(rezervasyon_id: int, kullanici: dict = Depends(mevcut_kullanici)):
    return rezervasyon_servisi.iptal(kullanici["id"], rezervasyon_id)


@router.get("/rezervasyonlarim")
def rezervasyonlarim(kullanici: dict = Depends(mevcut_kullanici)):
    return rezervasyon_servisi.listem(kullanici["id"])
