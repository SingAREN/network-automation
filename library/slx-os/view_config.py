from lxml import etree


def pretty_print_response(response):
    print(etree.tostring(response.data_ele, pretty_print=True, encoding='utf-8').decode('utf-8'))
    return


def extract_vlan_configuration(response):
    xml_string = response.data_xml
    root = etree.fromstring(xml_string.encode('utf-8'))
    ns = {
        'br'  : 'urn:brocade.com:mgmt:brocade-interface',
        'xstp': 'urn:brocade.com:mgmt:brocade-xstp'
    }
    
    vlans = root.xpath('.//br:interface-vlan/br:vlan',namespaces=ns)
    
    for vlan in vlans:
        vlan_id = vlan.findtext('br:name', namespaces=ns)
        vlan_name = vlan.findtext('br:vlan-name', namespaces=ns)
    
        statistics = vlan.xpath('br:statistics', namespaces=ns)
        statistics_status = True if statistics else False
        
        ve_config = vlan.xpath('.//br:router-interface/br:ve-config/text()', namespaces=ns)
        ve_val = ve_config[0] if ve_config else "N/A"
        
        # Check if spanning-tree shutdown is present (uses the second namespace)
        stp_shutdown = vlan.xpath('.//xstp:spanning-tree/xstp:stp-shutdown', namespaces=ns)
        stp_status = False if stp_shutdown else True
        
        print(f"VLAN ID: \t\t{vlan_id}")
        print(f"Name: \t\t\t{vlan_name}")
        print(f"VLAN Statistics: \t{statistics_status}")
        print(f"Router Interface: \t{ve_val}")
        print(f"STP Status: \t\t{stp_status}")
        print("-" * 40)


