from azure.identity import DefaultAzureCredential
from azure.mgmt.cdn import CdnManagementClient
from azure.mgmt.cdn.models import (
    Profile,
    Sku,
    AFDEndpoint,
    AFDOriginGroup,
    AFDOrigin,
)

# Configurações
subscription_id = 'aff87ef7-615a-4815-99d9-c8673c2dfc22'
resource_group = 'rg_teste'
location = 'global'  # Front Door é sempre 'global'
profile_name = 'vestigio-teste'
endpoint_name = 'vestigio-endpoint'
origin_group_name = 'originGroup1'
origin_name = 'originStorage'
storage_account_hostname = 'custodiatestehml.blob.core.windows.net'

# Autenticação
credential = DefaultAzureCredential()
client = CdnManagementClient(credential, subscription_id)

# Criar Profile do Azure Front Door
client.profiles.begin_create(
    resource_group_name=resource_group,
    profile_name=profile_name,
    profile=Profile(
        location=location,
        sku=Sku(name='Standard_AzureFrontDoor')
    )
).result()

# Criar Origin Group para o Front Door
client.afd_origin_groups.begin_create(
    resource_group_name=resource_group,
    profile_name=profile_name,
    origin_group_name=origin_group_name,
    origin_group=AFDOriginGroup(
        location=location,
        load_balancing_settings={"sample_size": 4, "successful_samples_required": 2},
        health_probe_settings={
            "probe_interval_in_seconds": 120,
            "probe_path": "/",
            "probe_protocol": "Https",
            "probe_request_type": "GET"
        }
    )
).result()

# Criar Origin (apontando para o Storage Account)
client.afd_origins.begin_create(
    resource_group_name=resource_group,
    profile_name=profile_name,
    origin_group_name=origin_group_name,
    origin_name=origin_name,
    origin=AFDOrigin(
        host_name=storage_account_hostname,
        origin_host_header=storage_account_hostname,
        https_port=443,
        location=location,
        enabled_state="Enabled"
    )
).result()

# Criar Endpoint para o Front Door
client.afd_endpoints.begin_create(
    resource_group_name=resource_group,
    profile_name=profile_name,
    endpoint_name=endpoint_name,
    endpoint=AFDEndpoint(
        location=location,
        enabled_state="Enabled"
    )
).result()

print("Front Door Standard configurado com sucesso com origem apontando para o Storage Account!")
