from azure.identity import DefaultAzureCredential
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.containerregistry.models import Registry, Sku

# Configurações
subscription_id = "<YOUR_SUBSCRIPTION_ID>"  # Change to your subscription ID
resource_group = "<YOUR_RESOURCE_GROUP>"  # Change to your resource group name
location = "<YOUR_LOCATION>"  # Change to your desired location, e.g., "brazilsouth"
registry_name = "<YOUR_ACR_NAME>"  # Change to your desired ACR name (must be unique)

# Autentication and client setup
credential = DefaultAzureCredential()
client = ContainerRegistryManagementClient(credential, subscription_id)

# Create ACR
print(f"Criando ACR '{registry_name}' em '{location}'...")

acr = client.registries.begin_create(
    resource_group_name=resource_group,
    registry_name=registry_name,
    registry=Registry(
        location=location,
        sku=Sku(name="Standard"),  # Opções: Basic, Standard, Premium
        admin_user_enabled=True
    )
).result()

print(f"ACR '{acr.name}' criado com sucesso!")
