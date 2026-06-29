import getpass
from ncclient import manager
from ncclient.xml_ import to_ele
from lxml import etree

secret_password = getpass.getpass(prompt="Enter device password: ")

with manager.connect(
        host="127.0.0.1",
        port=830,
        username="readonly",
        password=secret_password,
        hostkey_verify=False,
        device_params={'name': 'default'}
) as m:
    print("Successfully authenticated using SSH Keys!")
