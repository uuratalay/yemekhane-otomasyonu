"""Menü uçları: günün menüsü (kişiye özel alerjen uyarısı) ve haftalık menü."""
from fastapi import APIRouter, Depends

from .bagimliliklar import menu_servisi, mevcut_kullanici

router = APIRouter(prefix="/api")


@router.get("/menu/gunluk")
def gunluk(yemekhane_id: int, tarih: str, ogun_id: int,
           kullanici: dict = Depends(mevcut_kullanici)):
    # kullanıcı id'si: alerjen uyarısını kişiye göre eklemek için
    return menu_servisi.gunluk(yemekhane_id, tarih, ogun_id, kullanici["id"])


@router.get("/menu/haftalik")
def haftalik(yemekhane_id: int, kullanici: dict = Depends(mevcut_kullanici)):
    return menu_servisi.haftalik(yemekhane_id, kullanici["rol"])
