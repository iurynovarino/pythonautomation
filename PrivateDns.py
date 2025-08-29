from azure.identity import DefaultAzureCredential
from azure.mgmt.privatedns import PrivateDnsManagementClient
from azure.mgmt.privatedns.models import ARecord, RecordSet

# Variables declaration
subscription_id = '<subscription_id>'  # Change to your subscription ID
resource_group_name = "<resource_group>" # Change to your resource group name
zone_name = "<your_private_dns_zone>"  # Change to your Private DNS Zone name, e.g., "myprivatednszone.com"
ip_servidor = "<public_ip_address>" # Change to your server's private IP address

# Services list
servicos = [
    "audit-service-homolog",
    "catalog-service-homolog",
    "communication-service-homolog",
    "device-service-homolog",
    "maps-service-homolog",
    "media-service-homolog",
    "monitoring-service-homolog",
    "report-service-homolog",
    "security-service-homolog",
    "user-service-homolog",
]

# Autentication and client setup
credential = DefaultAzureCredential()
private_dns_client = PrivateDnsManagementClient(credential, subscription_id)

def create_or_update_private_dns_record(record_name, ip_address):
    try:
        print(f"\nCriando ou atualizando Record Set '{record_name}'...")

        record_set_params = RecordSet(
            ttl=3600,
            a_records=[ARecord(ipv4_address=ip_address)]
        )

        private_dns_client.record_sets.create_or_update(
            resource_group_name=resource_group_name,
            private_zone_name=zone_name,
            record_type="A",  # Aqui o tipo precisa ser 'A' para Private DNS
            relative_record_set_name=record_name,
            parameters=record_set_params
        )
        print(f"✅ Record Set '{record_name}' criado/atualizado com sucesso.")

    except Exception as e:
        print(f"❌ Erro ao processar '{record_name}':", e)
        raise

# Looping to add all services
for service in servicos:
    create_or_update_private_dns_record(service, ip_servidor)

print("\n✅ Todos os registros Private DNS foram criados ou atualizados com sucesso!")
