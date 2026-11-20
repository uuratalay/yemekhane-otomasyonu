"""
Alan (domain) hataları.
Tek bir taban hata (UygulamaHatasi) tüm kullanıcıya gösterilebilir durumları
temsil eder; main.py'deki tek exception handler bunları {"hata": mesaj}
JSON'una çevirir. Böylece "hata mesajını arayüze taşıma" mantığı tek yerdedir.
"""


class UygulamaHatasi(Exception):
    """Kullanıcıya gösterilebilir hata. kod = HTTP durum kodu."""
    def __init__(self, mesaj: str, kod: int = 400):
        super().__init__(mesaj)
        self.mesaj = mesaj
        self.kod = kod


class IsKuraliHatasi(UygulamaHatasi):
    """
    Stored procedure'den gelen SIGNAL SQLSTATE '45000' (MySQL errno 1644).
    Türkçe mesaj (ör. 'Bakiye yetersiz.') DEĞİŞTİRİLMEDEN taşınır.
    """
    pass


class KimlikHatasi(UygulamaHatasi):
    def __init__(self, mesaj: str = "Oturum geçersiz. Lütfen tekrar giriş yapın."):
        super().__init__(mesaj, kod=401)


class YetkiHatasi(UygulamaHatasi):
    def __init__(self, mesaj: str = "Bu işlem için yetkiniz yok."):
        super().__init__(mesaj, kod=403)
