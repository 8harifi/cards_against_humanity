import os
from dotenv import load_dotenv

load_dotenv()

pepper = os.getenv("PEPPER")
if not pepper:
    pepper = ""
    print('[!] WARNING: PEPPER environment variable was not set! (DEFAULT: no pepper)')

salt_length = os.getenv('SALT_LENGTH')
if salt_length:
    salt_length = int(salt_length)
else:
    salt_length = 24
    print('[!] WARNING: SALT_LENGTH environment variable was not set! (DEFAULT: 24)')
