RPA Conitec - Extração de Tecnologias Demandadas: 

Repositório contém um robô de automação (RPA) desenvolvido em Python para acessar o portal da **Conitec (Comissão Nacional de Incorporação de Tecnologias no Sistema Único de Saúde)**, baixar a planilha de dados contendo as tecnologias demandadas e convertê-la para o formato CSV.

 Objetivo do RPA:

No site da Conitec vai disponibilizar um painel de tecnologias sob avaliação ou já avaliadas em formato Excel (`.xlsx`). O robô realiza os seguintes passos:
1. **Navegação**: Acessa a página principal de tecnologias demandadas.
2. **Localização**: Identifica dinamicamente o link Plone de redirecionamento (`resolveuid`) correspondente ao arquivo Excel, no qual é um encurtador de links inteligente, pegando sempre o link mais recente
3. **Navegação de Detalhes & Download**: Acessa o link de redirecionamento, abrindo a página de visualização do arquivo, localiza o link real de download da planilha (`@@download/file`) e dispara o clique nativo do Chrome para salvar o arquivo Excel na pasta raw.
4. **Conversão**: Processa a planilha baixada usando o "pandas" e gera uma versão limpa no formato CSV (`conitec_raw.csv`) com codificação `UTF-8`.
5. **Geração de Logs**: Registra de forma detalhada o progresso, avisos e eventuais falhas durante a execução, tanto no console quanto no arquivo de log local.

=======================================================

Estrutura de Diretórios Gerada

O script resolve e cria a seguinte estrutura:

inova_trial_ai/
│
├── data_conitec/
│   └── raw_conitec/
│       ├── Painel_Demandas_Conitec_YYYYMMDD.xlsx  # Arquivo Excel original baixado
│       └── conitec_raw.csv                        # Arquivo CSV final convertido
│
├── logs/
│   └── rpa_conitec/
│       └── rpa_conitec.log                        # Histórico de logs de execução do robô
│
└── extract_publications.py                        # Script principal do RPA

=====================================================
 Pré-requisitos e Dependências

Para rodar este script, você precisará do **Python 3.8+** instalado. As dependências necessárias estão descritas abaixo:

- **selenium**: Usado para controle e extração dinâmica de elementos da página.
- **webdriver-manager**: Para gerenciamento automático da instalação do driver do Google Chrome.
- **pandas** & **openpyxl**: Carregar e converter o arquivo Excel (`.xlsx`) em CSV.
- **pathlib**: Utilizada para gerenciar e manipular caminhos de arquivos e pastas utilizando orientação a objetos.

=====================================================
Como instalar as dependências

Se o seu ambiente virtual (`.venv`) já estiver configurado, as dependências já estarão presentes. Caso precise instalar manualmente no seu ambiente:

pip install -r requirements.txt


===============

Como Executar o Script

Executar terminal apontado para a pasta raiz do projeto, execute o comando abaixo utilizando o interpretador do seu ambiente virtual:

powershell
.venv\Scripts\python extract_publications.py

