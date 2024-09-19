class UserNotFoundException(Exception):
    """Exception raised when a user is not found in the database."""
    
    def __init__(self, user_name: str, user_email: str, message: str = "User not found in the database"):
        self.user_name = user_name
        self.message = message
        self.user_email = user_email
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.user_name}, {self.user_email}'

class AppointmentNotFoundException(Exception):
    """Exception raised when an appointment is not found in the database."""
    
    def __init__(self, date: str, user_name: str = None, user_email: str = None, message: str ="Appointment not found in the database"):
        self.user_name = user_name
        self.message = message
        self.user_email = user_email
        self.date = date
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: User: {self.user_name}, e-mail: {self.user_email}, date: {self.date}'

class NoAppointmentsForSpecifiedPeriod(Exception):
    """Exception raised when there are no appointments for the specified period."""
    
    def __init__(self, message: str = "No appointments in agenda"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
