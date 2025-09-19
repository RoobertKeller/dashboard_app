import streamlit as st 
import pandas as pd
import datetime
from database import inserir_conta_mysql, fetch_contas_mysql

st.set_page_config(page_title='Contas a pagar', page_icon="💰", layout="centered")
st.title('Contas a pagar')

# Formulário para adicionar uma nova conta a pagar
with st.form(key='add_account_form'):
    vencimento_original = st.date_input('Data de Vencimento', format='DD/MM/YYYY')
    beneficiario = st.text_input('Beneficiário')
    descricao = st.text_input('Descrição')
    parcelas_input = st.number_input('Parcelas', min_value=1, step=1)
    setor = st.selectbox('Setor', ['Saúde', 'Compras', 'Transporte', 'Lazer'])
    valor_input = st.text_input('Valor')
    
    submitted = st.form_submit_button(label='Adicionar Conta', type='primary')

    if submitted:
        try:
            valor_final = float(valor_input.replace(',', '.'))
            
            for i in range(int(parcelas_input)):
                mes_da_parcela = vencimento_original.month + i
                ano_da_parcela = vencimento_original.year + (mes_da_parcela - 1) // 12
                mes_da_parcela = (mes_da_parcela - 1) % 12 + 1
                
                try:
                    data_parcela = datetime.date(ano_da_parcela, mes_da_parcela, vencimento_original.day)
                except ValueError:
                    data_parcela = datetime.date(ano_da_parcela, mes_da_parcela, 1).replace(day=28)
                
                nova_conta = {
                    'Vencimento': data_parcela.strftime('%Y-%m-%d'),
                    'Beneficiário': beneficiario,
                    'Descrição': f"{descricao} ({i+1}/{int(parcelas_input)})",
                    'Parcela': f"{i+1}/{int(parcelas_input)}",
                    'Setor': setor,
                    'Valor': valor_final,
                }
                
                if not inserir_conta_mysql(nova_conta):
                    st.error(f"Falha ao inserir a parcela {i+1} no banco de dados.")
                    break
            else:
                st.success('Contas adicionadas com sucesso no banco de dados!')
                st.rerun()
        except ValueError:
            st.error("Por favor, digite um valor numérico válido.")


### Exibição da tabela do banco de dados

st.subheader('Contas Cadastradas')

contas_db = fetch_contas_mysql('contas_a_pagar')

if contas_db:
    df = pd.DataFrame(contas_db)
    
    # 1. Converte a coluna para o tipo de data
    df['vencimento'] = pd.to_datetime(df['vencimento'])
    
    # 2. Ordena o DataFrame pela data de vencimento
    df.sort_values(by='vencimento', inplace=True)

    # Formata as colunas para exibição
    df['vencimento'] = df['vencimento'].dt.strftime('%d/%m/%Y')
    df['valor'] = df['valor'].apply(lambda x: f"R$ {x:.2f}".replace('.', ','))

    # Oculta colunas que você não quer exibir
    columns_to_hide = ['id', 'pago', 'status']
    df = df.drop(columns=columns_to_hide, errors='ignore')
    
    st.dataframe(df, use_container_width=True)
else:
    st.info('Nenhuma conta cadastrada no banco de dados ainda.')