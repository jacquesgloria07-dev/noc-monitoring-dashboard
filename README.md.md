# 📡 NOC | Advanced RAN Monitoring Dashboard

Este projeto é um dashboard interativo desenvolvido em Python para simular o monitoramento avançado de uma Rede de Acesso de Rádio (RAN). A aplicação foi desenhada com foco na rotina operacional de um Network Operations Center (NOC), permitindo o isolamento rápido de falhas e a análise de causa raiz em ambientes de missão crítica.

## 🎯 Objetivo
Transformar dados brutos de rede em inteligência visual acionável. O painel facilita o *troubleshooting* ágil em salas de crise, permitindo que as equipes de engenharia cruzem dimensões de Região, Tecnologia e Vendor para identificar degradações na qualidade do serviço (QoS) e na experiência do usuário (QoE).

## 📊 KPIs Monitorados
O painel monitora os principais indicadores de desempenho da infraestrutura:
*   **Retenção e Mobilidade:** Acompanhamento de *Drop Rate* (taxa de queda) e *Handover Success Rate* (HOSR).
*   **Integridade e Acessibilidade:** Visão em tempo real da disponibilidade das células e sucesso de estabelecimento de conexão (RRC/RAB).
*   **Utilização e Tráfego:** Análise de saturação física através da Utilização de PRB (Physical Resource Block) em Downlink, cruzada com o volume total de tráfego de dados e voz (Erlangs).
*   **Qualidade e QoE:** Monitoramento do *Throughput* de usuário e Latência por tecnologia (3G, 4G, 5G).

## 🛠️ Stack Tecnológico
*   **Linguagem:** Python
*   **Processamento de Dados:** Pandas & NumPy
*   **Visualização Interativa:** Plotly (Express & Graph Objects)
*   **Framework Web:** Streamlit

## 🚀 Como Executar Localmente
Para rodar a aplicação na sua máquina, siga os passos abaixo:

1. Clone este repositório.
2. Instale as dependências executando: `pip install streamlit pandas plotly numpy`
3. Inicie o servidor local com o comando: `streamlit run noc_dashboard.py`

---
*Projeto desenvolvido para demonstração prática da aplicação de Data Science e automação na Engenharia de Telecomunicações.*