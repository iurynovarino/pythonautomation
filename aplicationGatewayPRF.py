from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import (
    ApplicationGatewayFrontendPort,
    ApplicationGatewayBackendAddressPool,
    ApplicationGatewayBackendHttpSettings,
    ApplicationGatewayHttpListener,
    ApplicationGatewayRequestRoutingRule,
    ApplicationGatewayProbe,
    ApplicationGatewayProbeHealthResponseMatch,
    ApplicationGatewayRedirectConfiguration
)

# Autenticação
credential = DefaultAzureCredential()

# Informações básicas
subscription_id = "aff87ef7-615a-4815-99d9-c8673c2dfc22"
resource_group_name = "GlobalService"
application_gateway_name = "custodia_agw_globalservice"

# Lista dos serviços que você quer adicionar
services = [
    {
        "backend_pool_name": "pool_prf_hml",
        "backend_http_settings_name": "bp_prf_hml",
        "backend_server_ip": "10.22.64.206",
        "hostname": "prf-hml.custodia.seg.br",
        "listener_https_name": "lst_prf_hml",
        "listener_http_name": "lst_prf_hml_redirect",
        "rule_https_name": "rr_prf_hml",
        "rule_http_redirect_name": "rr_prf_hml_redirect",
        "probe_name": "pb_prf_hml",
        "probe_path": "/"
    }
#Adicione mais serviços conforme necessário
]

# Configurações fixas
frontend_ip_config_name = "appGatewayFrontendPub"
ssl_certificate_name = "custodia-cert"
frontend_port_443_name = "port-443"
frontend_port_80_name = "port-80"

# Inicializar o client
network_client = NetworkManagementClient(credential, subscription_id)

# Buscar o Application Gateway atual
print("Buscando Application Gateway...")
app_gateway = network_client.application_gateways.get(resource_group_name, application_gateway_name)

# Funções utilitárias
def exists(collection, name):
    return any(item.name == name for item in collection)

def get_existing_priorities(app_gateway):
    return [rule.priority for rule in app_gateway.request_routing_rules if rule.priority is not None]

def get_next_available_priority(existing_priorities, start=100, step=10):
    priority = start
    while priority in existing_priorities:
        priority += step
    return priority

# ------------------
# Frontend Ports
# ------------------
print("Configurando Frontend Ports se necessário...")

# Buscar se já existe um frontend port para a porta 443
existing_port_443 = next((fp for fp in app_gateway.frontend_ports if fp.port == 443), None)
if existing_port_443:
    frontend_port_443_name = existing_port_443.name
    print(f"Reutilizando Frontend Port existente para 443: {frontend_port_443_name}")
else:
    print(f"❗ Não encontrou Frontend Port para 443. Abortando para evitar erro.")
    exit(1)

# Buscar se já existe um frontend port para a porta 80
existing_port_80 = next((fp for fp in app_gateway.frontend_ports if fp.port == 80), None)
if existing_port_80:
    frontend_port_80_name = existing_port_80.name
    print(f"Reutilizando Frontend Port existente para 80: {frontend_port_80_name}")
else:
    print(f"❗ Não encontrou Frontend Port para 80. Abortando para evitar erro.")
    exit(1)

