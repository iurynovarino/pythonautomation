# 🚀 Infraestrutura como Código (IaC) com Python para Azure

Bem-vindo a este repositório de automação! Aqui você encontrará uma poderosa coleção de scripts Python que utilizam o SDK da Azure para provisionar uma infraestrutura de nuvem completa e robusta.

Esqueça os cliques manuais no portal! Com estes scripts, você pode implantar, replicar e gerenciar sua arquitetura de forma **programática, consistente e veloz**.

---

## 🌟 O que este projeto faz?

Este projeto automatiza a criação de um ambiente de homologação (`hml`) complexo na Azure, ideal para aplicações modernas baseadas em microsserviços. Ele provisiona e configura os seguintes recursos:

### 🌐 **Core de Rede e Segurança**
- **Grupos de Recursos**: Isola o ambiente de forma organizada.
- **Redes Virtuais (VNet) e Subnets**: Cria a espinha dorsal da rede para os serviços.
- **VNet Peering**: Conecta a VNet da aplicação com uma VNet de serviços globais.
- **Zonas de DNS (Públicas e Privadas)**: Gerencia a resolução de nomes para os serviços, tanto para acesso externo quanto interno.

### 📦 **Containers e Orquestração**
- **Azure Container Registry (ACR)**: Um registro privado para armazenar e gerenciar as imagens de container.
- **Azure Kubernetes Service (AKS)**: Um cluster Kubernetes gerenciado, configurado para rodar em uma subnet específica e integrado ao ACR.

### 🚚 **Entrega e Roteamento de Aplicações**
- **Application Gateway (AGW)**: Configuração avançada e detalhada para dezenas de serviços, incluindo:
  - Backend Pools apontando para os IPs dos serviços.
  - Health Probes customizadas para monitorar a saúde das aplicações.
  - Listeners HTTPS na porta 443 com certificado SSL.
  - Listeners HTTP na porta 80 com redirecionamento automático para HTTPS.
  - Regras de roteamento para direcionar o tráfego para os backends corretos.
- **Azure Front Door**: Configura um ponto de entrada global para aplicações web, apontando para um Storage Account.

### 🗄️ **Armazenamento e Banco de Dados**
- **Storage Accounts**: Cria contas de armazenamento para diversos fins (blobs, arquivos, etc.).
- **Blob Containers**: Provisiona múltiplos containers com diferentes níveis de acesso público (`blob` ou `container`).
- **PostgreSQL Flexible Server**: Um banco de dados como serviço, gerenciado e escalável.

### 🔄 **Integração e Mensageria**
- **Azure Service Bus**: Namespace com múltiplos tópicos e subscrições para comunicação assíncrona e arquiteturas orientadas a eventos.
- **Azure Data Factory**: Orquestração de pipelines de dados.

---

## 🛠️ Pré-requisitos

Antes de começar, garanta que você tenha:

1.  **Python 3.8+** instalado.
2.  **Azure CLI** instalado e configurado.
3.  Uma **assinatura ativa na Azure** com as permissões necessárias para criar os recursos listados.

---

## 🚀 Como usar

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_DIRETORIO>
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Autentique-se na Azure:**
    ```bash
    az login
    ```
    Os scripts usarão suas credenciais do CLI automaticamente.

5.  **Ajuste as variáveis!**
    Antes de executar qualquer script, abra o arquivo e **edite as variáveis** no topo (como `subscription_id`, `resource_group_name`, nomes de recursos, IPs, etc.) para que correspondam às suas necessidades.

6.  **Execute os scripts:**
    Os scripts podem ser executados individualmente. Recomenda-se seguir uma ordem lógica de dependência. Por exemplo:
    ```bash
    python RG.py          # 1. Crie o Grupo de Recursos
    python NET.py         # 2. Crie a VNet e Subnet
    python Storage.py     # 3. Crie o Storage
    python ACR.py         # 4. Crie o ACR
    python Aks.py         # 5. Crie o AKS (depende da VNet e ACR)
    # ... e assim por diante.
    ```

---

## 📜 Visão Geral dos Scripts

| Arquivo | Descrição |
| ----------------------------------- | ------------------------------------------------------------------------------------------------ |
| `RG.py` | Cria o Grupo de Recursos principal. |
| `NET.py` | Provisiona a VNet e a Subnet para o AKS. |
| `Peering.py` | Configura o VNet Peering entre duas redes virtuais. |
| `ACR.py` | Cria o Azure Container Registry. |
| `Storage.py` | Cria a Conta de Armazenamento e seus containers. |
| `PostgressFlexible.py` | Cria o servidor de banco de dados PostgreSQL. |
| `Aks.py` | Provisiona o cluster AKS e o integra com a rede e o ACR. |
| `ServiceBus.py` | Configura o Service Bus, com tópicos e subscrições. |
| `DataFactory.py` | Cria uma instância do Azure Data Factory. |
| `FrontD.py` | Cria uma instância do Azure Front Door. |
| `DnsZones.py` / `DnsZonesPoc.py` | Gerencia registros 'A' em uma Zona de DNS Pública. |
| `PrivateDns.py` | Gerencia registros 'A' em uma Zona de DNS Privada. |
| `aplicationGateway*.py` | Scripts detalhados para configurar o Application Gateway com todas as regras e listeners. |

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* para relatar bugs ou sugerir melhorias. Se quiser adicionar um novo script ou funcionalidade, por favor, abra um *Pull Request*.

