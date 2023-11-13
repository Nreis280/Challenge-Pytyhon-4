
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

'''1. CRIANDO TABELA PARA ARMAZENAR DADOS DA BICICLETA'''
def createTableInfoBike():
    
    conn= getConnection()
    cursor = conn.cursor()
    sql_bike = """
    CREATE TABLE tb_info_bike(
        id_bike     NUMBER(10) PRIMARY KEY,
        marca       VARCHAR2(25) NOT NULL,
        modelo      VARCHAR2(30) NOT NULL,
        valor       NUMBER(11) NOT NULL,
        ano_compra  VARCHAR2(4)  NOT NULL,
        nota_fiscal VARCHAR2(40) NOT NULL,
        id_pf       NUMBER(10)   NOT NULL,
        CONSTRAINT fk_pessoa_fisica FOREIGN KEY (id_pf) REFERENCES tb_pessoa_fisica (id_pf)
)"""

    try:
        cursor.execute(sql_bike)
        print("Tabela t_cycleSurvey_info_bike criada")
    except Exception as e:
        print(f'Erro ao criar a tabela t_cycleSurvey_info_bike: {e}')
    finally:
        cursor.close
        conn.close    

'''2. CRIANDO TABELA PARA ARMZAENAR DADOS DA PESSOA FISICA'''
def createTablePessoaF():
    
    conn= getConnection()
    cursor = conn.cursor()
    sql_pessoaF = """
    CREATE TABLE tb_pessoa_fisica(
        id_pf          NUMBER(10) PRIMARY KEY,
        nm_completo    VARCHAR2(40)  NOT NULL,
        dt_nascimento  DATE          NOT NULL,
        cpf            VARCHAR2(14)  NOT NULL,
        celular        VARCHAR2(14)  NOT NULL,
        cep            VARCHAR2(9)   NOT NULL,
        cidade         VARCHAR2(50)  NOT NULL,
        logradouro     VARCHAR2(100) NOT NULL,
        num_logradouro VARCHAR2(8)   NOT NULL,
        estado         CHAR(2)       NOT NULL,
        complemento    VARCHAR2(20)
        )"""

    try:
        cursor.execute(sql_pessoaF)
        print("Tabela t_cycleSurvey_pessoa_fisica criada")
    except Exception as e:
        print(f'Erro ao criar a tabela t_cycleSurvey_pessoa_fisica: {e}')
    finally:
        cursor.close
        conn.close 

