import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Configuração da Página
st.set_page_config(page_title="NOC RAN Dashboard", page_icon="📡", layout="wide")
st.title("📡 NOC | Monitoramento Avançado de RAN")

# 2. Geração de Dados Simulados (Multidimensional)
@st.cache_data
def gerar_dados():
    np.random.seed(42)
    horas = pd.date_range(start="2026-07-10 00:00", periods=24, freq="h")
    tecnologias = ['3G', '4G', '5G']
    vendors = ['Ericsson', 'Huawei', 'Nokia']
    regioes = ['SP', 'RJ', 'MG']

    dados = []
    for hora in horas:
        for tech in tecnologias:
            for vendor in vendors:
                for regiao in regioes:
                    t_mult = 10 if tech == '5G' else (2 if tech == '4G' else 0.5)
                    
                    dados.append({
                        'Horário': hora,
                        'Região': regiao,
                        'Tecnologia': tech,
                        'Vendor': vendor,
                        'Acessibilidade (%)': np.random.uniform(98.5, 99.99),
                        'Drop Rate (%)': np.random.uniform(0.1, 1.2),
                        'Disponibilidade (%)': np.random.uniform(99.0, 100.0),
                        'Handover SR (%)': np.random.uniform(97.0, 99.5),
                        'PRB DL Utilização (%)': np.random.uniform(30.0, 75.0),
                        'Throughput DL (Mbps)': np.random.uniform(10, 30) * t_mult,
                        'Latência (ms)': np.random.uniform(10, 20) / (0.5 if tech == '5G' else (1 if tech == '4G' else 3)),
                        'Tráfego Dados (TB)': np.random.uniform(10, 100) * t_mult,
                        'Tráfego Voz (Erlangs)': np.random.uniform(500, 3000) if tech in ['3G', '4G'] else 0
                    })

    df = pd.DataFrame(dados)

    # INCIDENTE DE CONGESTIONAMENTO (Região SP, 4G, Horário de Pico 19h)
    mask_pico = (df['Horário'] == "2026-07-10 19:00:00") & (df['Tecnologia'] == '4G') & (df['Região'] == 'SP')
    df.loc[mask_pico, 'PRB DL Utilização (%)'] = np.random.uniform(95.0, 99.9, size=mask_pico.sum())
    df.loc[mask_pico, 'Throughput DL (Mbps)'] = np.random.uniform(1.5, 5.0, size=mask_pico.sum())
    df.loc[mask_pico, 'Drop Rate (%)'] = np.random.uniform(3.5, 5.5, size=mask_pico.sum())
    df.loc[mask_pico, 'Handover SR (%)'] = np.random.uniform(85.0, 90.0, size=mask_pico.sum())
    df.loc[mask_pico, 'Latência (ms)'] = np.random.uniform(150.0, 300.0, size=mask_pico.sum())
    
    return df

df = gerar_dados()

# 3. Menu Lateral e Botão de Exportação
st.sidebar.header("Filtros Dinâmicos")
regiao_sel = st.sidebar.multiselect("Região", df['Região'].unique(), default=df['Região'].unique())
tech_sel = st.sidebar.multiselect("Tecnologia", df['Tecnologia'].unique(), default=df['Tecnologia'].unique())
vendor_sel = st.sidebar.multiselect("Vendor", df['Vendor'].unique(), default=df['Vendor'].unique())

df_filtrado = df[(df['Região'].isin(regiao_sel)) & (df['Tecnologia'].isin(tech_sel)) & (df['Vendor'].isin(vendor_sel))]

if df_filtrado.empty:
    st.error("Nenhum dado retornado com os filtros atuais.")
    st.stop()

# --- NOVIDADE: Botão de Exportação de Dados ---
st.sidebar.divider()
st.sidebar.markdown("### Exportação")
csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📥 Baixar Dados (CSV)",
    data=csv,
    file_name='noc_ran_export.csv',
    mime='text/csv',
)

# 4. Agrupamento para KPIs de Topo
df_hora = df_filtrado.groupby('Horário').mean(numeric_only=True).reset_index()
df_hora['Tráfego Dados (TB)'] = df_filtrado.groupby('Horário')['Tráfego Dados (TB)'].sum().values

kpi_atual = df_hora.iloc[-1]
kpi_anterior = df_hora.iloc[-2]

# --- NOVIDADE: Sistema de Alerta Visual (Visual Management) ---
if kpi_atual['Drop Rate (%)'] > 2.0 or kpi_atual['Acessibilidade (%)'] < 95.0:
    st.error("🚨 **ALERTA CRÍTICO:** Degradação severa detectada na rede. SLA violado nos filtros selecionados.")
