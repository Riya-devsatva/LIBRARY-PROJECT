from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes= ["bcrypt"], deprecated = "auto")

class Hash():
    """ password hashing """
    def bcrypt(self, password: str):
        """ bcrypt the password """
        return pwd_cxt.hash(password)
    def verify(self, hashed_password, plain_password):
        """ verify the hashed password """
        return pwd_cxt.verify(plain_password, hashed_password)
    