import streamlit as st 
import pandas as pd
import datetime
from database import inserir_recebimento_mysql, fetch_contas_mysql

st.set_page_config(page_title='Contas a receber', page_icon="💰", layout="centered")
st.title('Contas a receber')

# Formulário para adicionar uma nova conta a receber
with st.form(key='add_payment_form'):
    vencimento = st.date_input('Data de Vencimento', format='DD/MM/YYYY')
    pagador = st.text_input('Pagador')
    descricao = st.text_input('Descrição')
    valor_input = st.text_input('Valor')
    
    submitted = st.form_submit_button(label='Adicionar Pagamento', type='primary')
    
    if submitted:
        try:
            valor_final = float(valor_input.replace(',', '.'))
            
            nova_conta = {
                'Vencimento': vencimento.strftime('%Y-%m-%d'),
                'Pagador': pagador,
                'Descrição': descricao,
                'Valor': valor_final,
            }
            
            if not inserir_recebimento_mysql(nova_conta):
                st.error("Falha ao inserir o pagamento no banco de dados.")
            else:
                st.success('Pagamento adicionado com sucesso no banco de dados!')
                st.rerun()
        except ValueError:
            st.error("Por favor, digite um valor numérico válido.")

### Exibição da tabela do banco de dados

st.subheader('Pagamentos cadastrados')

# AQUI está a CORREÇÃO: Passa o nome da tabela
contas_db = fetch_contas_mysql('contas_a_receber')

if contas_db:
    df = pd.DataFrame(contas_db)
    
    df['valor'] = df['valor'].apply(lambda x: f"R$ {x:.2f}".replace('.', ','))
    df['vencimento'] = pd.to_datetime(df['vencimento']).dt.strftime('%d/%m/%Y')
    
    st.dataframe(df, use_container_width=True)
else:
    st.info('Nenhum pagamento cadastrado no banco de dados ainda.')