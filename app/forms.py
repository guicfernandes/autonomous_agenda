"""Module to create forms for the application"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from dao.users import get_user_by_email
from utils.exceptions import UserNotFoundException


class LoginForm(FlaskForm):
    """Class to create a Login Form

    Args:
        FlaskForm (_type_): FlaskForm class
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=20)]
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
        "Password", validators=[DataRequired(), Length(min=6, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), Length(min=6, max=20), EqualTo("password")],
    )
    submit = SubmitField("Register Now")

    def validate_email(self, email: str) -> None:
        """Method to validate if user email already exists in the database

        Args:
            email (str): Email to validate

        Raises:
            ValidationError: Exception raised when email already exists in the database
        """
        if get_user_by_email(email=email.data):
            raise ValidationError(
                "That email is already in use. Please choose a different one."
            )
