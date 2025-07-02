from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import os

# Parâmetros
subscription_id = "sua subscription_id"  # Substitua aqui
resource_group = "rg_teste"
location = "brazilsouth"
vnet_name = "vnet_teste-hml"
subnet_name = "sub_arck_teste"

# Inicializa a credencial e o client
credential = DefaultAzureCredential()
network_client = NetworkManagementClient(credential, subscription_id)

# Define configuração da VNet
vnet_params = {
    "location": location,
    "address_space": {
        "address_prefixes": ["10.24.0.0/16"]
    }
}

# Cria a VNet
print(f"Criando VNet '{vnet_name}'...")
async_vnet_creation = network_client.virtual_networks.begin_create_or_update(
    resource_group,
    vnet_name,
    vnet_params
)
vnet_result = async_vnet_creation.result()
print(f"VNet '{vnet_result.name}' criada com sucesso!")

# Define configuração da Subnet
subnet_params = {
    "address_prefix": "10.24.0.0/18"
}

# Cria a Subnet
print(f"Criando Subnet '{subnet_name}'...")
async_subnet_creation = network_client.subnets.begin_create_or_update(
    resource_group,
    vnet_name,
    subnet_name,
    subnet_params
)
subnet_result = async_subnet_creation.result()
print(f"Subnet '{subnet_result.name}' criada com sucesso dentro da VNet '{vnet_name}'")
