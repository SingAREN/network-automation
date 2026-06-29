def edit_config_from_payload(payload):
    return m.edit_config(target='running', config=payload)
    
def set_vlan_id(vlan_id, vlan_name):
    payload = f"""
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <interface-vlan xmlns="urn:brocade.com:mgmt:brocade-interface">
            <vlan>
                <name>{vlan_id}</name>
                <vlan-name>{vlan_name}</vlan-name>
            </vlan>
        </interface-vlan>
    </config>
    """
    return payload
