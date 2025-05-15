from passlib.context import CryptContext

# Configure Passlib to use PBKDF2-SHA256
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Hashed passwords
USERS = {
    "jordi": pwd_context.hash("random_pass"),
    "helene": pwd_context.hash("random_pass"),
}
