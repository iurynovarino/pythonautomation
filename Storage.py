from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobServiceClient, PublicAccess

# Variáveis
subscription_id = "sua_subscription_id"  # Substitua pelo ID da sua assinatura
resource_group = "rg_teste"
location = "brazilsouth"
storage_account_name = "stacctestehml".lower()  # precisa estar em minúsculo

# Inicializa credenciais
credential = DefaultAzureCredential()
storage_client = StorageManagementClient(credential, subscription_id)

# 1. Criar a conta de armazenamento
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

# 2. Obter a chave da conta de armazenamento
keys = storage_client.storage_accounts.list_keys(resource_group, storage_account_name)
account_key = keys.keys[0].value

# 3. Conectar ao serviço Blob
blob_service_client = BlobServiceClient(
    f"https://{storage_account_name}.blob.core.windows.net",
    credential=account_key
)

# 4. Containers a serem criados (crie conforme a sua necessidade)
containers = {
    "auditoria": "container",
    "templates": "container",
    "apps": "blob",
    "images": "blob",
    "tutorial": "container",
}

# 5. Criar os containers
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
