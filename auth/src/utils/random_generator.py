import secrets
import string


def random_string(size):
    letters = string.ascii_lowercase+string.ascii_uppercase+string.digits
    return ''.join(secrets.choice(letters) for _ in range(size))
