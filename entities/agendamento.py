"""Module to create an Appointment object"""

from entities.user import User


class Appointment:
    """Class to create an Appointment object"""

    def __init__(self, id: int, client: User, date: str) -> None:
        self.id = id
        self.client = client
        self.date = date

    def get_appointment_id(self) -> int:
        """Method to get appointment id

        Returns:
            int: Appointment id
        """
        return self.id

    def get_client(self) -> User:
        """Method to get client User object

        Returns:
            User: Client user
        """
        return self.client

    def get_appointment_date(self) -> str:
        """Method to get appointment date

        Returns:
            str: Appointment date
        """
        return self.date
