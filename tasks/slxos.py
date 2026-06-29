import getpass
from ncclient import manager
from ncclient.xml_ import to_ele
from lxml import etree


def edit_config_from_payload(payload):
    return m.edit_config(target='running', config=payload)
	
def get_config_from_filter(payload):
    return m.get_config(source='running', filter=('subtree', payload))
	
def custom_rpc_get_output(payload):
    return m.dispatch(to_ele(payload))

      
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
