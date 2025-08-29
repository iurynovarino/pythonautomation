from azure.identity import DefaultAzureCredential
from azure.mgmt.servicebus import ServiceBusManagementClient
from azure.mgmt.servicebus.models import (
    SBTopic,
    SBSubscription,
    SBNamespace
)

# Variables declaration
subscription_id = "<YOUR_AZURE_SUBSCRIPTION_ID>"  # Replace with your Azure Subscription ID
resource_group = "<YOUR_RESOURCE_GROUP>"  # Replace with your Resource Group name
location = "<YOUR_AZURE_LOCATION>"  # e.g., "brazilsouth"
namespace_name = "<YOUR_NAMESPACE_NAME>" # Replace with your desired namespace name

# Autentication and client setup
credential = DefaultAzureCredential()
client = ServiceBusManagementClient(credential, subscription_id)

# Create namespace
print(f"Criando namespace '{namespace_name}'...")
client.namespaces.begin_create_or_update(
    resource_group_name=resource_group,
    namespace_name=namespace_name,
    parameters=SBNamespace(location=location, sku={"name": "Standard"})
).result()

# Topic list and subscriptions (adjust as you wish )
topics_with_subs = {
    "security": ["audit", "communication"],
    "download-report": ["main"],
    "import-users": ["main"],
    "log-index": ["main"],
}

# Create topics and subscriptions
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
