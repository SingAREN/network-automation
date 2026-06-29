yang = [
    'brocade-common-def',
    'brocade-interface',
    'brocade-bfd',
    'brocade-system-capabilities',
    'brocade-bridge-domain',
    'brocade-bgp',
]

for model in yang:
    schema = m.get_schema(identifier=model)
        
        # Print it out or save it to a local file
    with open(f"{model}.yang", "w") as f:
        f.write(schema.data)
        
    print(f"Success! Saved to {model}.yang")
