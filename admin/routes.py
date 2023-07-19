from flask import Flask, render_template, request, Blueprint
import sqlite3
import pandas as pd
import threading
import datetime

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def index():
    return render_template('admin.html')

@admin.route('/admin/importa_relatorio_ciap', methods=['GET', 'POST'])
def importa_relatorio_ciap():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
            # Carregar o arquivo Excel usando a biblioteca pandas
            df = pd.read_excel(file)

            # Conectar ao banco de dados SQLite
            conn = sqlite3.connect('ciap.db')

            # Inserir os dados no banco de dados
            df.to_sql('ciap_s4hana', conn, if_exists='append', index=False)

            # Fechar a conexão com o banco de dados
            conn.close()

            return render_template('admin.html', message_relatorio_ciap='Dados importados com sucesso')

        else:
            return render_template('admin.html', message_relatorio_ciap='Tipo de arquivo inválido. Por favor, envie um arquivo Excel')

    return render_template('admin.html')

@admin.route('/admin/importa_relatorio_zsdr133', methods=['GET', 'POST'])
def importa_relatorio_zsdr133():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
            # Carregar o arquivo Excel usando a biblioteca pandas
            df = pd.read_excel(file)

            # Conectar ao banco de dados SQLite
            conn = sqlite3.connect('ciap.db')

            # Inserir os dados no banco de dados
            df.to_sql('entradas_fiscais', conn, if_exists='append', index=False)

            # Fechar a conexão com o banco de dados
            conn.close()

            return render_template('admin.html', message_133='Dados importados com sucesso')

        else:
            return render_template('admin.html', message_133='Tipo de arquivo inválido. Por favor, envie um arquivo Excel')

    return render_template('admin.html')

@admin.route('/admin/importa_tabela_anek', methods=['GET', 'POST'])
def importa_tabela_anek():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
            # Carregar o arquivo Excel usando a biblioteca pandas
            df = pd.read_excel(file)

            # Conectar ao banco de dados SQLite
            conn = sqlite3.connect('ciap.db')

            # Inserir os dados no banco de dados
            df.to_sql('ANEK', conn, if_exists='append', index=False)

            # Fechar a conexão com o banco de dados
            conn.close()

            return render_template('admin.html', message_anek='Dados importados com sucesso')

        else:
            return render_template('admin.html', message_anek='Tipo de arquivo inválido. Por favor, envie um arquivo Excel')

    return render_template('admin.html')

@admin.route('/admin/importa_tabela_anla', methods=['GET', 'POST'])
def importa_tabela_anla():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
            # Carregar o arquivo Excel usando a biblioteca pandas
            df = pd.read_excel(file)

            # Conectar ao banco de dados SQLite
            conn = sqlite3.connect('ciap.db')

            # Inserir os dados no banco de dados
            df.to_sql('ANLA', conn, if_exists='append', index=False)

            # Fechar a conexão com o banco de dados
            conn.close()

            return render_template('admin.html', message_relatorio_ciap='Dados importados com sucesso')

        else:
            return render_template('admin.html', message_relatorio_ciap='Tipo de arquivo inválido. Por favor, envie um arquivo Excel')

    return render_template('admin.html')

@admin.route('/admin/importa_planilha_transferencias_e_baixas', methods=['GET', 'POST'])
def importa_planilha_modelo_transferencias_e_baixas():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
            # Carregar o arquivo Excel usando a biblioteca pandas
            df = pd.read_excel(file)

            # Conectar ao banco de dados SQLite
            conn = sqlite3.connect('ciap.db')

            # Inserir os dados no banco de dados
            df.to_sql('planilha_transferencias_baixas', conn, if_exists='append', index=False)

            # Fechar a conexão com o banco de dados
            conn.close()

            return render_template('admin.html', message_relatorio_ciap='Dados importados com sucesso')

        else:
            return render_template('admin.html', message_relatorio_ciap='Tipo de arquivo inválido. Por favor, envie um arquivo Excel')

    return render_template('admin.html')

