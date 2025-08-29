from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# Variables declaration
subscription_id = "<YOUR_SUBSCRIPTION_ID>"  # Change to your subscription ID
resource_group_name = "<YOUR_RESOURCE_GROUP>"  # Change to your resource group name
location = "<YOUR_LOCATION>"  # Change to your desired location, e.g., "brazilsouth"

# Autenticating using the Azure Cli or Managed Identity
credential = DefaultAzureCredential()

# Start Resource Management client
resource_client = ResourceManagementClient(credential, subscription_id)

# Create or update the resource group
resource_group_params = {"location": location}
result = resource_client.resource_groups.create_or_update(
    resource_group_name, resource_group_params
)

# Show result
print(f"Grupo de recurso '{result.name}' criado com sucesso em '{result.location}'")
