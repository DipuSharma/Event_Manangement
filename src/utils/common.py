from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class EncryptedPassword:
    @staticmethod
    def get_hash_passssword(plain_password):
        return pwd_context.hash(plain_password)

    @staticmethod
    def verify_hash_password(plain_password, hash_password):
        verified = pwd_context.verify(plain_password, hash_password)
        if verified:
            return True
        else:
            return False
