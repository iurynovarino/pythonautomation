from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient

# Parâmetros
subscription_id = "sua subscription_id"  # Substitua pelo ID da sua assinatura
resource_group = "rg_teste"

# VNet 1
vnet1_name = "vnet_teste-hml"
vnet1_rg = resource_group
vnet1_peer_name = "vnet_teste-hml-to-vnet_globalservice"

# VNet 2
vnet2_name = "vnet_globalservice"
vnet2_rg = "GlobalService"
vnet2_peer_name = "vnet_globalservice-to-vnet_teste-hml"

# Inicializa cliente
credential = DefaultAzureCredential()
network_client = NetworkManagementClient(credential, subscription_id)

# Recupera informações das redes
vnet1 = network_client.virtual_networks.get(vnet1_rg, vnet1_name)
vnet2 = network_client.virtual_networks.get(vnet2_rg, vnet2_name)

# 1. Peering da VNet A para VNet B
print(f"Criando peering de '{vnet1_name}' para '{vnet2_name}'...")
peer1 = network_client.virtual_network_peerings.begin_create_or_update(
    vnet1_rg,
    vnet1_name,
    vnet1_peer_name,
    {
        "remote_virtual_network": {
            "id": vnet2.id
        },
        "allow_virtual_network_access": True,
        "allow_forwarded_traffic": False,
        "allow_gateway_transit": False,
        "use_remote_gateways": False
    }
).result()
print("Peering A → B criado.")

# 2. Peering da VNet B para VNet A
print(f"Criando peering de '{vnet2_name}' para '{vnet1_name}'...")
peer2 = network_client.virtual_network_peerings.begin_create_or_update(
    vnet2_rg,
    vnet2_name,
    vnet2_peer_name,
    {
        "remote_virtual_network": {
            "id": vnet1.id
        },
        "allow_virtual_network_access": True,
        "allow_forwarded_traffic": False,
        "allow_gateway_transit": False,
        "use_remote_gateways": False
    }
).result()
print("Peering B → A criado.")
