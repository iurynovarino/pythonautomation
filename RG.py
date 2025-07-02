from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# Parâmetros de entrada
subscription_id = "<sua_subscription_id>"
resource_group_name = "rg_teste"
location = "brazilsouth"

# Autenticação usando o Azure CLI ou Managed Identity
credential = DefaultAzureCredential()

# Inicializa o cliente de Resource Management
resource_client = ResourceManagementClient(credential, subscription_id)

# Cria (ou atualiza) o grupo de recursos
resource_group_params = {"location": location}
result = resource_client.resource_groups.create_or_update(
    resource_group_name, resource_group_params
)

# Exibe o resultado
print(f"Grupo de recurso '{result.name}' criado com sucesso em '{result.location}'")