# ------------------
# Processar Serviços
# ------------------
for service in services:
    print(f"\n🔵 Processando serviço: {service['hostname']}")

    backend_pool_name = service["backend_pool_name"]
    backend_http_settings_name = service["backend_http_settings_name"]
    backend_server_ip = service["backend_server_ip"]
    hostname = service["hostname"]
    listener_https_name = service["listener_https_name"]
    listener_http_name = service["listener_http_name"]
    rule_https_name = service["rule_https_name"]
    rule_http_redirect_name = service["rule_http_redirect_name"]
    probe_name = service["probe_name"]
    probe_path = service["probe_path"]

    # ------------------
    # Backend Address Pool
    # ------------------
    print("Adicionando Backend Address Pool...")
    if not exists(app_gateway.backend_address_pools, backend_pool_name):
        app_gateway.backend_address_pools.append(ApplicationGatewayBackendAddressPool(
            name=backend_pool_name,
            backend_addresses=[{"ip_address": backend_server_ip}]
        ))
    else:
        print(f"Backend Address Pool '{backend_pool_name}' já existe. Pulando...")

    # ------------------
    # Backend HTTP Settings
    # ------------------
    print("Adicionando Backend HTTP Settings...")
    if not exists(app_gateway.backend_http_settings_collection, backend_http_settings_name):
        app_gateway.backend_http_settings_collection.append(ApplicationGatewayBackendHttpSettings(
            name=backend_http_settings_name,
            port=80,
            protocol="Http",
            cookie_based_affinity="Disabled",
            pick_host_name_from_backend_address=False,
            probe={"id": f"{app_gateway.id}/probes/{probe_name}"},
        ))
    else:
        print(f"Backend HTTP Settings '{backend_http_settings_name}' já existe. Pulando...")

    # ------------------
    # HTTP Listeners
    # ------------------
    print("Adicionando HTTP e HTTPS Listeners...")
    if not exists(app_gateway.http_listeners, listener_https_name):
        app_gateway.http_listeners.append(ApplicationGatewayHttpListener(
            name=listener_https_name,
            frontend_ip_configuration={"id": f"{app_gateway.id}/frontendIPConfigurations/{frontend_ip_config_name}"},
            frontend_port={"id": f"{app_gateway.id}/frontendPorts/{frontend_port_443_name}"},
            protocol="Https",
            ssl_certificate={"id": f"{app_gateway.id}/sslCertificates/{ssl_certificate_name}"},
            host_name=hostname
        ))
    else:
        print(f"HTTPS Listener '{listener_https_name}' já existe. Pulando...")

    if not exists(app_gateway.http_listeners, listener_http_name):
        app_gateway.http_listeners.append(ApplicationGatewayHttpListener(
            name=listener_http_name,
            frontend_ip_configuration={"id": f"{app_gateway.id}/frontendIPConfigurations/{frontend_ip_config_name}"},
            frontend_port={"id": f"{app_gateway.id}/frontendPorts/{frontend_port_80_name}"},
            protocol="Http",
            host_name=hostname
        ))
    else:
        print(f"HTTP Listener '{listener_http_name}' já existe. Pulando...")

    # ------------------
    # Health Probe
    # ------------------
    print("Adicionando Health Probe...")
    if not exists(app_gateway.probes, probe_name):
        new_probe = ApplicationGatewayProbe(
            name=probe_name,
            protocol="Http",
            host=hostname,
            path=probe_path,
            interval=30,
            timeout=30,
            unhealthy_threshold=3,
            pick_host_name_from_backend_http_settings=False,
            min_servers=0,
            match=ApplicationGatewayProbeHealthResponseMatch(
                body=None,
                status_codes=["200-399"]
            )
        )
        app_gateway.probes.append(new_probe)
    else:
        print(f"Health Probe '{probe_name}' já existe. Pulando...")

    # ------------------
    # Request Routing Rules
    # ------------------
    print("Adicionando Request Routing Rules...")

    existing_priorities = get_existing_priorities(app_gateway)
    new_priority_https = get_next_available_priority(existing_priorities)
    existing_priorities.append(new_priority_https)

    if not exists(app_gateway.request_routing_rules, rule_https_name):
        app_gateway.request_routing_rules.append(ApplicationGatewayRequestRoutingRule(
            name=rule_https_name,
            rule_type="Basic",
            http_listener={"id": f"{app_gateway.id}/httpListeners/{listener_https_name}"},
            backend_address_pool={"id": f"{app_gateway.id}/backendAddressPools/{backend_pool_name}"},
            backend_http_settings={"id": f"{app_gateway.id}/backendHttpSettingsCollection/{backend_http_settings_name}"},
            priority=new_priority_https
        ))
    else:
        print(f"Request Routing Rule '{rule_https_name}' já existe. Pulando...")

    # Configurar Redirect (HTTP -> HTTPS)
    redirect_configuration_name = "redirectConfigurationHttpToHttps"
    if not hasattr(app_gateway, 'redirect_configurations') or app_gateway.redirect_configurations is None:
        app_gateway.redirect_configurations = []

    if not exists(app_gateway.redirect_configurations, redirect_configuration_name):
        app_gateway.redirect_configurations.append(ApplicationGatewayRedirectConfiguration(
            name=redirect_configuration_name,
            redirect_type="Permanent",
            target_listener={"id": f"{app_gateway.id}/httpListeners/{listener_https_name}"},
            include_path=True,
            include_query_string=True
        ))

    new_priority_redirect = get_next_available_priority(existing_priorities)
    if not exists(app_gateway.request_routing_rules, rule_http_redirect_name):
        app_gateway.request_routing_rules.append(ApplicationGatewayRequestRoutingRule(
            name=rule_http_redirect_name,
            rule_type="Basic",
            http_listener={"id": f"{app_gateway.id}/httpListeners/{listener_http_name}"},
            redirect_configuration={"id": f"{app_gateway.id}/redirectConfigurations/{redirect_configuration_name}"},
            priority=new_priority_redirect
        ))
    else:
        print(f"Request Routing Rule '{rule_http_redirect_name}' já existe. Pulando...")

# ------------------
# Atualizar o Application Gateway
# ------------------
print("\n🚀 Atualizando o Application Gateway...")
poller = network_client.application_gateways.begin_create_or_update(
    resource_group_name,
    application_gateway_name,
    app_gateway
)
result = poller.result()

print("\n✅ Atualização do Application Gateway concluída com sucesso!")
