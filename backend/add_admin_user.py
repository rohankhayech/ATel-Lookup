import argparse
from controller.authentication import add_admin_user, InvalidCredentialsError

my_parser = argparse.ArgumentParser()
my_parser.add_argument("--username", action="store", type=str, required=True)
my_parser.add_argument("--password", action="store", type=str, required=True)

args = my_parser.parse_args()

try:
    add_admin_user(args.username, args.password)
except InvalidCredentialsError:
    print("ERROR: Could not add admin user")
