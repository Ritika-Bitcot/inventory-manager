"""
def login(username: str, password: str)->None:
    # Check credentials
    if username == "admin" and password == "1234":
        print("Login successful!")
        # Log activity
        with open("log.txt", "a") as f:
            f.write(f"{username} logged in\n")
    else:
        print("Login failed!")

Problem:
This function is:

Verifying user credentials

Handling output

Logging to a file

3 responsibilities = SRP broken.

"""

def is_valid_user(username: str, password: str)->bool:
    """
    Check if the given username and password are valid.
    """
    return username == "admin" and password == "1234"

def show_login_message(success: bool)->None:
    """
    Display a login message based on the success parameter.
    """
    if success:
        print("Login successful!")
    else:
        print("Login failed!")

def log_login_activity(username: str)->None:
    """
    Log the login activity to a file.
    """
    with open("log.txt", "a") as f:
        f.write(f"{username} logged in\n")

user = input("Username: ")
pwd = input("Password: ")

success = is_valid_user(user, pwd)
show_login_message(success)

if success:
    log_login_activity(user)
