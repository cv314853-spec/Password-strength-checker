import re
import getpass

COMMON_PASSWORDS = {
    "password",
    "12345678",
    "123456789",
    "qwerty",
    "admin",
    "letmein",
    "welcome",
    "password123"
}


def has_common_pattern(password):
    patterns = [
        r"^[a-zA-Z]+@123$",
        r"^[a-zA-Z]+123$",
        r"^[a-zA-Z]+@1234$",
        r"^[a-zA-Z]+(19[89][0-9]|20[0-2][0-9]|2030)$",
        r"^[a-zA-Z]+@[0-9]{4}$"
    ]

    return any(re.match(pattern, password) for pattern in patterns)


def check_password(password):
    score = 0
    suggestions = []

    # Common password check
    if password.lower() in COMMON_PASSWORDS:
        return 0, [
            "This is a commonly used password. Choose a different one."
        ]

    # Predictable pattern check
    if has_common_pattern(password):
        suggestions.append(
            "Avoid predictable patterns such as name@123 or name+birth-year."
        )
        score -= 2

    # Length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append(
            "Use at least 8 characters; 12+ characters is better."
        )

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add an uppercase letter.")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add a lowercase letter.")

    # Number
    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Add a number.")

    # Special character
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        suggestions.append("Add a special character.")

    return max(score, 0), suggestions


# Main program
print("=" * 45)
print("       PASSWORD STRENGTH CHECKER")
print("=" * 45)

password = getpass.getpass("Enter password to test: ")

score, suggestions = check_password(password)

# Strength calculation
if score <= 2:
    strength = "Weak"
elif score <= 4:
    strength = "Medium"
else:
    strength = "Strong"

print("\nPassword Strength:", strength)

if suggestions:
    print("\nSuggestions:")

    for suggestion in suggestions:
        print("- " + suggestion)
else:
    print("\nNo major weaknesses detected.")

print("\nSecurity Note:")
print("Your password is not stored by this program.")
