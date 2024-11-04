import os


# Check if password meets minimum length requirement
def check_length(password):
    """Checks if password meets minimum length requirement."""
    return len(password) >= 8


# Check for uppercase, lowercase, numeric, and special characters excluding spaces
def check_char_types(password):
    """Checks for uppercase, lowercase, numeric, and special characters (excluding spaces)."""
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(
        not c.isalnum() and c != " " for c in password
    )  # Excludes spaces as special
    return has_upper and has_lower and has_digit and has_special


# Check if password exists in common password dataset
def load_common_passwords():
    """Loads a set of common passwords from a file for easy lookup."""
    file_path = os.path.join(
        os.path.dirname(__file__), "../data/processed/probable-v2-top12000.txt"
    )
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    with open(file_path) as file:
        return set(file.read().splitlines())


# Load common passwords at the start
COMMON_PASSWORDS = load_common_passwords()


def is_common_password(password):
    """Checks if the given password is in the common password list."""
    return password in COMMON_PASSWORDS


# Refine password strength categorization
def categorize_strength(row):
    """Categorizes password strength based on certain criteria."""
    length = row["length"]
    has_number = row["has_number"]
    has_uppercase = row["has_uppercase"]
    has_lowercase = row["has_lowercase"]
    has_special = row["has_special"]

    # Strong password criteria
    if length >= 12 and has_number and has_uppercase and has_lowercase and has_special:
        return "strong"

    # Moderate password criteria
    elif length >= 8 and (
        has_number + has_uppercase + has_lowercase + has_special >= 3
    ):
        return "moderate"

    # Weak password criteria
    else:
        return "weak"


# Extra function to assess password properties
def analyze_password_strength(password):
    """Analyzes a password and provides a strength assessment directly."""
    password_data = {
        "password": password,
        "has_number": any(c.isdigit() for c in password),
        "has_uppercase": any(c.isupper() for c in password),
        "has_lowercase": any(c.islower() for c in password),
        "has_special": any(
            not c.isalnum() and c != " " for c in password
        ),  # Excludes spaces
        "length": len(password),
    }
    return categorize_strength(password_data)
