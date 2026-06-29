from ncclient import manager
from ncclient.xml_ import to_ele
from lxml import etree


def get_output_from_rpc(rpc_input):
    return m.dispatch(to_ele(rpc_input))

def get_output_from_filter(rpc_filter):
    return m.get_config(source='running', filter=('subtree', rpc_filter))


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


# Get configuration information from payload
def get_interface_vlan_from_id(vlan_id):
    # This is specifically L2 VLANs, not VEs when configuring L3 interface
    
    payload_filter = f"""
    <interface-vlan xmlns="urn:brocade.com:mgmt:brocade-interface">
        <vlan>
            <name>{vlan_id}</name>
        </vlan>
    </interface-vlan>
    """
    return get_output_from_filter(payload_filter)
    
def get_interface_ethernet_config(ethernet_interface):
    payload_filter = f"""
    <interface xmlns="urn:brocade.com:mgmt:brocade-interface">
        <ethernet>
            <name>{ethernet_interface}</name>
        </ethernet>
    </interface>
    """
    return get_output_from_filter(payload_filter)

def get_interface_lag_config(lag_interface):
    payload_filter = f"""
    <interface xmlns="urn:brocade.com:mgmt:brocade-interface">
        <port-channel>
            <name>{lag_interface}</name>
        </port-channel>
    </interface>
    """
    return get_output_from_filter(payload_filter)

def get_bgp_full_config():
    payload_filter = f"""
    <routing-system xmlns="urn:brocade.com:mgmt:brocade-common-def">
        <router>
            <router-bgp xmlns="urn:brocade.com:mgmt:brocade-bgp"/>
        </router>
    </routing-system>
    """
    return get_output_from_filter(payload_filter)
