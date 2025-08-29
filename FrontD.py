from azure.identity import DefaultAzureCredential
from azure.mgmt.cdn import CdnManagementClient
from azure.mgmt.cdn.models import (
    Profile,
    Sku,
    AFDEndpoint,
    AFDOriginGroup,
    AFDOrigin,
)

# Settings
subscription_id = '<subscription_id>'  # Change to your subscription ID
resource_group = '<resource_group>'  # Change to your resource group name
location = 'global'  # Front Door is always 'global'
profile_name = '<your_front_door_profile>'  # Change to your desired Front Door profile name
endpoint_name = '<your_front_door_endpoint>'  # Change to your desired Front Door endpoint name
origin_group_name = '<your_origin_group>'  # Change to your desired Origin Group name
origin_name = '<your_origin>'  # Change to your desired Origin name
storage_account_hostname = '<storage_account_name>.blob.core.windows.net'

# Autentication
credential = DefaultAzureCredential()
client = CdnManagementClient(credential, subscription_id)

# Create Profile do Azure Front Door
client.profiles.begin_create(
    resource_group_name=resource_group,
    profile_name=profile_name,
    profile=Profile(
        location=location,
        sku=Sku(name='Standard_AzureFrontDoor')
    )
).result()

# Criate Origin Group to Front Door
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

# Create Origin (ponting to the Storage Account)
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

# Create Endpoint to the Front Door
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
