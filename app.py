import streamlit as st
import pandas as pd
import altair as alt
from database import fetch_contas_mysql

st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.title("Visão Geral Financeira")

# --- Cria o layout de 2 colunas para a primeira linha ---
col1, col2 = st.columns(2)

# --- Gráfico de Gastos por Setor (Gráfico de Barras) ---
with col1:
    st.subheader("Gastos por Setor")
    df_pagar = fetch_contas_mysql('contas_a_pagar')
    if df_pagar:
        df_pagar = pd.DataFrame(df_pagar)
        df_pagar['valor'] = pd.to_numeric(df_pagar['valor'])
        
        gastos_por_setor = df_pagar.groupby('setor')['valor'].sum().reset_index()
        gastos_por_setor.columns = ['Setor', 'Total']
        
        st.bar_chart(gastos_por_setor, x='Setor', y='Total')
    else:
        st.info("Nenhum dado de contas a pagar para exibir.")

# --- Contas Recebidas vs. Contas a Pagar (Gráfico de Linhas) ---
with col2:
    st.subheader("Recebidas vs. a Pagar (Últimos Meses)")
    df_pagar = fetch_contas_mysql('contas_a_pagar')
    df_receber = fetch_contas_mysql('contas_a_receber')

    if df_pagar and df_receber:
        df_pagar = pd.DataFrame(df_pagar)
        df_receber = pd.DataFrame(df_receber)
        
        # Converte para o tipo de dado correto
        df_pagar['vencimento'] = pd.to_datetime(df_pagar['vencimento'])
        df_pagar['valor'] = pd.to_numeric(df_pagar['valor'])
        df_receber['vencimento'] = pd.to_datetime(df_receber['vencimento'])
        df_receber['valor'] = pd.to_numeric(df_receber['valor'])

        # Prepara os dados por mês
        df_pagar['mes_ano'] = df_pagar['vencimento'].dt.to_period('M').astype(str)
        df_receber['mes_ano'] = df_receber['vencimento'].dt.to_period('M').astype(str)

        gastos_mensais = df_pagar.groupby('mes_ano')['valor'].sum().reset_index()
        receitas_mensais = df_receber.groupby('mes_ano')['valor'].sum().reset_index()

        # Combina os dados em um único DataFrame
        df_merged = pd.merge(gastos_mensais, receitas_mensais, on='mes_ano', how='outer', suffixes=('_pagar', '_receber')).fillna(0)
        df_merged = df_merged.rename(columns={'valor_pagar': 'Contas a Pagar', 'valor_receber': 'Contas a Receber'})

        # Cria o gráfico de linhas
        st.line_chart(df_merged, x='mes_ano')
    else:
        st.info("Dados de contas a pagar ou a receber insuficientes para o gráfico.")

st.markdown("---") # Linha divisória entre os gráficos

# --- Cria o layout de 2 colunas para a segunda linha ---
col3, col4 = st.columns(2)

# --- Meta de Investimento (Gráfico de Rosca) ---
with col3:
    st.subheader("Meta de R$ 10.000,00")
    
    df_invest = fetch_contas_mysql('investimentos')
    
    meta = 10000.00
    if df_invest:
        df_invest = pd.DataFrame(df_invest)
        # CORRIGIDO: usa 'valor_total'
        df_invest['valor_total'] = pd.to_numeric(df_invest['valor_total'])
        
        total_investido = df_invest['valor_total'].sum()
        
        # Cria um DataFrame para o gráfico de rosca
        df_meta = pd.DataFrame({
            'categoria': ['Alcançado', 'Falta'],
            'valor': [total_investido, max(0, meta - total_investido)]
        })
        
        base = alt.Chart(df_meta).encode(
            theta=alt.Theta("valor", stack=True)
        )
        
        chart = base.mark_arc(outerRadius=120, innerRadius=80).encode(
            color=alt.Color("categoria", scale=alt.Scale(domain=['Alcançado', 'Falta'], range=['#4CAF50', '#f3f3f3'])),
            order=alt.Order("valor", sort="descending"),
            tooltip=['categoria', 'valor']
        )
        
        st.altair_chart(chart, use_container_width=True)
        st.metric(label="Total Investido", value=f"R$ {total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    else:
        st.info("Nenhum dado de investimentos para exibir.")

# --- Investimentos por Ativo (Gráfico de Pizza) ---
with col4:
    st.subheader("Investimentos por Ativo")
    
    df_invest = fetch_contas_mysql('investimentos')
    if df_invest:
        df_invest = pd.DataFrame(df_invest)
        # CORRIGIDO: usa 'valor_total'
        df_invest['valor_total'] = pd.to_numeric(df_invest['valor_total'])
        
        # Agrupa os dados por ativo e soma os valores
        invest_por_ativo = df_invest.groupby('ativo')['valor_total'].sum().reset_index()
        invest_por_ativo.columns = ['Ativo', 'Total']

        base = alt.Chart(invest_por_ativo).encode(
            theta=alt.Theta("Total", stack=True)
        )
        
        pie = base.mark_arc(outerRadius=120).encode(
            color=alt.Color("Ativo"),
            order=alt.Order("Total", sort="descending"),
            tooltip=["Ativo", "Total"]
        )
        
        st.altair_chart(pie, use_container_width=True)
    else:
        st.info("Nenhum dado de investimentos para exibir.")