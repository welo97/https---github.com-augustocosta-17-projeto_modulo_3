import time
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#  Criação das Pastas 
PASTA_RAIZ = Path(__file__).resolve().parent
PASTA_RAW = PASTA_RAIZ / "data_conitec" / "raw_conitec"
PASTA_LOGS = PASTA_RAIZ / "logs" / "rpa_conitec"
for pasta in [PASTA_RAW, PASTA_LOGS]:
    pasta.mkdir(parents=True, exist_ok=True)

#  Criação do Logging 
logging.basicConfig(
    filename=PASTA_LOGS / "rpa_conitec.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def criar_driver():
    """Cria driver Chrome com configuração de download automático."""
    options = Options()
    prefs = {
        "download.default_directory": str(PASTA_RAW.resolve()),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Habilita download no modo headless via CDP (Comando CDP para liberar downloads em modo oculto (headless)
    driver.execute_cdp_cmd("Page.setDownloadBehavior", {
        "behavior": "allow",
        "downloadPath": str(PASTA_RAW.resolve())
    })
    return driver

def baixar_xlsx_conitec(url, xpath_inicial):
    """Abre a página da Conitec, no qual vai navegar até a página do arquivo, fazendo o download."""
    driver = criar_driver()
    try:
        logging.info(f"Navegando até a página principal: {url}")
        driver.get(url)

        # vai fechar banner de cookies se aparecer
        try:
            botao_cookie = driver.find_element(By.XPATH, "//button[contains(text(),'Aceitar')]")
            botao_cookie.click()
            logging.info("Banner de cookies fechado.")
            time.sleep(2)
        except:
            logging.info("Nenhum banner de cookies encontrado.")

        # 1. Localizar o link de redirecionamento (resolveuid) e extrai o href
        link_inicial = driver.find_element(By.XPATH, xpath_inicial)
        url_detalhes = link_inicial.get_attribute("href")
        logging.info(f"URL de detalhes extraída: {url_detalhes}")

        # 2. Navegar para a página de detalhes do arquivo
        driver.get(url_detalhes)
        time.sleep(3)

        # 3. Localizar o link real de download (contendo @@download/file)
        xpath_download_real = "//a[contains(@href, '@@download/file')]"
        link_real = driver.find_element(By.XPATH, xpath_download_real)
        
        # 4. Dispara o clique no link de download real
        logging.info("Disparando o clique no link real de download...")
        driver.execute_script("arguments[0].click();", link_real)

        # Monitora a pasta no qual vai esperar o download ser finalizado (Tempo máximo de 30 segundos)
        logging.info("Aguardando finalização do download...")
        for _ in range(30):
            time.sleep(1)
            arquivos = list(PASTA_RAW.glob("*.xlsx"))
            temporarios = list(PASTA_RAW.glob("*.crdownload"))
            if arquivos and not temporarios:
                break

        arquivos = list(PASTA_RAW.glob("*.xlsx"))
        if not arquivos:
            raise FileNotFoundError("Nenhum arquivo Excel encontrado na pasta de download.")
        xlsx_path = arquivos[0]

        logging.info("Arquivo baixado com sucesso: %s", xlsx_path)
        return xlsx_path
    finally:
        driver.quit()

def converter_para_csv(xlsx_path): 
    """Converter o Excel baixado para CSV."""
    df = pd.read_excel(xlsx_path, engine="openpyxl")
    csv_path = PASTA_RAW / "conitec_raw.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")
    logging.info("CSV gerado em %s", csv_path)
    return csv_path

if __name__ == "__main__":
    url_conitec = "https://www.gov.br/conitec/pt-br/assuntos/avaliacao-de-tecnologias-em-saude/tecnologias-demandadas"
    
    # XPath para encontrar o link inicial de redirecionamento UID
    xpath_inicial = "//a[contains(@class, 'internal-link') and contains(@href, 'resolveuid')]"
    
    try:
        xlsx_file = baixar_xlsx_conitec(url_conitec, xpath_inicial)
        csv_file = converter_para_csv(xlsx_file)
        print("Coleta concluída com sucesso:", csv_file)
    except Exception as e:
        logging.error("Erro na coleta: %s", e)
        print("Erro:", e)
