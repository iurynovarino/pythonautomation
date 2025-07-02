from azure.identity import DefaultAzureCredential
from azure.mgmt.servicebus import ServiceBusManagementClient
from azure.mgmt.servicebus.models import (
    SBTopic,
    SBSubscription,
    SBNamespace
)

# Variáveis de configuração
subscription_id = "sua_subscription_id"  # Substitua pelo ID da sua assinatura
resource_group = "rg_teste"
location = "brazilsouth"
namespace_name = "sbns-teste-hml" # Nome do namespace do Service Bus

# Autenticação
credential = DefaultAzureCredential()
client = ServiceBusManagementClient(credential, subscription_id)

# Criar namespace
print(f"Criando namespace '{namespace_name}'...")
client.namespaces.begin_create_or_update(
    resource_group_name=resource_group,
    namespace_name=namespace_name,
    parameters=SBNamespace(location=location, sku={"name": "Standard"})
).result()

# Lista de tópicos e subscrições (essa é uma lista fictícia, ajuste conforme necessário)
topics_with_subs = {
    "security": ["audit", "communication"],
    "download-report": ["main"],
    "import-users": ["main"],
    "log-index": ["main"],
}

# Criar tópicos e subscrições
for topic_name, subs in topics_with_subs.items():
    print(f"Criando tópico '{topic_name}'...")
    client.topics.create_or_update(
        resource_group_name=resource_group,
        namespace_name=namespace_name,
        topic_name=topic_name,
        parameters=SBTopic(
            max_size_in_megabytes=1024,
            default_message_time_to_live="PT2M"
        )
    )

    for sub_name in subs:
        print(f"  -> Criando subscrição '{sub_name}' para tópico '{topic_name}'...")
        client.subscriptions.create_or_update(
            resource_group_name=resource_group,
            namespace_name=namespace_name,
            topic_name=topic_name,
            subscription_name=sub_name,
            parameters=SBSubscription(
                max_delivery_count=10,
                default_message_time_to_live="PT2M",
                lock_duration="PT2M",
                dead_letter_on_filter_evaluation_exceptions=False
            )
        )

print("Provisionamento completo.")
