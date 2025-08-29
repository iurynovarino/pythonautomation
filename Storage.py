import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobServiceClient, PublicAccess
from azure.core.exceptions import ResourceExistsError

def create_storage_account(storage_client, resource_group, account_name, location):
    """Creates or updates a storage account."""
    print(f"Criando conta de armazenamento '{account_name}'...")
    try:
        storage_async = storage_client.storage_accounts.begin_create(
            resource_group_name=resource_group,
            account_name=account_name,
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
        print(f"Conta de armazenamento '{account_name}' criada com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao criar conta de armazenamento: {e}")
        raise

def create_containers(blob_service_client, containers_to_create):
    """Creates multiple blob containers with specified public access."""
    for name, access_level_str in containers_to_create.items():
        try:
            print(f"Criando container '{name}' com acesso '{access_level_str}'...")
            public_access = PublicAccess.Container if access_level_str == "container" else PublicAccess.Blob
            blob_service_client.create_container(name, public_access=public_access)
            print(f"  -> Container '{name}' criado.")
        except ResourceExistsError:
            print(f"  -> Container '{name}' já existe. Pulando.")
        except Exception as e:
            print(f"❌ Erro inesperado ao criar container '{name}': {e}")
    print("\nTodos os containers foram processados.")

def main():
    """Main function to orchestrate storage provisioning."""
    load_dotenv()

    # Variables declaration
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP")
    location = os.getenv("AZURE_LOCATION", "brazilsouth")
    storage_account_name = os.getenv("STORAGE_ACCOUNT_NAME").lower()

    credential = DefaultAzureCredential()
    storage_client = StorageManagementClient(credential, subscription_id)

    create_storage_account(storage_client, resource_group, storage_account_name, location)

    blob_service_client = BlobServiceClient(
        account_url=f"https://{storage_account_name}.blob.core.windows.net",
        credential=credential
    )

    containers_to_create = {
        "auditoria": "container", "templates": "container", "apps": "blob",
        "images": "blob", "tutorial": "container",
    }
    create_containers(blob_service_client, containers_to_create)

if __name__ == "__main__":
    main()