def extract_interface_information(response):
    xml_string = response.data_xml
    root = etree.fromstring(xml_string.encode('utf-8'))
    ns = {
        'br'   : 'urn:brocade.com:mgmt:brocade-interface',
        'ipv4' : 'urn:brocade.com:mgmt:brocade-ip-config',
        'ipv6' : 'urn:brocade.com:mgmt:brocade-ipv6-config',
        'nd-ra': 'urn:brocade.com:mgmt:brocade-ipv6-nd-ra',
        'icmp' : 'urn:brocade.com:mgmt:brocade-icmp',
        'lldp' : 'urn:brocade.com:mgmt:brocade-lldp',
        'lacp' : 'urn:brocade.com:mgmt:brocade-lacp',
        'xstp' : 'urn:brocade.com:mgmt:brocade-xstp',
        'sflow': 'urn:brocade.com:mgmt:brocade-sflow'
    }
    
    interfaces = root.xpath('.//br:interface/br:ethernet',namespaces=ns)
    
    for interface in interfaces:
        interface_id = interface.findtext('br:name', namespaces=ns)
        interface_description = interface.findtext('br:description', namespaces=ns)
        interface_mtu = interface.findtext('br:mtu', namespaces=ns)

        """
        <sflow xmlns="urn:brocade.com:mgmt:brocade-sflow">
            <enable/>
        </sflow>
        """
        sflow = interface.xpath('.//sflow:sflow/sflow:enable', namespaces=ns)
        sflow_status = True if sflow else False
        """
        <switchport-basic>
          <basic/>
        </switchport-basic>
        <switchport>
          <mode>
            <vlan-mode>trunk</vlan-mode>
          </mode>
          <trunk>
            <allowed>
              <vlanoper>
                <vlan>
                  <add>102</add>
                </vlan>
              </vlanoper>
              <vlan>
                <add>102</add>
              </vlan>
            </allowed>
            <tag>
              <native-vlan/>
            </tag>
            <native-vlan-classification>
              <native-vlan-id>1</native-vlan-id>
            </native-vlan-classification>
          </trunk>
        </switchport>
        """
        switchport = interface.findtext('br:switchport-basic/br:basic', namespaces=ns)
        switchport_mode = interface.findtext('br:switchport/br:mode/br:vlan-mode', namespaces=ns)
        switchport_trunk_vlans = interface.xpath('br:switchport/br:trunk/br:allowed/br:vlan/br:add/text()', namespaces=ns)
        switchport_access_vlan = interface.findtext('br:switchport/br:access/br:accessvlan', namespaces=ns)

        """
        <spanning-tree xmlns="urn:brocade.com:mgmt:brocade-xstp">
          <edgeport>
            <edgeportbasic/>
          </edgeport>
        </spanning-tree>
        """
        spanning_tree_edge_port = interface.xpath('.//xstp:spanning-tree/xstp:edgeport/xstp:edgeportbasic', namespaces=ns)
        spanning_tree_edge_port_status = True if spanning_tree_edge_port else False

        """
        <ip>
          <ip-config xmlns="urn:brocade.com:mgmt:brocade-ip-config">
            <address>
              <address>192.168.0.100/31</address>
            </address>
          </ip-config>
          <icmp xmlns="urn:brocade.com:mgmt:brocade-icmp">
            <echo-reply/>
          </icmp>
        </ip>
        """
        ipv4_addresses = interface.xpath('.//br:ip/ipv4:ip-config/ipv4:address/ipv4:address/text()', namespaces=ns)
        ip_mtu = interface.findtext('.//br:ip/ipv4:ip-config/ipv4:mtu', namespaces=ns)
        ipv4_icmp_echo_reply = interface.xpath('.//br:ip/icmp:icmp/icmp:echo-reply', namespaces=ns)
        ipv4_icmp_echo_reply_status = True if ipv4_icmp_echo_reply else False        
        
        """
        <ipv6>
          <ipv6-nd-ra xmlns="urn:brocade.com:mgmt:brocade-ipv6-nd-ra">
            <ipv6-intf-cmds>
              <nd>
                <suppress-ra>
                  <suppress-ra-all/>
                </suppress-ra>
              </nd>
            </ipv6-intf-cmds>
          </ipv6-nd-ra>
          <ipv6-config xmlns="urn:brocade.com:mgmt:brocade-ipv6-config">
            <address>
              <ipv6-address>
                <address>de8::/64</address>
              </ipv6-address>
            </address>
          </ipv6-config>
          <icmpv6 xmlns="urn:brocade.com:mgmt:brocade-icmp">
            <echo-reply/>
          </icmpv6>
        </ipv6>
        """
        ipv6_addresses = interface.xpath('.//br:ipv6/ipv6:ipv6-config/ipv6:address/ipv6:ipv6-address/ipv6:address/text()', namespaces=ns)
        ipv6_icmp_echo_reply = interface.xpath('.//br:ipv6/icmp:icmpv6/icmp:echo-reply', namespaces=ns)
        ipv6_icmp_echo_reply_status = True if ipv6_icmp_echo_reply else False  
        ipv6_nd_suppress_ra_all = interface.xpath('.//br:ipv6/nd-ra:ipv6-nd-ra/nd-ra:ipv6-intf-cmds/nd-ra:nd/nd-ra:suppress-ra/nd-ra:suppress-ra-all', namespaces=ns)
        ipv6_nd_suppress_ra_all_status = True if ipv6_nd_suppress_ra_all else False

        port_channel_interface = interface.findtext('.//br:channel-group/br:port-int', namespaces=ns)
        port_channel_mode = interface.findtext('.//br:channel-group/br:mode', namespaces=ns)
        port_channel_type = interface.findtext('.//br:channel-group/br:type', namespaces=ns)
            
        lacp = interface.findtext('.//lacp:lacp/lacp:timeout', namespaces=ns)

        #lldp = interface.findtext('.//lldp:lldp/lldp:cee/lldp:lldp-cee-on-off', namespaces=ns)      
        
        print(f"Interface ID: \t\tEthernet {interface_id}")
        print(f"Description: \t\t{interface_description}")
        print(f"Interface MTU: \t\t{interface_mtu}")
        print(f"sFlow Status: \t\t{sflow_status}")

        if switchport_mode:
            print(f"Interface Type: \tSwitchport")
            print(f"Switchport Mode: \t{switchport_mode}")
            trunk_vlans = ", ".join(switchport_trunk_vlans)
            if not trunk_vlans:
                trunk_vlans = None
            print(f"Trunk VLANs: \t\t{trunk_vlans}")
            print(f"Access VLAN: \t\t{switchport_access_vlan}")
        
        if spanning_tree_edge_port:
            print(f"STP Edge Port: \t\t{spanning_tree_edge_port_status}")
        
        if ipv4_addresses or ipv6_addresses:
            print(f"Interface Type: \tRouted")

        if ipv4_addresses:
            addresses = ", ".join(ipv4_addresses)
            print(f"IPv4 Addresses: \t{addresses}")
            print(f"IPv4 ICMP Echo-Reply: \t{ipv4_icmp_echo_reply_status}")
        
        if ip_mtu:
            print(f"IP MTU: \t\t{ip_mtu}")
  
        if ipv6_addresses:
            addresses = ", ".join(ipv6_addresses)
            print(f"IPv6 Addresses: \t{addresses}")
            print(f"IPv6 ICMP Echo-Reply: \t{ipv6_icmp_echo_reply_status}")
            print(f"IPv6 ND RA Supress All: {ipv6_nd_suppress_ra_all_status}")
        
        if port_channel_interface:
            print(f"Port-Channel: \t\tPo {port_channel_interface}")
            print(f"Port-Channel Mode: \t{port_channel_mode}")
            print(f"Port-Channel Type: \t{port_channel_type}")
        if lacp:
            print(f"LACP Timeout: \t\t{lacp}")
        #if lldp:
        #    print(f"LLDP Cee: \t\t{lldp}")
        
        print("-" * 40)