@admin.route('/admin/criar_relatorio_ciap_consolidado', methods=['GET', 'POST'])
def criar_relatorio_ciap_consolidado():
    conexao = sqlite3.connect('ciap.db')
    cursor = conexao.cursor()
    if request.method == 'POST':
        if 'criar-ciap-consolidado' in request.form:
            executar_criacao_relatorio_ciap_consolidado()
            cursor.execute("""CREATE TABLE IF NOT EXISTS CIAP_CONSOLIDADO AS SELECT "Nota Fiscal"	AS NF,	"Nº Documento"	AS	DOCNUM,	entradas_fiscais."Empresa"	AS	EMPRESA,	"Local de negócio"	AS	LOC_NEG,	"Parceiro"	AS	COD_PART,	
                    "Nº CNPJ"	AS	CNPJ_PART,	"Nº CPF"	AS	CPF_PART,	entradas_fiscais."Data de lançamento"	AS	DATA_LANCAMENTO,	"Item NF"	AS	NUM_ITEM,	
                    entradas_fiscais."Material"	AS	MATERIAL,	"Texto breve material"	AS	DESCRICAO_MATERIAL,	"NCM"	AS	NCM,	"CFOP"	AS	CFOP,	
                    "Qdt. Un. Med. Básica"	AS	QTD,	"Un. Med. Básica"	AS	UND_MEDIDA,	"Valor Total"	AS	VLR_TOTAL,	"Valor Produtos"	AS	VLR_PRODUTOS,	
                    "Valor ICMS"	AS	VLR_ICMS,	"IVA"	AS	IVA,	"Item Pedido de Compra"	AS	ITEM_PEDIDO,	"Pedido de Compra"	AS	PEDIDO,
                    "Doc. MIRO"	AS	DOC_MIRO,	"Doc.referência"	AS	DOC_REF,	"Conta Contábil Pedido"	AS	CC_PEDIDO,	"Descrição da Conta"	AS	DESCRICAO_CC,	
                    "Chave de Acesso"	AS	CHV_NFE_CTE,	"Dt.iníc.depreciação"	AS	DT_INICIO_DEPRECIACAO,	"Tp.movimento imob."	AS	TP_MOVIMENTO,	
                    "Subnº"	AS	SUB_ITEM,	ciap_s4hana."Imobilizado"	AS	IMOBILIZADO,	"Nº do imobilizado"	AS	"IMOBILIZADO+SUBITEM",	"Centro custo ativo"	AS	CENTRO_CUSTO,	
                    "Classe imobilizado"	AS	CLASSE,	"Determ.contas"	AS	DETERM_CONTAS,	"Vida útil planejada"	AS	VIDA_UTIL_PLANEJADA,	
                    "Transação CAP"	AS	TRANS_CAP,	"Ajuste do valor"	AS	AJ_VALOR,	"Ano de aquisição"	AS	ANO_AQUISICAO,	ciap_s4hana."Atribuição"	AS	ATRIBUICAO,	
                    "Baixa"	AS	BAIXA,	"Chave de depreciação"	AS	CHV_DEPRECIACAO,	"Ctg.tipo movimento"	AS	CTG_TIPO_MOV,	"Data da criação"	AS	DT_CRIACAO,	
                    "Data de referência"	AS	DT_REFERENCIA,	"Depreciação baixa"	AS	DEPRECIACAO_BAIXA,	"Dt.lnçmto.cont."	AS	DT_LANÇAMENTO_CONTABIL,
                    "Elemento PEP"	AS	ELEMENTO_PEP,	ANEK."Referência"	AS	REFERENCIA,	ciap_s4hana."Período contábil"	AS	PERIODO_CONTABIL,	"Mont.moeda empresa"	AS	MONTANTE,	
                    "Depreciação normal"	AS	DEPRECIACAO_NORMAL
                    
                    FROM entradas_fiscais
                    INNER JOIN ANEK ON entradas_fiscais."Doc. MIRO" = ANEK."Doc.ref."
                           AND entradas_fiscais."Pedido de Compra" = ANEK."Doc.compra" 
                           AND entradas_fiscais."Item Pedido de Compra" = ANEK."Item"
                          
                    INNER JOIN ciap_s4hana ON ANEK."Doc.ref." = ciap_s4hana."Doc.referência"
                           AND ANEK."Imobilizado" = ciap_s4hana."Imobilizado"
                           AND ANEK."Sbnº" = SUBSTRING(ciap_s4hana."Subnº", 1, 1)
                           AND entradas_fiscais."Doc. MIRO" = ciap_s4hana."Doc.referência"
                    WHERE ANEK."Op.refer." = "RMRP" and ciap_s4hana."Está estornando" = 0 """)

            conexao.commit()
            conexao.close()
            excluir_105_e_100_correspondente()
            criar_tabela_temp()
            juntar_tabelas()
            criar_colunas_adicionais()
            preencher_colunas_adicionais()
            criar_ci()

            return render_template('admin.html',message_funcao_criar_relatorio_ciap='Função Executada com Sucesso')
    return render_template('admin.html',message_funcao_criar_relatorio_ciap='Erro na Função')
