"""Menü uçları: günün menüsü ve haftalık menü."""
from fastapi import APIRouter, Depends

from .bagimliliklar import menu_servisi, mevcut_kullanici

router = APIRouter(prefix="/api")


@router.get("/menu/gunluk")
def gunluk(yemekhane_id: int, tarih: str, ogun_id: int,
           kullanici: dict = Depends(mevcut_kullanici)):
    return menu_servisi.gunluk(yemekhane_id, tarih, ogun_id)


@router.get("/menu/haftalik")
def haftalik(yemekhane_id: int, kullanici: dict = Depends(mevcut_kullanici)):
    # Fiyat, giriş yapan kullanıcının rolüne göre seçilir
    return menu_servisi.haftalik(yemekhane_id, kullanici["rol"])
