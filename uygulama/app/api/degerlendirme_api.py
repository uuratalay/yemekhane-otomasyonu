"""Değerlendirme uçları: bekleyen menüler ve oy ekleme."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .bagimliliklar import degerlendirme_servisi, mevcut_kullanici

router = APIRouter(prefix="/api")


class DegerlendirmeIstegi(BaseModel):
    menu_id: int
    puan: int
    yorum: str | None = None


@router.get("/degerlendirme/bekleyenler")
def bekleyenler(kullanici: dict = Depends(mevcut_kullanici)):
    return degerlendirme_servisi.listele(kullanici["id"])


@router.post("/degerlendirme")
def ekle(istek: DegerlendirmeIstegi, kullanici: dict = Depends(mevcut_kullanici)):
    return degerlendirme_servisi.ekle(
        kullanici["id"], istek.menu_id, istek.puan, istek.yorum)
