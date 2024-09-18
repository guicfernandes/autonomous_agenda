from entities.user import User

class Appointment:
    def __init__(self, id: int, client: User, date: str) -> None:
        id = id
        client = client
        date = date
    
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
