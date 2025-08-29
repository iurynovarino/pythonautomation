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

# Autentication
credential = DefaultAzureCredential()

# Basic information
subscription_id = "<id da subscription>"  # change for your subscription ID
resource_group_name = "<grupo de recursos>"  # change for your resource group name
application_gateway_name = "<aplication gateway>"  # change for your app gateway name

# Service list
services = [
    {
        "backend_pool_name": "pool_audit_service_hml",
        "backend_http_settings_name": "bp_audit_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "audit-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_audit_service_hml",
        "listener_http_name": "lst_audit_service_hml_redirect",
        "rule_https_name": "rr_audit_service_hml",
        "rule_http_redirect_name": "rr_audit_service_hml_redirect",
        "probe_name": "pb_audit_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_catalog_service_hml",
        "backend_http_settings_name": "bp_catalog_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "catalog-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_catalog_service_hml",
        "listener_http_name": "lst_catalog_service_hml_redirect",
        "rule_https_name": "rr_catalog_service_hml",
        "rule_http_redirect_name": "rr_catalog_service_hml_redirect",
        "probe_name": "pb_catalog_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_communication_service_hml",
        "backend_http_settings_name": "bp_communication_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "communication-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_communication_service_hml",
        "listener_http_name": "lst_communication_service_hml_redirect",
        "rule_https_name": "rr_communication_service_hml",
        "rule_http_redirect_name": "rr_communication_service_hml_redirect",
        "probe_name": "pb_communication_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_datadoc_service_hml",
        "backend_http_settings_name": "bp_datadoc_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "datadoc-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_datadoc_service_hml",
        "listener_http_name": "lst_datadoc_service_hml_redirect",
        "rule_https_name": "rr_datadoc_service_hml",
        "rule_http_redirect_name": "rr_datadoc_service_hml_redirect",
        "probe_name": "pb_datadoc_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_device_service_hml",
        "backend_http_settings_name": "bp_device_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "device-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_device_service_hml",
        "listener_http_name": "lst_device_service_hml_redirect",
        "rule_https_name": "rr_device_service_hml",
        "rule_http_redirect_name": "rr_device_service_hml_redirect",
        "probe_name": "pb_device_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_evidence_service_hml",
        "backend_http_settings_name": "bp_evidence_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "evidence-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_evidence_service_hml",
        "listener_http_name": "lst_evidence_service_hml_redirect",
        "rule_https_name": "rr_evidence_service_hml",
        "rule_http_redirect_name": "rr_evidence_service_hml_redirect",
        "probe_name": "pb_evidence_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_hash_service_hml",
        "backend_http_settings_name": "bp_hash_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "hash-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_hash_service_hml",
        "listener_http_name": "lst_hash_service_hml_redirect",
        "rule_https_name": "rr_hash_service_hml",
        "rule_http_redirect_name": "rr_hash_service_hml_redirect",
        "probe_name": "pb_hash_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_hybridboard_service_hml",
        "backend_http_settings_name": "bp_hybridboard_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "hybridboard-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_hybridboard_service_hml",
        "listener_http_name": "lst_hybridboard_service_hml_redirect",
        "rule_https_name": "rr_hybridboard_service_hml",
        "rule_http_redirect_name": "rr_hybridboard_service_hml_redirect",
        "probe_name": "pb_hybridboard_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_icat_service_hml",
        "backend_http_settings_name": "bp_icat_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "icat-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_icat_service_hml",
        "listener_http_name": "lst_icat_service_hml_redirect",
        "rule_https_name": "rr_icat_service_hml",
        "rule_http_redirect_name": "rr_icat_service_hml_redirect",
        "probe_name": "pb_icat_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_inquiry_service_hml",
        "backend_http_settings_name": "bp_inquiry_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "inquiry-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_inquiry_service_hml",
        "listener_http_name": "lst_inquiry_service_hml_redirect",
        "rule_https_name": "rr_inquiry_service_hml",
        "rule_http_redirect_name": "rr_inquiry_service_hml_redirect",
        "probe_name": "pb_inquiry_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_interfacerecognition_service_hml",
        "backend_http_settings_name": "bp_interfacerecognition_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "interfacerecognition-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_interfacerecognition_service_hml",
        "listener_http_name": "lst_interfacerecognition_service_hml_redirect",
        "rule_https_name": "rr_interfacerecognition_service_hml",
        "rule_http_redirect_name": "rr_interfacerecognition_service_hml_redirect",
        "probe_name": "pb_interfacerecognition_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_maps_service_hml",
        "backend_http_settings_name": "bp_maps_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "maps-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_maps_service_hml",
        "listener_http_name": "lst_maps_service_hml_redirect",
        "rule_https_name": "rr_maps_service_hml",
        "rule_http_redirect_name": "rr_maps_service_hml_redirect",
        "probe_name": "pb_maps_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_media_service_hml",
        "backend_http_settings_name": "bp__media_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "media-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_media_service_hml",
        "listener_http_name": "lst_media_service_hml_redirect",
        "rule_https_name": "rr_media_service_hml",
        "rule_http_redirect_name": "rr_media_service_hml_redirect",
        "probe_name": "pb_media_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_metadado_service_hml",
        "backend_http_settings_name": "bp_metadado_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "metadado-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_metadado_service_hml",
        "listener_http_name": "lst_metadado_service_hml_redirect",
        "rule_https_name": "rr_metadado_service_hml",
        "rule_http_redirect_name": "rr_metadado_service_hml_redirect",
        "probe_name": "pb_metadado_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_monitoring_service_hml",
        "backend_http_settings_name": "bp_monitoring_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "monitoring-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_monitoring_service_hml",
        "listener_http_name": "lst_monitoring_service_hml_redirect",
        "rule_https_name": "rr_monitoring_service_hml",
        "rule_http_redirect_name": "rr_monitoring_service_hml_redirect",
        "probe_name": "pb_monitoring_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_report_service_hml",
        "backend_http_settings_name": "bp_report_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "report-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_report_service_hml",
        "listener_http_name": "lst_report_service_hml_redirect",
        "rule_https_name": "rr_report_service_hml",
        "rule_http_redirect_name": "rr_report_service_hml_redirect",
        "probe_name": "pb_report_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_security_service_hml",
        "backend_http_settings_name": "bp_security_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "security-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_security_service_hml",
        "listener_http_name": "lst_security_service_hml_redirect",
        "rule_https_name": "rr_security_service_hml",
        "rule_http_redirect_name": "rr_security_service_hml_redirect",
        "probe_name": "pb_security_service_hml",
        "probe_path": "/swagger/index.html"
    },
    {
        "backend_pool_name": "pool_user_service_hml",
        "backend_http_settings_name": "bp_user_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "user-service-homolog.custodia.seg.br",
        "listener_https_name": "lst_user_service_hml",
        "listener_http_name": "lst_user_service_hml_redirect",
        "rule_https_name": "rr_user_service_hml",
        "rule_http_redirect_name": "rr_user_service_hml_redirect",
        "probe_name": "pb_user_service_hml",
        "probe_path": "/swagger/index.html"
    },

    {
        "backend_pool_name": "pool_verso_service_hml",
        "backend_http_settings_name": "bp_verso_service_hml",
        "backend_server_ip": "10.21.0.120",
        "hostname": "service-homolog.custodia.seg.br",
        "listener_https_name": "lst_verso_service_hml",
        "listener_http_name": "lst_verso_service_hml_redirect",
        "rule_https_name": "rr_verso_service_hml",
        "rule_http_redirect_name": "rr_verso_service_hml_redirect",
        "probe_name": "pb_verso_service_hml",
        "probe_path": "/swagger/index.html"
    },
    # Adicione mais serviços conforme necessário
]

