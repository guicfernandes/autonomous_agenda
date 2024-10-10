"""Module to create forms for the application"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from dao.users import get_user_by_email, create_user
from utils.exceptions import UserNotFoundException, UserRegistrationError
from utils.util import hash_password


class LoginForm(FlaskForm):
    """Class to create a Login Form

    Args:
        FlaskForm (_type_): FlaskForm class
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=30)]
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

    def validate_user(self, email: str, password: str) -> None:
        """Method to validate if user email and password are correct

        Args:
            email (str): Email to validate
            password (str): Password to validate

        Raises:
            ValidationError: Exception raised when email and password are incorrect
        """
        try:
            user = get_user_by_email(email)
            if user.check_user_password(password=password):
                return True
            raise ValidationError("Login Unsuccessful. Please check email and password")
        except UserNotFoundException as e:
            raise ValidationError(
                "Login Unsuccessful. Please check email and password"
            ) from e


class RegisterForm(FlaskForm):
    """Class to create a Register Form

    Args:
        FlaskForm (_type_): FlaskForm class

    Raises:
        ValidationError: Exception raised when form validation fails
    """

    first_name = StringField("Name", validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(min=2, max=60)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=30)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), Length(min=6, max=30), EqualTo("password")],
    )
    birth_date = DateField("Birth Date", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Register Now")

    def validate_registration(self) -> bool:
        """Method to validate user registration

        Raises:
            ValidationError: Exception raised when user already exists
            ValidationError: Exception raised when user registration fails

        Returns:
            bool: True if registration is successful
        """
        try:
            user = get_user_by_email(self.email.data)
            if user:
                raise ValidationError("Email already registered")
        except UserNotFoundException:
            try:
                create_user(
                    first_name=self.first_name.data,
                    last_name=self.last_name.data,
                    email=self.email.data,
                    password=hash_password(self.password.data),
                    birth_date=self.birth_date.data.strftime("%Y-%m-%d"),
                )
                return True
            except Exception as e:
                raise UserRegistrationError(user_email=self.email.data) from e
