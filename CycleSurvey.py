from flask import Flask, render_template, request, redirect, url_for, jsonify


import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_12")
""" """ 
def getConnection():
    try:
        connection = cx_Oracle.connect("RM98819", "260104", "oracle.fiap.com.br/ORCL")
        """  connection = cx_Oracle.connect(user="RM98819", password="260104", host="oracle.fiap.com.br", port="1521", service="ORCL") """
        print("conexão: ", connection.version)
        return connection
    except Exception as e:
        print(f'Erro ao obter conexão: {e}')

'''1. CRIANDO TABELA PARA ARMAZENAR ENDEREÇO DA PESSOA FISICA'''
def createTableEndereco():
    conn= getConnection()
    cursor = conn.cursor()
    sql_endereco = """
    CREATE TABLE t_cycleSurvey_endereco(
        CEP VARCHAR(9) NOT NULL,
        CIDADE VARCHAR(50) NOT NULL,
        LOGRADOURO VARCHAR(100) NOT NULL,
        NUM_LOGRADOURO VARCHAR(8) NOT NULL,
        ESTADO CHAR(2) NOT NULL,
        COMPLEMENTO VARCHAR(15),
        CONSTRAINT pk_t_cycleSurvey_endereco PRIMARY KEY (cep)
    )"""

    try:
        cursor.execute(sql_endereco)
        print("Tabela t_cycleSurvey_endereco criada")
    except Exception as e:
        print(f'Erro ao criar a tabela t_cycleSurvey_endereco: {e}')
    finally:
        cursor.close
        conn.close    

'''2. CRIANDO TABELA PARA ARMAZENAR DADOS DA BICICLETA'''
def createTableInfoBike():
    
    conn= getConnection()
    cursor = conn.cursor()
    sql_bike = """
    CREATE TABLE t_cycleSurvey_info_bike(
        BICICLETA_ID NUMERIC(10),
        MARCA VARCHAR(25) NOT NULL,
        MODELO VARCHAR(30) NOT NULL,
        VALOR VARCHAR(11) NOT NULL,
        ANO_COMPRA VARCHAR(4) NOT NULL,
        NOTA_FISCAL VARCHAR(40) NOT NULL,
        CONSTRAINT pk_t_cycleSurvey_info_bike PRIMARY KEY(bicicleta_id)
)"""

    try:
        cursor.execute(sql_bike)
        print("Tabela t_cycleSurvey_info_bike criada")
    except Exception as e:
        print(f'Erro ao criar a tabela t_cycleSurvey_info_bike: {e}')
    finally:
        cursor.close
        conn.close    

'''3. CRIANDO TABELA PARA ARMZAENAR DADOS DA PESSOA FISICA'''
def createTablePessoaF():
    
    conn= getConnection()
    cursor = conn.cursor()
    sql_pessoaF = """
    CREATE TABLE t_cycleSurvey_pessoa_fisica (
        ID_PESSOA NUMERIC(10),
        NM_COMPLETO VARCHAR2(40) NOT NULL,
        DT_NASCIMENTO DATE NOT NULL,
        CPF VARCHAR2(14) NOT NULL,
        CELULAR VARCHAR2(14) NOT NULL,
        CEP VARCHAR2(9),
        BICICLETA_ID NUMBER,
        CONSTRAINT fk_pessoa_fisica_bicicleta FOREIGN KEY (BICICLETA_ID) REFERENCES t_cycleSurvey_info_bike (BICICLETA_ID),
        CONSTRAINT fk_pessoa_fisica_endereco FOREIGN KEY (CEP) REFERENCES t_cycleSurvey_endereco (CEP),
        CONSTRAINT pk_t_cycleSurvey_pessoa_fisica PRIMARY KEY (ID_PESSOA)
    )"""

    try:
        cursor.execute(sql_pessoaF)
        print("Tabela t_cycleSurvey_pessoa_fisica criada")
    except Exception as e:
        print(f'Erro ao criar a tabela t_cycleSurvey_pessoa_fisica: {e}')
    finally:
        cursor.close
        conn.close 

'''4. CRIANDO TABELA PARA ARMAZENAR DADOS DO ACESSORIO DA BICICLETA'''
def createTableAcessorio():
    
    conn= getConnection()
    cursor = conn.cursor()
    sql_acessorio = """
    CREATE TABLE t_cycleSurvey_acessorio (
        ACESSORIO_ID NUMERIC(10),
        MARCA_ACESSORIO VARCHAR2(25) NOT NULL,
        MODELO VARCHAR2(40) NOT NULL,
        TIPO_ACESSORIO VARCHAR2(30) NOT NULL,
        VALOR VARCHAR2(11) NOT NULL,
        NOTA_FISCAL VARCHAR2(40) NOT NULL,
        BICICLETA_ID NUMBER,
        CONSTRAINT fk_acessorio_bicicleta FOREIGN KEY (BICICLETA_ID) REFERENCES t_cycleSurvey_info_bike (BICICLETA_ID),
        CONSTRAINT pk_t_cycleSurvey_acessorio PRIMARY KEY (ACESSORIO_ID)
    )
"""
    try:
        cursor.execute(sql_acessorio)
        print("Tabela t_cycleSurvey_acessorio criada")
    except Exception as e:
        print(f'Erro ao criar a tabela t_cycleSurvey_acessorio: {e}')
    finally:
        cursor.close
        conn.close    

