"""Bakiye uçları: özet (sayfa) ve yükleme."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .bagimliliklar import bakiye_servisi, mevcut_kullanici

router = APIRouter(prefix="/api")


class YuklemeIstegi(BaseModel):
    tutar: float


@router.get("/bakiye")
def bakiye(kullanici: dict = Depends(mevcut_kullanici)):
    return bakiye_servisi.ozet(kullanici["id"])


@router.post("/bakiye/yukle")
def yukle(istek: YuklemeIstegi, kullanici: dict = Depends(mevcut_kullanici)):
    return bakiye_servisi.yukle(kullanici["id"], istek.tutar)
