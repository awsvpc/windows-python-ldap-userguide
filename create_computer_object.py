# Create computer object in OU
# Written by Maximilian Thoma 2023
# More infos at https://lanbugs.de

from ldap3 import Connection
from ldap3.core.exceptions import LDAPException
import random

BACKEND_USER = "CN=Backend User,CN=Users,DC=ad,DC=local"
BACKEND_PASS = "SuperSecret"

BACKEND_SERVER = "ldap://10.1.1.1"
OU_PATH_U = "OU=Unassigned,OU=AAAA,DC=ad,DC=local"

# random genrators
w = random.randint(1000, 9999)
x = random.randint(100000, 999999)
y = format(random.randint(0, 0xFFFF), '04X')
z = format(random.randint(0, 0xFFFF), '04X')

COMPUTER_NAME = f"XXXX{x}"
NAME = COMPUTER_NAME
SERIAL = f"EC-A08-{y}-{z}"
OSV = "1.0"
OS = "Secure Linux OS"
DESCRIPTION = f"Project XYZ{w}"

try:
    with Connection(BACKEND_SERVER, user=BACKEND_USER, password=BACKEND_PASS, auto_bind=True) as conn:
        computer_dn = "CN={},{}".format(COMPUTER_NAME, OU_PATH_U)
        computer_attributes = {
            'objectClass': ['top', 'person', 'organizationalPerson', 'user', 'computer'],
            'cn': COMPUTER_NAME,
            'serialNumber': SERIAL,
            'operatingSystemVersion': OSV,
            'operatingSystem': OS,
            'description': [DESCRIPTION],
            'sAMAccountName': f'{COMPUTER_NAME}$',
            'userAccountControl': '4096',
        }

        conn.add(computer_dn, attributes=computer_attributes)

        print(f'Computer "{COMPUTER_NAME}" created.')

except LDAPException as e:
    print(e)

conn.unbind()
