"""Module to implement utility functions for the application."""

import json
from werkzeug.security import generate_password_hash


def read_json_asset_file(file_name: str) -> dict:
    """Get data from mail_data.json file

    Args:
        file_name (str): Name of the file to be ridden

    Returns:
        dict: mail_data information in dict object
    """
    with open(f"./assets/{file_name}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def get_sender_information() -> tuple[str, str]:
    """Get sender information

    Returns:
        tuple[str, str]: Sender e-mail and pass
    """
    data = read_json_asset_file(file_name="mail_data")
    sender_email = data["sender_email"]
    sender_pass = data["sender_pass"]
    return sender_email, sender_pass


def get_smtp_data() -> tuple[str, str]:
    """Get SMTP information

    Returns:
        tuple[str, str]: SMTP server and port
    """
    data = read_json_asset_file(file_name="mail_data")
    smtp_server = data["smtp_server"]
    smtp_port = data["smtp_port"]
    return smtp_server, smtp_port


def hash_password(password) -> str:
    """Method to set user password

    Returns:
        password (str): User password hashed
    """
    return generate_password_hash(password)
