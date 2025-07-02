from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.containerservice.models import (
    ManagedCluster,
    ManagedClusterAgentPoolProfile,
    ContainerServiceNetworkProfile,
    ManagedClusterAADProfile,
    ManagedClusterIdentity
)

# Parâmetros
subscription_id = "sua subscription_id"
resource_group = "rg_teste"
location = "brazilsouth"
aks_name = "arck-teste-hml"
subnet_id = "/subscriptions/sua subscription_id/resourceGroups/rg_teste/providers/Microsoft.Network/virtualNetworks/vnet_teste-hml/subnets/sub_arck_teste"  # Formato: /subscriptions/.../subnets/...
node_vm_size = "Standard_DS2_v2"
dns_name_prefix = "arck-teste-hml-dns"
dns_service_ip = "10.240.6.5"         # Ex: 10.2.0.10
service_cidr = "10.240.6.0/24"                # Ex: 10.2.0.0/16
acr_id = "acrtestehml"                # /subscriptions/.../resourceGroups/.../providers/Microsoft.ContainerRegistry/registries/...

# Inicializa client
credential = DefaultAzureCredential()
aks_client = ContainerServiceClient(credential, subscription_id)

# Define perfil de agente (nó)
agent_pool_profile = ManagedClusterAgentPoolProfile(
    name="nodepool1",
    count=1,
    vm_size=node_vm_size,
    os_type="Linux",
    type="VirtualMachineScaleSets",
    mode="System",
    vnet_subnet_id=subnet_id
)

# Define perfil de rede
network_profile = ContainerServiceNetworkProfile(
    network_plugin="azure",
    dns_service_ip=dns_service_ip,
    service_cidr=service_cidr
)

# Define cluster
cluster = ManagedCluster(
    location=location,
    dns_prefix=dns_name_prefix,
    kubernetes_version="1.31.7",
    agent_pool_profiles=[agent_pool_profile],
    network_profile=network_profile,
    enable_rbac=True,
    identity=ManagedClusterIdentity(type="SystemAssigned"),
    addon_profiles={},  # Você pode adicionar addons aqui se quiser
    enable_pod_security_policy=False,
    aad_profile=None
)

# Criar cluster AKS
print(f"Criando cluster AKS '{aks_name}'...")
poller = aks_client.managed_clusters.begin_create_or_update(
    resource_group_name=resource_group,
    resource_name=aks_name,
    parameters=cluster
)
result = poller.result()
print(f"Cluster AKS '{aks_name}' criado com sucesso.")

# Anexar o ACR ao AKS (requer permissões extras se feito via código)
# Alternativa via Azure CLI: az aks update -n $aks --attach-acr $acr
print(f"Anexando ACR '{acr_id}' ao cluster...")
aks_client.managed_clusters.begin_list_cluster_admin_credentials(resource_group, aks_name)
aks_client.managed_clusters.begin_attach_acr(resource_group, aks_name, acr_id)  # apenas em versões com suporte

print("ACR anexado com sucesso.")
