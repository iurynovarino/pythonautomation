from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import Factory

# Configurações
subscription_id = "aff87ef7-615a-4815-99d9-c8673c2dfc22"
resource_group = "rg_teste"
location = "brazilsouth"
datafactory_name = "archon-dt-teste-hml"

# Autenticação
credential = DefaultAzureCredential()
client = DataFactoryManagementClient(credential, subscription_id)

# Criação do Data Factory
print(f"Criando Azure Data Factory '{datafactory_name}' em '{location}'...")

factory = client.factories.create_or_update(
    resource_group_name=resource_group,
    factory_name=datafactory_name,
    factory=Factory(location=location)
)

print(f"Data Factory '{factory.name}' criado com sucesso!")