def executar_criacao_relatorio_ciap_consolidado():
    thread = threading.Thread(target=criar_relatorio_ciap_consolidado)
    thread.start()
def excluir_105_e_100_correspondente():
    conexao = sqlite3.connect('ciap.db')
    cursor = conexao.cursor()
    cursor.execute("""DELETE FROM CIAP_CONSOLIDADO
                WHERE TP_MOVIMENTO = '105 (Nota de crédito no exercício da fatura)'
                OR (TP_MOVIMENTO = '100 (Aquisição do imobilizado externo)'
                   AND "IMOBILIZADO+SUBITEM" IN (
                       SELECT "IMOBILIZADO+SUBITEM"
                       FROM CIAP_CONSOLIDADO
                       WHERE TP_MOVIMENTO = '105 (Nota de crédito no exercício da fatura)'
                   )
                   AND doc_miro IN (
                       SELECT doc_miro
                       FROM CIAP_CONSOLIDADO
                       WHERE TP_MOVIMENTO = '105 (Nota de crédito no exercício da fatura)'
                   )
                  );""")

    conexao.commit()
    conexao.close()
# def criar_coluna_repetido():
#     conexao = sqlite3.connect('ciap.db')
#     cursor = conexao.cursor()
#     cursor.execute("""ALTER TABLE CIAP_CONSOLIDADO ADD COLUMN informacao VARCHAR(50);""")
#     cursor.execute("""
#         UPDATE CIAP_CONSOLIDADO
#         SET informacao = CASE
#             WHEN (
#               SELECT COUNT(*) FROM CIAP_CONSOLIDADO AS t2
#               WHERE t2."IMOBILIZADO+SUBITEM" = CIAP_CONSOLIDADO."IMOBILIZADO+SUBITEM"
#             ) > 1 AND (
#               SELECT COUNT(DISTINCT "DOC_MIRO") FROM CIAP_CONSOLIDADO AS t2
#               WHERE t2."IMOBILIZADO+SUBITEM" = CIAP_CONSOLIDADO."IMOBILIZADO+SUBITEM"
#             ) = 1 THEN 'Repetido com dado diferente'
#             WHEN (
#               SELECT COUNT(*) FROM CIAP_CONSOLIDADO AS t2
#               WHERE t2."IMOBILIZADO+SUBITEM" = CIAP_CONSOLIDADO."IMOBILIZADO+SUBITEM"
#             ) > 1 AND (
#               SELECT COUNT(DISTINCT "DOC_MIRO") FROM CIAP_CONSOLIDADO AS t2
#               WHERE t2."IMOBILIZADO+SUBITEM" = CIAP_CONSOLIDADO."IMOBILIZADO+SUBITEM"
#             ) > 1 THEN 'Repetido em ambos'
#             ELSE 'Não'
#           END;
#     """)
#
#     conexao.commit()
#     cursor.close()
def criar_colunas_adicionais():
    conexao = sqlite3.connect('ciap.db')
    cursor = conexao.cursor()
    cursor.execute("""ALTER TABLE CIAP_CONSOLIDADO
                            ADD COLUMN ANO TEXT; """)
    cursor.execute("""ALTER TABLE CIAP_CONSOLIDADO 
                            ADD COLUMN N_IMOBILIZADO_FISCAL VARCHAR(50);""")
    cursor.execute("""ALTER TABLE CIAP_CONSOLIDADO
                            ADD COLUMN STATUS_IMOBILIZADO TEXT""")
    cursor.execute("""ALTER TABLE CIAP_CONSOLIDADO
                            ADD COLUMN NUMERO_PARCELA TEXT""")
    cursor.execute("""alter table CIAP_CONSOLIDADO
                    add column TIPO_IMOBILIZADO_SPED""")
