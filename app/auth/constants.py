from enum import Enum

from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/security/token")


class MediaEnum(str, Enum):
    audio = "audio"
    video = "video"
