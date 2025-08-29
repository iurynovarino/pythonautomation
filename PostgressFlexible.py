from azure.identity import DefaultAzureCredential
from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSQLManagementClient
from azure.mgmt.rdbms.postgresql_flexibleservers.models import Server, Sku, Storage, ServerVersion

# Parameters
subscription_id = "<YOUR_SUBSCRIPTION_ID>" # change to your subscription ID
resource_group = "<YOUR_RESOURCE_GROUP>"  # change to your resource group name
server_name = "<YOUR_SERVER_NAME>" # change to your desired server name
location = "<YOUR_LOCATION>"  # change to your desired location, e.g., "brazilsouth"

# Autentication and client setup
credential = DefaultAzureCredential()
client = PostgreSQLManagementClient(credential, subscription_id)

# Creating server
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
