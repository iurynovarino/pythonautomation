from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import os

# Variables declaration
subscription_id = "<subscription_id>"  # change to your subscription ID
resource_group = "<resource_group>"  # change to your resource group name
location = "<location>"  # change to your desired location, e.g., "brazilsouth"
vnet_name = "<vnet_name>"  # change to your desired VNet name
subnet_name = "<subnet_name>"  # change to your desired Subnet name

# Start the credential and the client
credential = DefaultAzureCredential()
network_client = NetworkManagementClient(credential, subscription_id)

# setting the vnet configuration
vnet_params = {
    "location": location,
    "address_space": {
        "address_prefixes": ["10.24.0.0/16"]
    }
}

# Creating the VNet
print(f"Criando VNet '{vnet_name}'...")
async_vnet_creation = network_client.virtual_networks.begin_create_or_update(
    resource_group,
    vnet_name,
    vnet_params
)
vnet_result = async_vnet_creation.result()
print(f"VNet '{vnet_result.name}' criada com sucesso!")

# Setting the subnet configuration
subnet_params = {
    "address_prefix": "10.24.0.0/18"
}

# Creating the subnet
print(f"Criando Subnet '{subnet_name}'...")
async_subnet_creation = network_client.subnets.begin_create_or_update(
    resource_group,
    vnet_name,
    subnet_name,
    subnet_params
)
subnet_result = async_subnet_creation.result()
print(f"Subnet '{subnet_result.name}' criada com sucesso dentro da VNet '{vnet_name}'")