'''3. CRIANDO TABELA PARA ARMAZENAR DADOS DO ACESSORIO DA BICICLETA'''
def createTableAcessorio():
    
    conn= getConnection()
    cursor = conn.cursor()
    sql_acessorio = """
    CREATE TABLE tb_acessorio(
        id_acessorio          NUMBER(10) PRIMARY KEY,
        nota_fiscal_acessorio VARCHAR2(40) NOT NULL,
        marca_acessorio       VARCHAR2(25) NOT NULL,
        modelo                VARCHAR2(40) NOT NULL,
        tipo_acessorio        VARCHAR2(30) NOT NULL,
        valor                 NUMBER(19,2) NOT NULL,
        id_bike               NUMBER(10),
        CONSTRAINT fk_info_bike FOREIGN KEY (id_bike) REFERENCES tb_info_bike (id_bike)
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

# ------------------------------------------------------------ 
## Funções para Obter dados enviados pelo usuario.
def informacao_proprietario():
    infoCliente = []

    print('\n -------- 📋 Informações Pessoais 📋 --------')
    nome = input('\n✏️  Nome completo: ')
    infoCliente.append(nome)

    nascimento = input('📅 Data de Nascimento [dd/mm/aaaa]: ')
    infoCliente.append(nascimento)

    validCpf = 1
    while validCpf == 1 :
        cpf = input('🪪  CPF:')
        if len(cpf) !=11:
            print('CPF inválido!, digite novamente')
            validCpf = 1
        else:
            infoCliente.append(cpf)
            validCpf = 0

    
    validCel = 1
    while validCel == 1 :
        cel = input('📱 Celular: ')
        if len(cel) !=11:
            print('número de telefone inválido, lembre-se de colocar o ddd antes do número')
        else:
            infoCliente.append(cel)
            validCel = 0

    validCep = 1
    while validCep == 1:
        cep = input('📫 CEP: ')
        if len(cep) !=8:
            print('Quantidade de digitos inválida!')
            validCep = 1
        else:
            import requests
            requests = requests.get('https://viacep.com.br/ws/{}/json/'.format(cep))
            address_data = requests.json()
            if 'erro' not in address_data:
                infoCliente.append(cep)
                validCep = 0
            else:
                print('{}: CEP invalido! porfavor insira um cep valido!!'.format(cep))
                print('------------------------------------------------')
                validCep = 1

    cidade = '{}'.format(address_data['localidade'])
    print(f'🏠 Cidade: {cidade}')
    infoCliente.append(cidade)

    logradouro = '{}'.format(address_data['logradouro'])
    print(f'🛣️  logradouro: {logradouro}')
    infoCliente.append(logradouro)

    numero = input('🪧  Número: ')
    infoCliente.append(numero)

    estado = '{}'.format(address_data['uf'])
    print(f'🗺️  Estado: {estado}')
    infoCliente.append(estado)

    complemento = '{}'.format(address_data['complemento'])
    print(f'🏘️  Complemento: {complemento}')
    infoCliente.append(complemento)
    

    return infoCliente

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

                nfAc = input('🧾 Nota Fiscal: ')
                acs.append(nfAc)

                marca = input('🏷️  Marca:')
                acs.append(marca)

                modelo = input('🔖 Modelo: ')
                acs.append(modelo)

                tipo = input('📍 Tipo: ') #pegar o valor para somar com o valor da bike
                acs.append(tipo)
                valorAc = float(input('💰 Valor: ')) #pegar o valor para somar com o valor da bike
                acs.append(valorAc)

                

                
                

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

# ------------------------------------------------------------ 
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

# ------------------------------------------------------------ 
## Funções para Inserir os dados obtidos nas tabelas

def insert_pessoa_fisica(infoCliente):
    conn = getConnection()
    cursor = conn.cursor()
    
    sql_query = "INSERT INTO tb_pessoa_fisica (id_pf, nm_completo, dt_nascimento, cpf, celular, cep, cidade, logradouro, num_logradouro,estado, complemento) VALUES (:0,:1, TO_DATE(:2, 'dd/mm/yyyy'), :3, :4, :5, :6, :7, :8, :9, :10)"

    try:

        cursor.execute("SELECT seq_Pessoa.NEXTVAL FROM dual")
        nextval_result = cursor.fetchone()
        
        if nextval_result:
            pessoa_id = nextval_result[0]

            
            cursor.execute(sql_query, (pessoa_id,infoCliente[0], infoCliente[1], infoCliente[2], infoCliente[3], infoCliente[4],infoCliente[5],infoCliente[6],infoCliente[7],infoCliente[8],infoCliente[9]))
            conn.commit()
            print("Registro de cliente inserido com sucesso.")
            print("Cadastro do Cliente efetuado com sucesso. ID do cliente:", pessoa_id)

            cursor.execute("SELECT seq_Pessoa.currval FROM dual")
            result = cursor.fetchone()
            if result:
                lgi = result[0]
                return lgi
            else:
                    print(f"Erro ao obter o último valor gerado pela sequência: {e}")
        else:
            print("Erro ao obter o próximo valor da sequência")

    except Exception as e:
        print(f'Erro ao inserir o registro de cliente: {e}')
    finally:
        cursor.close()
        conn.close()

def insert_Bike(infoBike,lgi):
    conn = getConnection()
    cursor = conn.cursor()

    sql_query = "INSERT INTO tb_info_bike (id_bike, MARCA, MODELO, VALOR, ANO_COMPRA, NOTA_FISCAL, id_pf) VALUES ( :0, :1, :2, :3, :4, :5, :6)"

    try:
        # Obtenha o próximo valor da sequência
        cursor.execute("SELECT seq_Bike.NEXTVAL FROM dual")
        nextval_result = cursor.fetchone()
        
        if nextval_result:
            bicicleta_id = nextval_result[0]

            # Inserir a bicicleta
            cursor.execute(sql_query, (bicicleta_id,infoBike[0], infoBike[1], infoBike[2], infoBike[3], infoBike[4],lgi))
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

    sql_query = "INSERT INTO tb_acessorio (id_acessorio, nota_fiscal_acessorio, MARCA_ACESSORIO, MODELO, tipo_acessorio, VALOR, id_bike ) VALUES (:0, :1, :2, :3, :4, :5, :6)"

    try:
        
        cursor.execute("SELECT seq_Ac.NEXTVAL FROM dual")
        nextval_result = cursor.fetchone()
        
        if nextval_result:
            ac_id = nextval_result[0]

            cursor.execute(sql_query, (ac_id,acs[0], acs[1], acs[2], acs[3], acs[4], last_generated_id))
            conn.commit()
            print("Cadastro de acessório efetuado com sucesso.")
            print("Cadastro de acessório efetuado com sucesso. ID do Acessorio:", ac_id)
        else:
            print("Erro ao obter o próximo valor da sequência")
    except Exception as e:
        print(f'Erro ao cadastrar acessório: {e}')
    finally:
        cursor.close()
        conn.close()


#Principal
# Variavel para acessar as funções para criar as tabelas!
creatTable = createTablePessoaF(),createTableInfoBike(),createTableAcessorio()
# ------------------------------------------------------------ 

# Criando as seguencias do ID!
create_seq_pessoa()
create_seq_bike()
create_seq_Ac()

# ------------------------------------------------------------ 

# funçoes para cadastrar Proprietario, endereço, bicicleta e acessorio. 
infoP = informacao_proprietario()
inP = insert_pessoa_fisica(infoP)
infoB = cadastrar_bike()
# ------------------------------------------------------------ 

# funçoes para inserir no banco de dados as informaçoes Proprietario , endereço, bicicleta e acessoerios.

inB = insert_Bike(infoB,inP) 
