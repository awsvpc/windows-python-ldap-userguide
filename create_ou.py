# Create new sub OU
# Written by Maximilian Thoma 2023
# More infos at https://lanbugs.de

from ldap3 import Connection

AD_SERVER = 'ldap://10.1.1.1'
BACKEND_USER = "CN=Backend User,CN=Users,DC=ad,DC=local"
BACKEND_PASS = "SuperSecret"
base_dn = 'DC=ad,DC=local'

target_ou = 'OU=Assigned,OU=AAAA,' + base_dn

new_ou="C"

conn = Connection(AD_SERVER, user=BACKEND_USER, password=BACKEND_PASS, auto_bind=True)

new_ou_dn = f'OU={new_ou},{target_ou}'

ou_attributes = {
    'objectClass': ['top', 'organizationalUnit'],
    'ou': new_ou
}

conn.add(new_ou_dn, attributes=ou_attributes)
print(conn.result)
conn.unbind()
