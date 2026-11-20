"""Yönetici uçları: menü oluştur/güncelle, menü listesi ve özet. Hepsi 'yonetici' ister."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .bagimliliklar import yonetim_servisi, yonetici

router = APIRouter(prefix="/api")


class MenuOlusturIstegi(BaseModel):
    yemekhane_id: int
    tarih: str
    ogun_id: int
    ogrenci_fiyati: float
    personel_fiyati: float
    yemek_idler: list[int]


class MenuGuncelleIstegi(BaseModel):
    ogrenci_fiyati: float
    personel_fiyati: float
    yemek_idler: list[int]


@router.get("/yonetim/menuler")
def menuler(yon: dict = Depends(yonetici)):
    return yonetim_servisi.menu_listesi()


@router.get("/yonetim/menu/{menu_id}/ozet")
def ozet(menu_id: int, yon: dict = Depends(yonetici)):
    return yonetim_servisi.ozet(menu_id)


@router.post("/yonetim/menu")
def olustur(istek: MenuOlusturIstegi, yon: dict = Depends(yonetici)):
    return yonetim_servisi.menu_olustur(istek)


@router.put("/yonetim/menu/{menu_id}")
def guncelle(menu_id: int, istek: MenuGuncelleIstegi, yon: dict = Depends(yonetici)):
    return yonetim_servisi.menu_guncelle(menu_id, istek)
