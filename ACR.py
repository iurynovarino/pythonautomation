from azure.identity import DefaultAzureCredential
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.containerregistry.models import Registry, Sku

# Configurações
subscription_id = "sua  subscription_id"  # Substitua pelo ID da sua assinatura
resource_group = "rg_teste"
location = "brazilsouth"
registry_name = "acrtestehml" 

# Autenticação
credential = DefaultAzureCredential()
client = ContainerRegistryManagementClient(credential, subscription_id)

# Criação do ACR
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
