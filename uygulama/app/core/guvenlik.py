"""
Güvenlik yardımcıları: bcrypt şifre doğrulama ve oturum token üretimi.
Şema şifreleri bcrypt ($2a$, cost 10) ile saklanır; düz şifre asla tutulmaz.
"""
import secrets

import bcrypt


def sifre_dogrula(sifre: str, bcrypt_hash: str) -> bool:
    try:
        return bcrypt.checkpw(sifre.encode("utf-8"), bcrypt_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def token_uret() -> str:
    """Tahmin edilemez oturum anahtarı."""
    return secrets.token_urlsafe(32)
