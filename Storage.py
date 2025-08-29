from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobServiceClient, PublicAccess

# Variables declaration
subscription_id = "<YOUR_SUBSCRIPTION_ID>"  # Change to your subscription ID
resource_group = "<YOUR_RESOURCE_GROUP>"  # Change to your resource group name
location = "<YOUR_LOCATION>"  # Change to your desired location, e.g., "brazilsouth"
storage_account_name = "<YOUR_STORAGE_ACCOUNT_NAME>".lower() # Change to your desired storage account name (must be lowercase and unique)

# start credencials
credential = DefaultAzureCredential()
storage_client = StorageManagementClient(credential, subscription_id)

# 1. Create a storage account
print(f"Criando conta de armazenamento '{storage_account_name}'...")
storage_async = storage_client.storage_accounts.begin_create(
    resource_group_name=resource_group,
    account_name=storage_account_name,
    parameters={
        "location": location,
        "sku": {"name": "Standard_LRS"},
        "kind": "StorageV2",
        "access_tier": "Cool",
        "allow_blob_public_access": True,
        "public_network_access": "Enabled"
    }
)
storage_async.result()
print(f"Conta de armazenamento '{storage_account_name}' criada com sucesso.")

# 2. Obtain the storage accouunt key
keys = storage_client.storage_accounts.list_keys(resource_group, storage_account_name)
account_key = keys.keys[0].value

# 3. Storage account conect
blob_service_client = BlobServiceClient(
    f"https://{storage_account_name}.blob.core.windows.net",
    credential=account_key
)

# 4. Create containers (make as you wish)
containers = {
    "auditoria": "container",
    "templates": "container",
    "apps": "blob",
    "images": "blob",
    "tutorial": "container",
}

# 5. Loping to create various containers
for name, access in containers.items():
    try:
        print(f"Criando container '{name}' com acesso '{access}'...")
        blob_service_client.create_container(
            name,
            public_access=PublicAccess.Container if access == "container" else PublicAccess.Blob
        )
    except Exception as e:
        print(f"Erro ao criar container '{name}': {e}")

print("Todos os containers foram processados.")