# fixed configurations
frontend_ip_config_name = "appGatewayFrontendPub"
ssl_certificate_name = "custodia-cert"
frontend_port_443_name = "port-443"
frontend_port_80_name = "port-80"

# start the client
network_client = NetworkManagementClient(credential, subscription_id)

# To find the main Application Gateway
print("Buscando Application Gateway...")
app_gateway = network_client.application_gateways.get(resource_group_name, application_gateway_name)

# Utilitarian functions
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

# Veriry if frontend port to 443 port already exists
existing_port_443 = next((fp for fp in app_gateway.frontend_ports if fp.port == 443), None)
if existing_port_443:
    frontend_port_443_name = existing_port_443.name
    print(f"Reutilizando Frontend Port existente para 443: {frontend_port_443_name}")
else:
    print(f"❗ Não encontrou Frontend Port para 443. Abortando para evitar erro.")
    exit(1)

# Veriry if frontend port to 80 port already exists
existing_port_80 = next((fp for fp in app_gateway.frontend_ports if fp.port == 80), None)
if existing_port_80:
    frontend_port_80_name = existing_port_80.name
    print(f"Reutilizando Frontend Port existente para 80: {frontend_port_80_name}")
else:
    print(f"❗ Não encontrou Frontend Port para 80. Abortando para evitar erro.")
    exit(1)

# ------------------
# Services processing
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
# Application Gateway update
# ------------------
print("\n🚀 Atualizando o Application Gateway...")
poller = network_client.application_gateways.begin_create_or_update(
    resource_group_name,
    application_gateway_name,
    app_gateway
)
result = poller.result()

print("\n✅ Atualização do Application Gateway concluída com sucesso!")
