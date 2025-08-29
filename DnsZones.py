from azure.identity import DefaultAzureCredential
from azure.mgmt.dns import DnsManagementClient
from azure.mgmt.dns.models import ARecord, RecordSet
from azure.core.exceptions import ResourceNotFoundError

# Main settings
subscription_id = '<subscription_id>'  # Change to your subscription ID
resource_group_name = "<resource_group>"  # Change to your resource group name
zone_name = "<your_dns_zone>"  # Change to your DNS zone name, e.g., "example.com"
ttl = 3600

# Input your entries here
registros = [
    {"name": "audit-service-homolog", "ip": "<public_ip_address>"},
    {"name": "com-service-homolog", "ip": "<public_ip_address>"},
    {"name": "catalog-service-homolog", "ip": "<public_ip_address>"},
    {"name": "datadoc-service-homolog", "ip": "<public_ip_address>"},
    {"name": "decryptor-service-homolog-service-homolog", "ip": "<public_ip_address>"},
    {"name": "device-service-homolog", "ip": "<public_ip_address>"},
    {"name": "evidence-service-homolog", "ip": "<public_ip_address>"},
    {"name": "hash-service-homolog", "ip": "<public_ip_address>"},
    {"name": "hybridboard-service-homolog", "ip": "<public_ip_address>"},
    {"name": "icat-service-homolog", "ip": "<public_ip_address>"},
    {"name": "inquiry-service-homolog", "ip": "<public_ip_address>"},
    {"name": "interfacerecognition-service-homolog", "ip": "<public_ip_address>"},
    {"name": "log-service-homolog-service-homolog", "ip": "<public_ip_address>"},
    {"name": "maps-service-homolog", "ip": "<public_ip_address>"},
    {"name": "media-service-homolog", "ip": "13.82.228.245"},
    {"name": "monitoring-service-homolog", "ip": "<public_ip_address>"},
    {"name": "report-service-homolog", "ip": "<public_ip_address>"},
    {"name": "security-service-homolog", "ip": "<public_ip_address>"},
    {"name": "user-service-homolog", "ip": "<public_ip_address>"},
    {"name": "verso-service-homolog", "ip": "<public_ip_address>"},    
    
]

# Autentication
credential = DefaultAzureCredential()
dns_client = DnsManagementClient(credential, subscription_id)

def create_or_update_record_set(record_name, ip_address):
    try:
        print(f"\nBuscando Record Set '{record_name}'...")
        record_set = dns_client.record_sets.get(
            resource_group_name,
            zone_name,
            record_name,
            "A"
        )
        print("Record Set encontrado.")
        
        existing_ips = {record.ipv4_address for record in (record_set.a_records or [])}
        if ip_address not in existing_ips:
            print(f"Adicionando IP '{ip_address}' ao Record Set '{record_name}'...")
            record_set.a_records.append(ARecord(ipv4_address=ip_address))
            dns_client.record_sets.create_or_update(
                resource_group_name,
                zone_name,
                record_name,
                "A",
                record_set
            )
            print("IP adicionado com sucesso.")
        else:
            print(f"O IP '{ip_address}' já existe no Record Set '{record_name}'.")
            
    except ResourceNotFoundError:
        print(f"Record Set '{record_name}' não encontrado. Criando novo...")
        record_set_params = RecordSet(
            ttl=ttl,
            a_records=[ARecord(ipv4_address=ip_address)]
        )
        dns_client.record_sets.create_or_update(
            resource_group_name,
            zone_name,
            record_name,
            "A",
            record_set_params
        )
        print("Record Set criado com sucesso.")
    except Exception as e:
        print(f"Erro inesperado ao processar '{record_name}':", e)
        raise

# Looping to processing all registries
for registro in registros:
    create_or_update_record_set(registro["name"], registro["ip"])

print("\n✅ Todos os registros processados.")
