from azure.identity import DefaultAzureCredential
from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSQLManagementClient
from azure.mgmt.rdbms.postgresql_flexibleservers.models import Server, Sku, Storage, ServerVersion

# Parâmetros
subscription_id = "sua subscription_id"  # Substitua pelo ID da sua assinatura
resource_group = "rg_teste"
server_name = "teste-hml-db"  # Nome do servidor do banco de dados
location = "brazilsouth"

# Autenticação
credential = DefaultAzureCredential()
client = PostgreSQLManagementClient(credential, subscription_id)

# Criação do servidor
poller = client.servers.begin_create(
    resource_group_name=resource_group,
    server_name=server_name,
    parameters=Server(
        location=location,
        sku=Sku(name="Standard_B1ms", tier="Burstable"),
        administrator_login="adminuser",
        administrator_login_password="SenhaSuperSegura123",
        version="14",
        storage=Storage(storage_size_gb=32)
    )
)

server_result = poller.result()
print(f"Servidor criado: {server_result.name}")
