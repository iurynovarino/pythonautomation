from azure.mgmt.network.models import (
    ApplicationGateway,
    ApplicationGatewaySku,
    ApplicationGatewayFrontendIPConfiguration,
    ApplicationGatewayFrontendPort,
    ApplicationGatewayBackendAddressPool,
    ApplicationGatewayBackendHttpSettings,
    ApplicationGatewayHttpListener,
    ApplicationGatewayRequestRoutingRule,
    SubResource,
    ApplicationGatewayIPConfiguration,
    ApplicationGatewayFrontendIPConfiguration,
    ApplicationGatewayGatewayIPConfiguration,
    ApplicationGatewayProtocol
)

# Defina os objetos básicos antes
subnet_id = "<YOUR_SUBNET_ID>" # Replace with your Subnet ID
public_ip_id = "pip_hml_agwfront"

app_gateway_params = ApplicationGateway(
    location="brazilsouth",
    sku=ApplicationGatewaySku(
        name="Standard_v2",
        tier="Standard_v2",
        capacity=1
    ),
    gateway_ip_configurations=[
        ApplicationGatewayIPConfiguration(
            name="appGwIpConfig",
            subnet=SubResource(id=subnet_id)
        )
    ],
    frontend_ip_configurations=[
        ApplicationGatewayFrontendIPConfiguration(
            name="appGwFrontendIP",
            public_ip_address=SubResource(id=public_ip_id)
        )
    ],
    frontend_ports=[
        ApplicationGatewayFrontendPort(
            name="appGwFrontendPort",
            port=80
        )
    ],
    backend_address_pools=[
        ApplicationGatewayBackendAddressPool(
            name="appGwBackendPool",
            backend_addresses=[]
        )
    ],
    backend_http_settings_collection=[
        ApplicationGatewayBackendHttpSettings(
            name="appGwBackendHttpSettings",
            port=80,
            protocol=ApplicationGatewayProtocol.http,
            cookie_based_affinity="Disabled"
        )
    ],
    http_listeners=[
        ApplicationGatewayHttpListener(
            name="appGwHttpListener",
            frontend_ip_configuration=SubResource(id="pip_hml_agwfront"),
            frontend_port=SubResource(id="pip_hml_agwfront"),
            protocol=ApplicationGatewayProtocol.http
        )
    ],
    request_routing_rules=[
        ApplicationGatewayRequestRoutingRule(
            name="rule1",
            rule_type="Basic",
            http_listener=SubResource(id="<id-do-listener>"),
            backend_address_pool=SubResource(id="<id-do-pool>"),
            backend_http_settings=SubResource(id="<id-do-http-settings>"),
            priority=100
        )
    ]
)

# Criar
poller = network_client.application_gateways.begin_create_or_update(
    "rg_teste",
    "agw_hml_front",
    app_gateway_params
)
result = poller.result()