## Funções para Obter dados enviados pelo usuario.
def informacao_proprietario():
    infoCliente = []

    print('\n -------- 📋 Informações Pessoais 📋 --------')
    nome = input('\n✏️  Nome completo: ')
    infoCliente.append(nome)

    nascimento = input('📅 Data de Nascimento [dd/mm/aaaa]: ')
    infoCliente.append(nascimento)

    cpf = input('🪪  CPF:')
    infoCliente.append(cpf)

    cel = input('📱 Celular: ')
    infoCliente.append(cel)

    return infoCliente

def informacao_endereco():
    infoEndereco = []

    cep = input('📫 CEP: ')
    infoEndereco.append(cep)

    cidade = input('🏠 Cidade: ')
    infoEndereco.append(cidade)

    logradouro = input('🛣️  logradouro:')
    infoEndereco.append(logradouro)

    numero = input('🪧  Número: ')
    infoEndereco.append(numero)

    estado = input('🗺️  Estado:')
    infoEndereco.append(estado)

    complemento = input('🏘️  Complemento:')
    infoEndereco.append(complemento)

    return infoEndereco

def cadastrar_bike():
    infoBike = []

    print('\n -------- 🚴Informações da Bike🚴 --------')
    marca = input('🏷️  Marca:')
    infoBike.append(marca)
    
    modelo = input('🔖 Modelo: ')
    infoBike.append(modelo)

    valorBike = float(input('💰 Valor: ')) #pegar o valor para somar com o valor do acessório
    infoBike.append(valorBike)

    anoBike = input('📅 Ano da compra: ') #validar if ano > 8 não entra
    infoBike.append(anoBike)

    nfBike = input('🧾 Nota Fiscal: ')
    infoBike.append(nfBike)
    

    #b = int(input('Deseja Fazer mais alguma operação?\n [0] = SIM \n [1] = NÃO \n'))
    #stop += b
    
    return infoBike

def cadastrar_acessorio(last_generated_id):
    escolha = 3
    while escolha == 3:
        ac = input("\nPossui acessório? (sim/não): ")
        if ac.lower() == "sim": #lower serve para que as letras maiusculas seja tranformadas em minusculas.
            escolha = 1
            r = 1
            while r == 1:
                acs = []
                print('\n -------- Informações do Acessório --------')
                print(f'Acessorio:')
                marca = input('🏷️  Marca:')
                acs.append(marca)
                
                modelo = input('🔖 Modelo: ')
                acs.append(modelo)

                valorAc = float(input('💰 Valor: ')) #pegar o valor para somar com o valor da bike
                acs.append(valorAc)

                tipo = input('📍 Tipo: ') #pegar o valor para somar com o valor da bike
                acs.append(tipo)

                nfAc = input('🧾 Nota Fiscal: ')
                acs.append(nfAc)
                

                falha=1
                while falha == 1:
                    resp = input("\nPossui mais um acessório? (sim/não): ")
                    if resp.lower() == "sim":
                        insert_Ac(acs,last_generated_id)
                        r = 1
                        falha = 0
                    elif resp.lower() == "nao" or resp.lower() == "não":
                        insert_Ac(acs,last_generated_id)
                        r = 2
                        falha = 0
                        return acs
                    else:
                        print('\nOpção inválida! Tente novamente')
                        falha = 1

        elif ac.lower() == "nao" or ac.lower() == "não":
            escolha = 2
        else:
            print('\nOpção inválida! Tente novamente')
            escolha = 3


## Funções para criar sequencias de IDs de cada tabala
def create_seq_pessoa():
    conn = getConnection()
    cursor = conn.cursor()

    create_sequence_query = """
    CREATE SEQUENCE seq_Pessoa
        START WITH 1
        INCREMENT BY 1
        MINVALUE 1
        MAXVALUE 1000
        NOCYCLE
    """
    
    try:
        cursor.execute(create_sequence_query)
        conn.commit()
        print("Sequência seq_Pessoa criada com sucesso.")
    except Exception as e:
        print(f'Erro ao criar a sequência: {e}')
    finally:
        cursor.close()
        conn.close()

def create_seq_bike():
    conn = getConnection()
    cursor = conn.cursor()

    create_sequence_Bike = """
    CREATE SEQUENCE seq_Bike
        START WITH 1
        INCREMENT BY 1
        MINVALUE 1
        MAXVALUE 1000
        NOCYCLE
    """
    
    try:
        cursor.execute(create_sequence_Bike)
        conn.commit()
        print("Sequência seq_Bike criada com sucesso.")
        return create_sequence_Bike
    except Exception as e:
        print(f'Erro ao criar a sequência: {e}')
    finally:
        cursor.close()
        conn.close()