def preencher_colunas_adicionais():
    conexao = sqlite3.connect('ciap.db')
    cursor = conexao.cursor()
    cursor.execute("""UPDATE ciap_consolidado
                        SET status_imobilizado = 
                    CASE 
                WHEN SUBSTR(classe, 1, 5) IN ('41000', '42000', '43000', '44000', '46000', '47000', '48000', '49000') 
                THEN 'BEM EM ANDAMENTO'
                ELSE 'BEM DEFINITIVO'
        END;""")
    cursor.execute("""UPDATE CIAP_CONSOLIDADO
                    SET NUMERO_PARCELA = 1""")
    cursor.execute("""UPDATE CIAP_CONSOLIDADO
                        SET TIPO_IMOBILIZADO_SPED = 
                        CASE WHEN NUMERO_PARCELA = 1 AND STATUS_IMOBILIZADO = "BEM DEFINITIVO"
                        THEN "IM"
                        WHEN NUMERO_PARCELA = 1 AND STATUS_IMOBILIZADO = "BEM EM ANDAMENTO"
                        THEN "IA"
                        END;""")
    cursor.execute("""UPDATE CIAP_CONSOLIDADO
    SET N_IMOBILIZADO_FISCAL = CASE
    WHEN TIPO_IMOBILIZADO_SPED = 'IA' THEN
        IMOBILIZADO || "A" || DOCNUM || NUM_ITEM
    ELSE N_IMOBILIZADO_FISCAL
    END;""")
    cursor.execute("""UPDATE CIAP_CONSOLIDADO
                    SET ANO = strftime('%Y', "DATA_LANCAMENTO")""")
    conexao.commit()
