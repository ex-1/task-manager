from app.user.constants import pwd_context


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def compare_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