def create_seq_Ac():
    conn = getConnection()
    cursor = conn.cursor()

    create_sequence_query = """
    CREATE SEQUENCE seq_Ac
        START WITH 1
        INCREMENT BY 1
        MINVALUE 1
        MAXVALUE 1000
        NOCYCLE
    """
    
    try:
        cursor.execute(create_sequence_query)
        conn.commit()
        print("Sequência seq_Ac criada com sucesso.")
    except Exception as e:
        print(f'Erro ao criar a sequência: {e}')
    finally:
        cursor.close()
        conn.close()


## Funções para Inserir os dados obtidos nas tabelas
def insert_endereco(infoEndereco):
    conn = getConnection()
    cursor = conn.cursor()
    sql_query = "INSERT INTO t_cycleSurvey_endereco (CEP, CIDADE , LOGRADOURO, NUM_LOGRADOURO, ESTADO, COMPLEMENTO) VALUES (:0, :1, :2, :3, :4, :5)"
    try:
        cursor.execute(sql_query, (infoEndereco[0], infoEndereco[1], infoEndereco[2], infoEndereco[3], infoEndereco[4], infoEndereco[5]))
        conn.commit()
        print("Registro inserido")
    except Exception as e:
        print(f'Erro ao inserir o registro: {e}')
    finally:
        cursor.close
        conn.close

def insert_pessoa_fisica(infoCliente, infoEndereco):
    conn = getConnection()
    cursor = conn.cursor()
    sql_query = "INSERT INTO t_cycleSurvey_pessoa_fisica (ID_PESSOA, NM_COMPLETO, DT_NASCIMENTO, CPF, CELULAR, CEP) VALUES (seq_Pessoa.NEXTVAL, :0, TO_DATE(:1, 'dd/mm/yyyy'), :2, :3, :4)"

    
    try:
        cursor.execute(sql_query, (infoCliente[0], infoCliente[1], infoCliente[2], infoCliente[3], infoEndereco[0]))
        conn.commit()
        print("Registro de cliente inserido com sucesso.")
    except Exception as e:
        print(f'Erro ao inserir o registro de cliente: {e}')
    finally:
        cursor.close()
        conn.close()

def insert_Bike(infoBike):
    conn = getConnection()
    cursor = conn.cursor()

    try:
        # Obtenha o próximo valor da sequência
        cursor.execute("SELECT seq_Bike.NEXTVAL FROM dual")
        nextval_result = cursor.fetchone()
        
        if nextval_result:
            bicicleta_id = nextval_result[0]

            # Inserir a bicicleta
            sql_query = "INSERT INTO t_cycleSurvey_info_bike (BICICLETA_ID, MARCA, MODELO, VALOR, ANO_COMPRA, NOTA_FISCAL) VALUES ( :0, :1, :2, :3, :4, :5)"
            cursor.execute(sql_query, (bicicleta_id,infoBike[0], infoBike[1], infoBike[2], infoBike[3], infoBike[4]))
            conn.commit()
            print("Cadastro de bicicleta efetuado com sucesso. ID da bicicleta:", bicicleta_id)

            cursor.execute("SELECT seq_Bike.currval FROM dual")
            result = cursor.fetchone()
            if result:
                last_generated_id = result[0]
                return last_generated_id
            else:
                print(f"Erro ao obter o último valor gerado pela sequência: {e}")

        else:
            print("Erro ao obter o próximo valor da sequência")
    except Exception as e:
        print(f'Erro ao cadastrar bicicleta: {e}')
    finally:
        cadastrar_acessorio(last_generated_id)
        cursor.close()
        conn.close()

def insert_Ac(acs, last_generated_id):
    conn = getConnection()
    cursor = conn.cursor()

    sql_query = "INSERT INTO t_cycleSurvey_acessorio (ACESSORIO_ID, MARCA_ACESSORIO, MODELO, TIPO_ACESSORIO, VALOR, NOTA_FISCAL, BICICLETA_ID) VALUES (seq_Ac.NEXTVAL, :0, :1, :2, :3, :4, :5)"

    try:
        cursor.execute(sql_query, (acs[0], acs[1], acs[2], acs[3], acs[4], last_generated_id))
        conn.commit()
        print("Cadastro de acessório efetuado com sucesso.")
    except Exception as e:
        print(f'Erro ao cadastrar acessório: {e}')
    finally:
        cursor.close()
        conn.close()


#Principal
# Variavel para acessar as funções para criar as tabelas!
""" creatTable= createTableEndereco(),createTableInfoBike(),createTablePessoaF(),createTableAcessorio() """

# Variavel para acessar as funções para criar as seguencias do ID!
""" seq = create_seq_pessoa() """

""" ifo = informacao_proprietario()
infoE = informacao_endereco() """

""" ine = insert_endereco(ifo) """

""" ine = insert_endereco(infoE)
ins = insert_pessoa_fisica(ifo,infoE) """

b = cadastrar_bike()
