from azure.identity import DefaultAzureCredential
from azure.mgmt.privatedns import PrivateDnsManagementClient
from azure.mgmt.privatedns.models import ARecord, RecordSet

# Variáveis principais
subscription_id = 'sua subscription_id'  # Substitua pelo ID da sua assinatura
resource_group_name = "GlobalService" # Substitua pelo nome do seu grupo de recursos
zone_name = "sua zone_name"  # Substitua pelo nome da sua zona DNS privada
ip_servidor = "10.21.0.120" #Inserir o IP do backend que será utilizado pelos serviços

# Lista dos serviços 
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

# Autenticação
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

# Loop para adicionar todos os serviços
for service in servicos:
    create_or_update_private_dns_record(service, ip_servidor)

print("\n✅ Todos os registros Private DNS foram criados ou atualizados com sucesso!")
