import streamlit as st 
import pandas as pd
import datetime
from database import inserir_investimento_mysql, fetch_contas_mysql

st.set_page_config(page_title='Investimentos', page_icon="📈", layout="centered")
st.title('Meus Investimentos')

# Formulário para adicionar um novo investimento
with st.form(key='add_investment_form'):
    data_investimento = st.date_input('Data do Investimento', format='DD/MM/YYYY')
    ativo = st.text_input('Ativo (Ex: BBDC4, CDB, Tesouro)')
    preco_pago_input = st.text_input('Preço pago (por cota)', help="Deixe em branco se não aplicável")
    cotas_input = st.text_input('Cotas', help="Deixe em branco se não aplicável")
    valor_total_input = st.text_input('Valor Total')
    
    submitted = st.form_submit_button(label='Adicionar Investimento', type='primary')
    
    if submitted:
        try:
            # 1. Validação de campos obrigatórios
            if not ativo or not valor_total_input:
                st.error("Por favor, preencha os campos 'Ativo' e 'Valor Total'.")
                st.stop()
            
            # 2. Converte os valores, tratando campos vazios
            valor_total_final = float(valor_total_input.replace(',', '.'))
            
            if preco_pago_input:
                preco_pago_final = float(preco_pago_input.replace(',', '.'))
            else:
                preco_pago_final = None

            if cotas_input:
                cotas_final = int(cotas_input)
            else:
                cotas_final = None

            novo_investimento = {
                'Data': data_investimento.strftime('%Y-%m-%d'),
                'Ativo': ativo,
                'Preco_Pago': preco_pago_final,
                'Cotas': cotas_final,
                'Valor_Total': valor_total_final,
            }
            
            # 3. Chama a função e armazena o resultado
            resultado_insercao = inserir_investimento_mysql(novo_investimento)

            # 4. Checa o resultado: se for True, deu certo; se for string, é o erro
            if resultado_insercao is True:
                st.success('Investimento adicionado com sucesso!')
                st.rerun()
            else:
                st.error(f"Falha ao inserir: {resultado_insercao}")

        except ValueError:
            st.error("Por favor, verifique se os valores numéricos estão corretos.")


### Exibição da tabela de investimentos

st.subheader('Meus Investimentos')

# Chama a função, passando o nome da tabela 'investimentos'
investimentos_db = fetch_contas_mysql('investimentos')

if investimentos_db:
    df = pd.DataFrame(investimentos_db)
    
    # Formata as colunas para exibição
    df['data'] = pd.to_datetime(df['data']).dt.strftime('%d/%m/%Y')
    df['preco_pago'] = df['preco_pago'].apply(lambda x: f"R$ {x:.2f}".replace('.', ',') if pd.notnull(x) else '')
    df['valor_total'] = df['valor_total'].apply(lambda x: f"R$ {x:.2f}".replace('.', ','))
    
    # Oculta a coluna 'id'
    df_display = df.drop(columns=['id'], errors='ignore')
    
    st.dataframe(df_display, use_container_width=True)
else:
    st.info('Nenhum investimento cadastrado ainda.')