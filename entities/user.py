"""Module to create a User entity"""

from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """Class to create a User entity"""

    def __init__(self, id, name, email) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = None

    def get_user_id(self) -> int:
        """Method to get user id

        Returns:
            int: User id
        """
        return self.id

    def get_user_name(self) -> str:
        """Method to get user name

        Returns:
            str: User name
        """
        return self.name

    def get_user_email(self) -> str:
        """Method to get user email

        Returns:
            str: User email
        """
        return self.email

    def set_user_password(self, password) -> None:
        """Method to set user password

        Args:
            password (str): User password
        """
        self.password = generate_password_hash(password)

    def get_user_password(self) -> str:
        """Method to get user password

        Returns:
            str: User password
        """
        return self.password

    def check_user_password(self, password) -> bool:
        """Method to check user password

        Args:
            password (str): User password

        Returns:
            bool: True if password is correct, False otherwise
        """
        return check_password_hash(self.password, password)
