import os
import requests 
from requests.exceptions import RequestException

class LGPDDataCollector:
    """
    Classe especializada para coleta do texto da Lei Geral de Proteção de Dados (LGPD) do Brasil.

    Atributos:
        url (str): URL do site onde a LGPD está disponível.
        output_dir (str): Diretório onde o arquivo de texto será salvo.
    """

    def __init__(self, output_dir: str = "data/raw"):
        self.url = "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm"

    def fetch_url(self):
        """
        Coleta o conteúdo da URL especificada.

        Retorna:
            str: Conteúdo HTML da página.
        """
        try:
            print("Acessando a URL...")
                    
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            response = requests.get(self.url, headers=headers, timeout=5)
            response.raise_for_status()

            return response.text
        
        except RequestException as e:
            print(f"Erro ao acessar a URL: {e}")
            return None
        
    def save_raw_html(self, html_content: str, filename: str = "lgpd_raw.html"):
        """
        Salva o conteúdo HTML em um arquivo.

        Parâmetros:
            html_content (str): Conteúdo HTML a ser salvo.
            filename (str): Nome do arquivo onde o conteúdo será salvo.
        """

        if not html_content:
            print("Nenhum conteúdo HTML para salvar.")
            return False
        
        try:
            os.makedirs("data/raw", exist_ok=True)
            
            with open(f"data/raw/{filename}", "w", encoding="utf-8") as file:
                file.write(html_content)
            return True
        
        except IOError as e:
            print(f"Erro ao salvar o arquivo: {e}")
            return False

    def execute(self) -> bool:
        """
        Executa o processo de coleta e salvamento do conteúdo da LGPD.

        Retorna:
            bool: True se o processo for bem-sucedido, False caso contrário.
        """

        html_content = self.fetch_url()
        
        if not html_content:
            return False
        
        return self.save_raw_html(html_content)