def criar_tabela_temp():
    conexao = sqlite3.connect('ciap.db')
    cursor = conexao.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS temp_transf AS SELECT NF,DOCNUM,ciap_s4hana.EMPRESA,LOC_NEG,	"Parceiro"	AS	COD_PART,	
                    "Nº CNPJ"	AS	CNPJ_PART,	"Nº CPF"	AS	CPF_PART,DATA_LANCAMENTO,NUM_ITEM,	
                    planilha_transferencias_baixas.MATERIAL,	"Texto breve material"	AS	DESCRICAO_MATERIAL,	"NCM"	AS	NCM,	"CFOP"	AS	CFOP,	
                    "Qdt. Un. Med. Básica"	AS	QTD,	"Un. Med. Básica"	AS	UND_MEDIDA,	"Valor Total"	AS	VLR_TOTAL,	"Valor Produtos"	AS	VLR_PRODUTOS,	
                    "Valor ICMS"	AS	VLR_ICMS,	"IVA"	AS	IVA,	"Item Pedido de Compra"	AS	ITEM_PEDIDO,	"Pedido de Compra"	AS	PEDIDO,
                    "Doc. MIRO"	AS	DOC_MIRO,	"Doc.referência"	AS	DOC_REF,	"Conta Contábil Pedido"	AS	CC_PEDIDO,	"Descrição da Conta"	AS	DESCRICAO_CC,	
                    "Chave de Acesso"	AS	CHV_NFE_CTE,	"Dt.iníc.depreciação"	AS	DT_INICIO_DEPRECIACAO,TP_MOVIMENTO,	
                    SUB_ITEM,	ciap_s4hana."Imobilizado"	AS	IMOBILIZADO,	"Nº do imobilizado"	AS	"IMOBILIZADO+SUBITEM",	"Centro custo ativo"	AS	CENTRO_CUSTO,	
                    "Classe imobilizado"	AS	CLASSE,	"Determ.contas"	AS	DETERM_CONTAS,	"Vida útil planejada"	AS	VIDA_UTIL_PLANEJADA,	
                    "Transação CAP"	AS	TRANS_CAP,	"Ajuste do valor"	AS	AJ_VALOR,	"Ano de aquisição"	AS	ANO_aquisicao,	ciap_s4hana."Atribuição"	AS	ATRIBUICAO,	
                    "Baixa"	AS	BAIXA,	"Chave de depreciação"	AS	CHV_DEPRECIACAO,	"Ctg.tipo movimento"	AS	CTG_TIPO_MOV,	"Data da criação"	AS	DT_CRIACAO,	
                    "Data de referência"	AS	DT_REFERENCIA,	"Depreciação baixa"	AS	DEPRECIACAO_BAIXA,	"Dt.lnçmto.cont."	AS	DT_LANÇAMENTO_CONTABIL,
                    "Elemento PEP"	AS	ELEMENTO_PEP,	"Referência"	AS	REFERENCIA,	ciap_s4hana."Período contábil"	AS	PERIODO_CONTABIL,	"Mont.moeda empresa"	AS	MONTANTE,	
                    "Depreciação normal"	AS	DEPRECIACAO_NORMAL FROM entradas_fiscais
                    INNER JOIN planilha_transferencias_baixas ON entradas_fiscais."Nota Fiscal" = planilha_transferencias_baixas."NF"
                           AND entradas_fiscais."Material" = planilha_transferencias_baixas."MATERIAL" 
                           AND entradas_fiscais."Item NF" = planilha_transferencias_baixas."NUM_ITEM"
					INNER JOIN ciap_s4hana ON planilha_transferencias_baixas."Imobilizado" = ciap_s4hana."Imobilizado"
                           AND planilha_transferencias_baixas."sub_item" = ciap_s4hana.'Subnº'""")
def juntar_tabelas():
    conexao = sqlite3.connect('ciap.db')
    cursor = conexao.cursor()
    cursor.execute("""INSERT INTO ciap_consolidado
                    SELECT * FROM temp_transf""")
    cursor.execute("""drop table temp_transf""")
    conexao.commit()
def criar_ci():
    conexao = sqlite3.connect('ciap.db')
    cursor = conexao.cursor()

    cursor.execute('''CREATE TABLE criar_ci AS
                    SELECT *
                    FROM carga_legado
                    INNER JOIN anla ON anla."imob.origem" = carga_legado.imobilizado''')

    cursor.execute('''DELETE FROM anla
                        WHERE "imob.origem" IN (
                            SELECT "imobilizado" FROM carga_legado);''')


    conexao.commit()
    conexao.close()

@admin.route('/admin/criar_relatorio_diferencas', methods=['GET', 'POST'])
def criar_relatorio_diferencas():
    if request.method == 'POST':
        if 'criar-relatorio-diferencas' in request.form:
            conexao = sqlite3.connect('ciap.db')
            cursor = conexao.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notas_sem_ciap AS
                SELECT *
                FROM entradas_fiscais
                WHERE ("Nº Documento", material) NOT IN (
                    SELECT docnum, material
                    FROM ciap_consolidado
                );
            """)
            conexao.commit()
            conexao.close()
            criar_colunas_notas_sem_ciap()
            preencher_colunas_notas_sem_ciap()
            return render_template('admin.html', message_relatorio_diferencas='Função Executada com Sucesso')
    return render_template('admin.html', message_relatorio_diferencas='Erro na Função')
def criar_colunas_notas_sem_ciap():
    conexao = sqlite3.connect('ciap.db')
    cursor = conexao.cursor()
    try:
        cursor.execute("""ALTER TABLE notas_sem_ciap
                        ADD COLUMN LOC_NEG TEXT""")
        cursor.execute("""ALTER TABLE notas_sem_ciap
                        ADD COLUMN PERIODO_CONTABIL TEXT""")
        cursor.execute("""ALTER TABLE notas_sem_ciap
                        ADD COLUMN ANO TEXT""")
    except:
            pass
def preencher_colunas_notas_sem_ciap():
    conexao = sqlite3.connect('ciap.db')
    cursor = conexao.cursor()
    cursor.execute("""UPDATE notas_sem_ciap
                    SET LOC_NEG = 'Local de Negócio'""")
    cursor.execute("""UPDATE notas_sem_ciap
                    SET PERIODO_CONTABIL = strftime('%m', "Data de Lançamento")*1""")
    cursor.execute("""UPDATE notas_sem_ciap
                    SET ANO = strftime('%Y', "Data de Lançamento")""")

