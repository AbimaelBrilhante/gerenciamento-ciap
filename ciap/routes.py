from flask import Blueprint, request, render_template,make_response,session
import sqlite3
import pandas as pd
from io import BytesIO
import os


ciap = Blueprint('ciap', __name__)

@ciap.route('/ciap/consulta',methods=['GET', 'POST'])
def consulta_ciap():
    if request.method == 'GET':
        if 'search' in request.args:
            local_de_negocio = request.args.get('local_de_negocio')
            periodo_mes = request.args.get('mes')
            periodo_ano = request.args.get('ano')

            # alterar local do banco de dados posteriormente
            db_path = r'C:\Users\abimaelsoares\PycharmProjects\ciap_sped\ciap.db'
            if not os.path.exists(db_path):
                return "O caminho do banco de dados não existe."
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            query = ""
            params = []

            # Verificar se pelo menos um dos parâmetros foi fornecido
            if local_de_negocio or periodo_mes or periodo_ano:
                query = "SELECT * FROM CIAP_CONSOLIDADO WHERE 1=1"
                params = []

                if local_de_negocio:
                    query += " AND LOC_NEG = ?"
                    params.append(local_de_negocio)

                if periodo_mes:
                    query += " AND PERIODO_CONTABIL = ?"
                    params.append(periodo_mes)

                if periodo_ano:
                    query += " AND ANO = ?"
                    params.append(periodo_ano)

                # Executar a consulta com os parâmetros fornecidos
                cursor.execute(query, params)

                dados = cursor.fetchall()
                cabecalho = [description[0] for description in cursor.description]

                # Armazenar os dados e cabeçalho na sessão
                session['dados'] = dados
                session['cabecalho'] = cabecalho

                # Fechar a conexão com o banco de dados
                conn.close()

                # Renderizar o template e passar os dados para exibição
                return render_template('consulta_ciap.html', dados=dados, cabecalho=cabecalho)


    return render_template('consulta_ciap.html')

@ciap.route('/ciap/export-ciap', methods=['GET'])
def export_ciap():
    # Recupere os dados e cabeçalho da sessão
    dados_ciap = session.get('dados_ciap')
    cabecalho = session.get('cabecalho')

    # Crie um DataFrame do Pandas com os dados e cabeçalho
    df = pd.DataFrame(dados_ciap, columns=cabecalho)

    # Crie um objeto BytesIO para armazenar o arquivo Excel em memória
    excel_file = BytesIO()

    # Salve o DataFrame como um arquivo Excel
    df.to_excel(excel_file, index=False)

    # Defina o cabeçalho e os cabeçalhos de resposta corretos para o arquivo Excel
    excel_file.seek(0)
    response = make_response(excel_file.getvalue())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename=ciap.xlsx'

    return response

@ciap.route('/ciap/export-notas-sem-ciap', methods=['GET'])
def export_notas_sem_ciap():
    # Recupere os parâmetros da consulta
    local_de_negocio = request.args.get('local_de_negocio')
    periodo_mes = request.args.get('mes')
    periodo_ano = request.args.get('ano')

    # Estabeleça a conexão com o banco de dados
    db_path = r'C:\Users\abimaelsoares\PycharmProjects\ciap_sped\ciap.db'
    if not os.path.exists(db_path):
        return "O caminho do banco de dados não existe."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute a consulta na tabela "notas_sem_ciap" com os parâmetros fornecidos
    query_notas_sem_ciap = "SELECT * FROM notas_sem_ciap WHERE 1=1"
    params = []

    if local_de_negocio:
        query_notas_sem_ciap += " AND LOC_NEG = ?"
        params.append(local_de_negocio)

    if periodo_mes:
        query_notas_sem_ciap += " AND PERIODO_CONTABIL = ?"
        params.append(periodo_mes)

    if periodo_ano:
        query_notas_sem_ciap += " AND ANO = ?"
        params.append(periodo_ano)

    # Execute a consulta com os parâmetros fornecidos
    cursor.execute(query_notas_sem_ciap, params)

    dados_notas_sem_ciap = cursor.fetchall()
    cabecalho = [description[0] for description in cursor.description]

    # Crie um DataFrame do Pandas com os dados e cabeçalho
    df = pd.DataFrame(dados_notas_sem_ciap, columns=cabecalho)

    # Crie um objeto BytesIO para armazenar o arquivo Excel em memória
    excel_file = BytesIO()

    # Salve o DataFrame como um arquivo Excel
    df.to_excel(excel_file, index=False)

    # Defina o cabeçalho e os cabeçalhos de resposta corretos para o arquivo Excel
    excel_file.seek(0)
    response = make_response(excel_file.getvalue())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename=notas_sem_ciap.xlsx'

    # Feche a conexão com o banco de dados
    conn.close()

    return response
