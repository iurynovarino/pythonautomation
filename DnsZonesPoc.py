from azure.identity import DefaultAzureCredential
from azure.mgmt.dns import DnsManagementClient
from azure.mgmt.dns.models import ARecord, RecordSet
from azure.core.exceptions import ResourceNotFoundError

# Configurações principais
subscription_id = 'aff87ef7-615a-4815-99d9-c8673c2dfc22'
resource_group_name = "GlobalService"
zone_name = "custodia.seg.br"
ttl = 3600

# Lista de registros que você quer adicionar
registros = [
    {"name": "audit-service-homolog", "ip": "20.233.170.215"},
    {"name": "com-service-homolog", "ip": "20.233.170.215"},
    {"name": "catalog-service-homolog", "ip": "20.233.170.215"},
    {"name": "datadoc-service-homolog", "ip": "20.233.170.215"},
    {"name": "decryptor-service-homolog-service-homolog", "ip": "20.233.170.215"},
    {"name": "device-service-homolog", "ip": "20.233.170.215"},
    {"name": "evidence-service-homolog", "ip": "20.233.170.215"},
    {"name": "hash-service-homolog", "ip": "20.233.170.215"},
    {"name": "hybridboard-service-homolog", "ip": "20.233.170.215"},
    {"name": "icat-service-homolog", "ip": "20.233.170.215"},
    {"name": "inquiry-service-homolog", "ip": "20.233.170.215"},
    {"name": "interfacerecognition-service-homolog", "ip": "20.233.170.215"},
    {"name": "log-service-homolog-service-homolog", "ip": "20.233.170.215"},
    {"name": "maps-service-homolog", "ip": "20.233.170.215"},
    {"name": "media-service-homolog", "ip": "20.233.170.215"},
    {"name": "monitoring-service-homolog", "ip": "20.233.170.215"},
    {"name": "report-service-homolog", "ip": "20.233.170.215"},
    {"name": "security-service-homolog", "ip": "20.233.170.215"},
    {"name": "user-service-homolog", "ip": "20.233.170.215"},
    {"name": "verso-service-homolog", "ip": "20.233.170.215"},    
    # Adicione quantos quiser aqui
]

# Autenticação
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

# Loop para processar todos os registros
for registro in registros:
    create_or_update_record_set(registro["name"], registro["ip"])

print("\n✅ Todos os registros processados.")