else:
    st.success("✅ **STATUS NORMAL:** A rede está operando dentro dos parâmetros de estabilidade.")

# 5. Painel de Indicadores (Cards)
st.markdown("### Visão Geral Operacional (Última Hora)")
c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("Acessibilidade", f"{kpi_atual['Acessibilidade (%)']:.2f}%", f"{kpi_atual['Acessibilidade (%)'] - kpi_anterior['Acessibilidade (%)']:.2f}%")
c2.metric("Drop Rate", f"{kpi_atual['Drop Rate (%)']:.2f}%", f"{kpi_atual['Drop Rate (%)'] - kpi_anterior['Drop Rate (%)']:.2f}%", delta_color="inverse")
c3.metric("Disponibilidade", f"{kpi_atual['Disponibilidade (%)']:.2f}%", f"{kpi_atual['Disponibilidade (%)'] - kpi_anterior['Disponibilidade (%)']:.2f}%")
c4.metric("Throughput DL", f"{kpi_atual['Throughput DL (Mbps)']:.1f} Mbps", f"{kpi_atual['Throughput DL (Mbps)'] - kpi_anterior['Throughput DL (Mbps)']:.1f} Mbps")
c5.metric("PRB Utilização", f"{kpi_atual['PRB DL Utilização (%)']:.1f}%", f"{kpi_atual['PRB DL Utilização (%)'] - kpi_anterior['PRB DL Utilização (%)']:.1f}%", delta_color="inverse")
c6.metric("Volume de Dados", f"{kpi_atual['Tráfego Dados (TB)']:.1f} TB", f"{kpi_atual['Tráfego Dados (TB)'] - kpi_anterior['Tráfego Dados (TB)']:.1f} TB")

st.divider()

# 6. Gráficos em Abas
tab1, tab2, tab3 = st.tabs(["📉 Retenção e Mobilidade", "📊 Tráfego e Utilização (PRB)", "⚙️ Qualidade e Latência"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        df_drop = df_filtrado.groupby(['Horário', 'Região'])['Drop Rate (%)'].mean().reset_index()
        fig_drop = px.line(df_drop, x='Horário', y='Drop Rate (%)', color='Região', markers=True, title='Drop Rate por Região (%)', template='plotly_dark')
        fig_drop.add_hline(y=2.0, line_dash="dash", line_color="red", annotation_text="Limite Crítico (>2%)")
        st.plotly_chart(fig_drop, use_container_width=True)
    with col2:
        df_ho = df_filtrado.groupby(['Horário', 'Tecnologia'])['Handover SR (%)'].mean().reset_index()
        fig_ho = px.line(df_ho, x='Horário', y='Handover SR (%)', color='Tecnologia', title='Handover Success Rate por Tecnologia', template='plotly_dark')
        st.plotly_chart(fig_ho, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        df_prb = df_filtrado.groupby(['Horário', 'Região'])['PRB DL Utilização (%)'].mean().reset_index()
        fig_prb = px.area(df_prb, x='Horário', y='PRB DL Utilização (%)', color='Região', title='Utilização de PRB Downlink (Congestionamento)', template='plotly_dark')
        fig_prb.add_hline(y=80.0, line_dash="dash", line_color="orange", annotation_text="Atenção (>80%)")
        st.plotly_chart(fig_prb, use_container_width=True)
    with col2:
        df_traf = df_filtrado.groupby(['Horário', 'Tecnologia'])['Tráfego Dados (TB)'].sum().reset_index()
        fig_traf = px.bar(df_traf, x='Horário', y='Tráfego Dados (TB)', color='Tecnologia', title='Tráfego de Dados Total (TB)', template='plotly_dark')
        st.plotly_chart(fig_traf, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        df_tput = df_filtrado.groupby(['Horário', 'Tecnologia'])['Throughput DL (Mbps)'].mean().reset_index()
        fig_tput = px.line(df_tput, x='Horário', y='Throughput DL (Mbps)', color='Tecnologia', markers=True, title='User Throughput DL (Mbps)', template='plotly_dark')
        st.plotly_chart(fig_tput, use_container_width=True)
    with col2:
        df_lat = df_filtrado.groupby(['Horário', 'Tecnologia'])['Latência (ms)'].mean().reset_index()
        fig_lat = px.box(df_filtrado, x='Tecnologia', y='Latência (ms)', color='Tecnologia', title='Distribuição de Latência', template='plotly_dark')
        st.plotly_chart(fig_lat, use_container_width=True)