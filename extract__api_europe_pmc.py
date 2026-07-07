import os
import json
import logging
from pathlib import Path
import requests
import pandas as pd

#  Criação das Pastas 
PASTA_RAIZ = Path(__file__).resolve().parent
PASTA_RAW = PASTA_RAIZ / "data_europe_pmc" / "raw_europe_pmc"
PASTA_LOGS = PASTA_RAIZ / "logs" / "rpa_europe_pmc"
for pasta in [PASTA_RAW, PASTA_LOGS]:
    pasta.mkdir(parents=True, exist_ok=True)
    
# Criação do Logging    
logging.basicConfig(
    filename=PASTA_LOGS / "extract_publications.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)    

def consultar_api_europe_pmc(termo_busca, max_resultados=10):
    """Consulta a API do Europe PMC e retorna a lista de artigos encontrados."""
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=p53"
    
    parametros = {
        "query": termo_busca,
        "format": "xml",
        "pageSize": max_resultados
    }
    
    logging.info(f"Iniciando consulta na API para o termo: '{termo_busca}'")
    try:
        resposta = requests.get(url, params=parametros, timeout=20)
        resposta.raise_for_status() # Dispara erro se a requisição falhar (ex: erro 404, 500)
        
        dados_json = resposta.json()
        
        # O Europe PMC coloca a lista de artigos dentro de: resultList -> result
        artigos = dados_json.get("resultList", {}).get("result", [])
        logging.info(f"Consulta concluída. Encontrados {len(artigos)} artigos.")
        
        return dados_json, artigos
    except Exception as e:
            logging.error(f"Falha na requisição da API: {e}")
            raise 
        
        
#Utilizar pandas para fazer do dataframe conitec_raw.csv, assim filtrando os temas mais utilizados, para usar na como termos de pesquisa na API do Europe PMC.