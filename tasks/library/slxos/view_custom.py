from lxml import etree


def extract_arp_information(response):
    """
    response: response from get_output_from_rpc function
    return: Full ARP information
    """
    # Safe handling: get raw XML string from ncclient object if available, else stringify
    xml_string = response.xml if hasattr(response, 'xml') else str(response)
    root = etree.fromstring(xml_string.encode('utf-8'))
    
    # FIX 1: Matched the exact namespace string from your switch output
    ns = {
        'base' : 'urn:ietf:params:xml:ns:netconf:base:1.0',
        'arp'  : 'urn:brocade.com:mgmt:brocade-arp'
    }
    
    # FIX 2: Simplified the path to find all <arp-entry> tags anywhere in the tree
    arp_entries = root.xpath('.//arp:arp-entry', namespaces=ns)
    
    # FIX 3: Loop through the list returned by .xpath()
    for arp in arp_entries:
        arp_ip_address = arp.findtext('arp:ip-address', namespaces=ns)
        arp_mac_address = arp.findtext('arp:mac-address', namespaces=ns)
        arp_interface_type = arp.findtext('arp:interface-type', namespaces=ns)
        arp_interface_name = arp.findtext('arp:interface-name', namespaces=ns)
        
        arp_is_resolved = arp.findtext('arp:is-resolved', namespaces=ns)
        if arp_is_resolved == "true":
            arp_is_resolved = True
        else:
            arp_is_resolved = False
            
        arp_vlan_bd_id = arp.findtext('arp:vlan-bd-id', namespaces=ns)
        if arp_vlan_bd_id == '--':
            arp_vlan_bd_id = None
        
        arp_age = arp.findtext('arp:age', namespaces=ns)
        arp_entry_type = arp.findtext('arp:entry-type', namespaces=ns)
        
        print(f"IPv4 Address: \t\t{arp_ip_address}")
        print(f"MAC Address: \t\t{arp_mac_address}")
        print(f"Interface Type: \t{arp_interface_type}")
        print(f"Interface Name: \t{arp_interface_name}")
        print(f"ARP Resolved: \t\t{arp_is_resolved}")
        print(f"VLAN ID: \t\t{arp_vlan_bd_id}")
        print(f"Entry Age: \t\t{arp_age}")
        print(f"Entry Type: \t\t{arp_entry_type}")
        print("-" * 40)
    
