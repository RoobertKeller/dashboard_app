import pymysql

# Configurações do seu banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = '957947564$Rk' # Sua senha!
db_name = 'personal_finance'

def get_connection():
    """Retorna uma nova conexão com o banco de dados."""
    return pymysql.connect(
        host=db_host,
        user=db_user,
        passwd=db_password,
        db=db_name
    )

def inserir_conta_mysql(conta):
    """Insere um único registro de conta a pagar no banco de dados MySQL."""
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO contas_a_pagar (vencimento, beneficiario, descricao, parcela, setor, valor, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            dados = (
                conta['Vencimento'],
                conta['Beneficiário'],
                conta['Descrição'],
                conta['Parcela'],
                conta['Setor'],
                conta['Valor'],
                'Pendente'
            )
            cursor.execute(sql, dados)
            connection.commit()
            return True
    except Exception as e:
        print(f"Erro ao conectar ou inserir no banco de dados: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

def inserir_recebimento_mysql(pagamento):
    """Insere um registro de recebimento no banco de dados MySQL."""
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO contas_a_receber (vencimento, pagador, descricao, valor)
                VALUES (%s, %s, %s, %s)
            """
            dados = (
                pagamento['Vencimento'],
                pagamento['Pagador'],
                pagamento['Descrição'],
                pagamento['Valor']
            )
            cursor.execute(sql, dados)
            connection.commit()
            return True
    except Exception as e:
        print(f"Erro ao conectar ou inserir no banco de dados: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

def inserir_investimento_mysql(investimento):
    """Insere um registro de investimento no banco de dados MySQL."""
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO investimentos (data, ativo, preco_pago, cotas, valor_total)
                VALUES (%s, %s, %s, %s, %s)
            """
            dados = (
                investimento['Data'],
                investimento['Ativo'],
                investimento['Preco_Pago'],
                investimento['Cotas'],
                investimento['Valor_Total']
            )
            cursor.execute(sql, dados)
            connection.commit()
            return True
    except Exception as e:
        return str(e)
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            
def fetch_contas_mysql(table_name):
    """Busca e retorna todos os registros de uma tabela específica."""
    try:
        connection = get_connection()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = f"SELECT * FROM {table_name}"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Erro ao buscar dados do banco de dados: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

def atualizar_status_mysql(conta_id, novo_status):
    """Atualiza o status de uma conta no banco de dados pelo seu ID."""
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "UPDATE contas_a_pagar SET status = %s WHERE id = %s"
            cursor.execute(sql, (novo_status, conta_id))
            connection.commit()
            return True
    except Exception as e:
        print(f"Erro ao atualizar o status: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()