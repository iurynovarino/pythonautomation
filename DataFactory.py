from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import Factory

# settings
subscription_id = "<subscription_id>"  # Change to your subscription ID
resource_group = "<resource_group>"  # Change to your resource group name
location = "<location>"  # Change to your desired location, e.g., "brazilsouth"
datafactory_name = "<your_datafactory_name>"  # Change to your desired Data Factory name

# Autentication
credential = DefaultAzureCredential()
client = DataFactoryManagementClient(credential, subscription_id)

# Create Data Factory
print(f"Criando Azure Data Factory '{datafactory_name}' em '{location}'...")

factory = client.factories.create_or_update(
    resource_group_name=resource_group,
    factory_name=datafactory_name,
    factory=Factory(location=location)
)

print(f"Data Factory '{factory.name}' criado com sucesso!")
