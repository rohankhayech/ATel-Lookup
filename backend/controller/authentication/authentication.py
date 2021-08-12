from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

import model.db_helper
from model.db_helper import ExistingUserError, get_hashed_password


class InvalidCredentialsError(Exception):
    """
    Raised when the credentials provided are invalid.
    """


def add_admin_user(username: str, password: str):
    """
    Creates a new admin user with specified username and password.

    Args:
        username (str): Username of the account
        password (str): Password of the account

    Raises:
        InvalidCredentialsError: Raised when user already exists or credentials don't meet requirements
    """

    hashed = generate_password_hash(password)
    try:
        model.db_helper.add_admin_user(
            username,
            password=hashed,
        )
    except ExistingUserError:
        raise InvalidCredentialsError()
    except ValueError:
        raise InvalidCredentialsError()


def login(username: str, password: str):
    """
    Creates an access token if given credentials are valid.

    Args:
        username (str): Username of the account
        password (str): Password of the account

    Raises:
        InvalidCredentialsError: Raised when credentials are not valid for the account

    Returns:
        string: An access token for the account
    """

    hashed = get_hashed_password(username)
    if not check_password_hash(hashed, password):
        raise InvalidCredentialsError()

    access_token = create_access_token(identity=username)
    return access_token
