"""
YonetimDeposu — yönetici menü işlemleri.
Menü oluşturma/güncelleme birden çok tabloya yazdığı için açık transaction
kullanır (menuler + menu_yemekleri birlikte ya hep ya hiç). Özet/rapor REPLİKA'dan.
"""
import mysql.connector

from .temel_depo import TemelDepo


class YonetimDeposu(TemelDepo):

    def menu_olustur(self, yemekhane_id, tarih, ogun_id, ogr_fiyat, per_fiyat, yemek_idler):
        with self._baglanti.yazma() as conn:
            conn.autocommit = False
            imlec = conn.cursor()
            try:
                imlec.execute(
                    "INSERT INTO menuler "
                    "(yemekhane_id, tarih, ogun_id, ogrenci_fiyati, personel_fiyati) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (yemekhane_id, tarih, ogun_id, ogr_fiyat, per_fiyat),
                )
                menu_id = imlec.lastrowid
                imlec.executemany(
                    "INSERT INTO menu_yemekleri (menu_id, yemek_id) VALUES (%s, %s)",
                    [(menu_id, y) for y in yemek_idler],
                )
                conn.commit()
                return menu_id
            except mysql.connector.Error as hata:
                conn.rollback()
                raise self._cevir(hata)
            finally:
                conn.autocommit = True
                imlec.close()

    def menu_guncelle(self, menu_id, ogr_fiyat, per_fiyat, yemek_idler):
        with self._baglanti.yazma() as conn:
            conn.autocommit = False
            imlec = conn.cursor()
            try:
                imlec.execute(
                    "UPDATE menuler SET ogrenci_fiyati = %s, personel_fiyati = %s "
                    "WHERE id = %s",
                    (ogr_fiyat, per_fiyat, menu_id),
                )
                imlec.execute("DELETE FROM menu_yemekleri WHERE menu_id = %s", (menu_id,))
                imlec.executemany(
                    "INSERT INTO menu_yemekleri (menu_id, yemek_id) VALUES (%s, %s)",
                    [(menu_id, y) for y in yemek_idler],
                )
                conn.commit()
            except mysql.connector.Error as hata:
                conn.rollback()
                raise self._cevir(hata)
            finally:
                conn.autocommit = True
                imlec.close()

    def menu_listesi(self):
        return self.oku_liste(
            """
            SELECT d.menu_id, d.tarih, d.ogun_id, d.ogun, d.yemekhane,
                   d.kapasite, d.rezerve, d.bos_yer, d.doluluk_yuzde,
                   p.oy_sayisi, p.ortalama_puan
              FROM v_menu_doluluk d
              JOIN v_menu_puan p ON p.menu_id = d.menu_id
             WHERE d.tarih BETWEEN CURDATE() AND CURDATE() + INTERVAL 6 DAY
             ORDER BY d.tarih, d.ogun_id
            """
        )

    def ozet(self, menu_id: int):
        return self.oku_tek(
            """
            SELECT d.menu_id, d.tarih, d.ogun, d.yemekhane, d.kapasite,
                   d.rezerve, d.bos_yer, d.doluluk_yuzde,
                   p.oy_sayisi, p.ortalama_puan,
                   m.ogrenci_fiyati, m.personel_fiyati
              FROM v_menu_doluluk d
              JOIN v_menu_puan p ON p.menu_id = d.menu_id
              JOIN menuler m     ON m.id = d.menu_id
             WHERE d.menu_id = %s
            """,
            (menu_id,),
        )

    def menu_yemek_idleri(self, menu_id: int):
        satirlar = self.oku_liste(
            "SELECT yemek_id FROM menu_yemekleri WHERE menu_id = %s", (menu_id,))
        return [s["yemek_id"] for s in satirlar]

    def baslik(self, menu_id: int):
        """Önbellek anahtarı için menünün yemekhane/tarih/öğün bilgisi."""
        return self.oku_tek(
            "SELECT yemekhane_id, tarih, ogun_id FROM menuler WHERE id = %s",
            (menu_id,),
        )
