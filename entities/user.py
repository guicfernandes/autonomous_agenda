class User:
    def __init__(self, id, name, email) -> None:
        id = id
        name = name
        email = email

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


