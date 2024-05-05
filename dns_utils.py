import json

def delete_records(client, domain, host, field_type):
    endpoint = f'/domain/zone/{domain}/record'
    ids = client.get(endpoint, fieldType=field_type, subDomain=host)
    for id in ids:
        record_endpoint = f'{endpoint}/{id}'
        record_info = client.get(record_endpoint)
        print(f"DELETE {record_endpoint}", json.dumps(record_info, indent=4))
        client.delete(record_endpoint)

def add_record(client, domain, subDomain, fieldType,target):
    endpoint = f'/domain/zone/{domain}/record'
    result = client.post(endpoint, fieldType=fieldType, subDomain=subDomain, target=target)
    print(f"POST {endpoint}", json.dumps(result, indent=4))

def refresh(client, domain):
    endpoint = f'/domain/zone/{domain}/refresh'
    result = client.post(endpoint)
    print(f"POST {endpoint}")

def export(client, domain):
    endpoint = f'/domain/zone/{domain}/export'
    result = client.get(endpoint)
    print(f"GET {endpoint}")
    print(result)