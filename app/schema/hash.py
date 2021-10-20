# app/schema/hash.py
# Password encryption

from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    """Helps to hash and verifying passwords using multiple algorithms."""

    @staticmethod
    def bcrypt(password: str) -> str:
        """Encrypts the password entered by the user.

        Args:
            password (str): Password entered by the user.

        Returns:
            str: Hashed password.
        """

        return pwd_ctx.hash(password)

    def verify(hashed_password: str, plain_password: str) -> bool:
        """Check if the hashed password matches the entered password.
        Args:
            hashed_password (str): Hashed password.
            plain_password (str): Password entered by the user.

        Returns:
            bool: True if there is a match but False.
        """

        return pwd_ctx.verify(plain_password, hashed_password)
