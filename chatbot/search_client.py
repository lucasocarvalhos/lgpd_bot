import os 
from dotenv import load_dotenv
import requests

load_dotenv()

class AzureSearchClient:
    def __init__(self):
        self.service_name = os.environ.get("AZURE_SEARCH_SERVICE_NAME")
        self.api_key = os.environ.get("AZURE_SEARCH_API_KEY")
        self.index_name = os.environ.get("AZURE_SEARCH_INDEX_NAME")
        self.api_version = "2023-07-01-Preview"

    def search(self, query, top_k=3):
        url = f"https://{self.service_name}.search.windows.net/indexes/{self.index_name}/docs"
        params = {
            "api-version": self.api_version,
            "search": query,
            "$top": top_k
        }
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            results = response.json().get("value", [])
            return [doc["conteudo"] for doc in results]
        else:
            raise Exception(f"Erro na busca: {response.status_code} - {response.text}")
