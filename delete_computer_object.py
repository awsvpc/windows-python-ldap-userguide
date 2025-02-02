# Delete computer
# Written by Maximilian Thoma 2023
# More infos at https://lanbugs.de

from ldap3 import Connection, SUBTREE, ALL_ATTRIBUTES

AD_SERVER = 'ldap://10.1.1.1'
BACKEND_USER = "CN=Backend User,CN=Users,DC=ad,DC=local"
BACKEND_PASS = "SuperSecret"

COMPUTER_DN = 'CN=XXXX182410,OU=A,OU=Assigned,OU=AAAA,DC=ad,DC=local'

conn = Connection(AD_SERVER, user=BACKEND_USER, password=BACKEND_PASS, auto_bind=True)

conn.delete(COMPUTER_DN)

if not conn.result['result']:
    print(f"computer {COMPUTER_DN} deleted.")
else:
    print(f"computer {COMPUTER_DN} NOT deleted.")

conn.unbind()
