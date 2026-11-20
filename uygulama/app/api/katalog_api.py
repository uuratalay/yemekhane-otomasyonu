"""Katalog uçları: formlar için referans veriler (yemekhane, öğün, yemek, alerjen)."""
from fastapi import APIRouter, Depends

from .bagimliliklar import katalog_depo, mevcut_kullanici

router = APIRouter(prefix="/api")


@router.get("/katalog")
def katalog(kullanici: dict = Depends(mevcut_kullanici)):
    return {
        "yemekhaneler": katalog_depo.yemekhaneler(),
        "ogunler": katalog_depo.ogunler(),
        "alerjenler": katalog_depo.alerjenler(),
        "yemekler": katalog_depo.yemekler(),
        "bugun": katalog_depo.bugun(),
    }
