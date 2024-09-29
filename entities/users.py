"""Module to create Users entity"""

from werkzeug.security import generate_password_hash, check_password_hash


class Users:
    """Class to create Users entity"""

    def __init__(
        self,
        user_id: str,
        first_name: str,
        last_name: str,
        email: str,
        birth_date: str,
        password: str = None,
        created_at: str = None,
        updated_at: str = None,
    ) -> None:
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_user_password(password) if password else None
        self.birth_date = birth_date
        self.created_at = created_at
        self.updated_at = updated_at

    def get_user_id(self) -> int:
        """Method to get user id

        Returns:
            int: User id
        """
        return self.id

    def get_user_first_name(self) -> str:
        """Method to get user first name

        Returns:
            str: User name
        """
        return self.first_name

    def get_user_last_name(self) -> str:
        """Method to get user last name

        Returns:
            str: User name
        """
        return self.last_name

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

    def check_user_password(self, password) -> bool:
        """Method to check user password

        Args:
            password (str): User password

        Returns:
            bool: True if password is correct, False otherwise
        """
        return check_password_hash(self.password, password)

    def get_user_birth_date(self) -> str:
        """Method to get user birth date

        Returns:
            str: User birth date
        """
        return self.birth_date

    def get_user_created_at(self) -> str:
        """Method to get user created at

        Returns:
            str: User created at
        """
        return self.created_at

    def get_user_updated_at(self) -> str:
        """Method to get user updated at

        Returns:
            str: User updated at
        """
        return self.updated_at
