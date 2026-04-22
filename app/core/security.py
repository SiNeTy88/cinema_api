from passlib.context import CryptContext

from authx import AuthX, AuthXConfig

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

configx = AuthXConfig()
configx.JWT_SECRET_KEY = "sinety88_super_secret_key_for_cinema_api_123"
configx.JWT_ACCESS_COOKIE_NAME = "my_access_token"
configx.JWT_TOKEN_LOCATION = ["cookies", "headers"]
configx.JWT_COOKIE_CSRF_PROTECT = False

security = AuthX(config=configx)