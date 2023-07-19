from flask import Blueprint

sped = Blueprint('sped', __name__)

@sped.route('/sped/importacao-relatorio', methods=['POST'])
def importacao_relatorio():
    # Lógica para importação de relatório do módulo Sped
    return 'Importação de Relatório do Sped'

@sped.route('/sped/importacao-sped', methods=['POST'])
def importacao_sped():
    # Lógica para importação de arquivo Sped do módulo Sped
    return 'Importação do Sped'

@sped.route('/sped/geracao-sped')
def geracao_sped():
    # Lógica para geração do arquivo Sped do módulo Sped
    return 'Geração do Sped'