@admin.route('/admin/excluir_dados_mes', methods=['GET','POST'])
def excluir_dados_do_mes():
    # Verificar se o botão "excluir_dados_do_mes" foi clicado
    if request.method == 'POST':
        if 'excluir_dados_do_mes' in request.form:
            try:
                # Conectar ao banco de dados
                conn = sqlite3.connect('ciap.db')
                cursor = conn.cursor()

                # Obter o mês e o ano correntes
                now = datetime.datetime.now()
                mes_corrente = now.month
                ano_corrente = now.year

                # Excluir os dados da tabela ciap_consolidado
                cursor.execute("""
                    DELETE FROM ciap_consolidado
                    WHERE periodo_contabil = ? AND ano = ?
                """, (mes_corrente, ano_corrente))

                # Excluir os dados da tabela anek
                cursor.execute("""
                    DELETE FROM anek
                    WHERE `Período Contábil` = ? AND Ano = ?
                """, (mes_corrente, ano_corrente))

                # Commit das alterações e fechar a conexão
                conn.commit()
                conn.close()

                # Mensagem de sucesso
                message = "Dados do mês excluídos com sucesso!"
                return render_template('admin.html', message_excluir_movimento=message)
            except Exception as e:
                # Em caso de erro, exibir mensagem de erro
                message = "Ocorreu um erro ao excluir os dados do mês: " + str(e)
                return render_template('sua_template.html', message_excluir_movimento=message)
        else:
            return render_template('index.html')

@admin.route('/admin/atualizar_historico_ciap', methods=['GET', 'POST'])
def atualizar_historico_ciap():
    conexao = sqlite3.connect('ciap.db')
    cursor = conexao.cursor()
    if request.method == 'POST':
        if 'atualizar-historico-ciap' in request.form:
            cursor.execute("""CREATE TABLE IF NOT EXISTS criar_ba AS
                            SELECT * FROM carga_legado WHERE 0;""")
            cursor.execute("""INSERT INTO criar_ba
                            SELECT * FROM carga_legado WHERE numero_parcela = 48;""")
            cursor.execute("""DELETE FROM carga_legado WHERE numero_parcela = 48;""")
            cursor.execute("""DELETE FROM criar_ba WHERE numero_parcela > 48;""")
            cursor.execute("""UPDATE CARGA_LEGADO SET numero_parcela = numero_parcela + 1;""")
            cursor.execute("""UPDATE CARGA_LEGADO SET tipo_imobilizado_sped = 'SI' WHERE tipo_imobilizado_sped <> 'si';""")
            cursor.execute("""DELETE FROM carga_legado
                                WHERE imobilizado IN (
                                    SELECT imobilizado
                                    FROM planilha_transferencias_baixas
                                    WHERE tp_movimento BETWEEN 200 AND 299
                                )
                                AND sub_item IN (
                                    SELECT sub_item
                                    FROM planilha_transferencias_baixas
                                    WHERE tp_movimento BETWEEN 200 AND 299
                                );""")
            cursor.execute("""UPDATE criar_ba SET tipo_imobilizado_sped = 'BA' WHERE tipo_imobilizado_sped <> 'BA';""")
            conexao.commit()
            return render_template('admin.html', message_atualizar_historico_ciap='Função Executada com Sucesso')
    return render_template('admin.html', message_atualizar_historico_ciap='Erro na Função')

@admin.route('/admin/consistir_dados_mes', methods=['GET', 'POST'])
def consistir_dados_mes():
    conexao = sqlite3.connect('ciap.db')
    cursor = conexao.cursor()
    if request.method == 'POST':
        if 'consistir_dados_mes' in request.form:
            cursor.execute("""INSERT INTO carga_legado
                    SELECT * FROM ciap_consolidado""")

            conexao.commit()
            return render_template('admin.html', message_funcao_consistir_dados_mes='Função Executada com Sucesso')
    return render_template('admin.html', message_funcao_consistir_dados_mes='Erro na Função')







#criar modulo para conciliação e modulo para fechamento
#fazer validações fiscais nos relatorios
#alterar localização do BD
#criar tabela de diferença inversa
#adicionar diferença inversa à exportação do usuario como nova aba

#consistir dados do mes
#  excluir anek (criar historico)
#  excluir padrão (criar historico)
#  excluir ciap consolidado













