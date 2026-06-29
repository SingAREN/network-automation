from ncclient.xml_ import to_ele

def get_output_from_rpc(rpc_input):
    return m.dispatch(to_ele(rpc_input))

# Get resource information from device (not device configuration)
def get_vlan_info(vlan_id):
    rpc_input = f"""
    <get-vlan-brief xmlns="urn:brocade.com:mgmt:brocade-interface-ext">
        <vlan-id>{vlan_id}</vlan-id>
    </get-vlan-brief>
    """
    return get_output_from_rpc(rpc_input)

def get_arp_info(ip_address):
    rpc_input = f"""
    <get-arp xmlns="urn:brocade.com:mgmt:brocade-arp">
        <ip-address>{ip_address}</ip-address>
    </get-arp>
    """
    return get_output_from_rpc(rpc_input)
