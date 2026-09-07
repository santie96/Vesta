import bcrypt


def create_password_hash(password: str) -> str:
    """
    Crea un hash di password
    """

    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password_hash(password: str, hashed_password: str) -> bool:
    """
    Verifica se la password fornita corrisponde al hash fornito
    """

    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
