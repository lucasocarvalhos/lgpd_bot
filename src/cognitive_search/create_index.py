import os
from dotenv import load_dotenv
import requests

class CreateIndex:
    def __init__(self, index_name=None):
        load_dotenv()
        
        self.search_service_name = os.environ.get("AZURE_SEARCH_SERVICE_NAME")
        self.api_key = os.environ.get("AZURE_SEARCH_API_KEY")
        self.index_name = index_name or os.environ.get("AZURE_SEARCH_INDEX_NAME")
        
        self.url = f"https://{self.search_service_name}.search.windows.net/indexes/{self.index_name}?api-version=2023-07-01-Preview"
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        
        self.index_schema = {
            "name": self.index_name,
            "fields": [
                { 
                    "name": "id", 
                    "type": "Edm.String", 
                    "key": True, 
                    "filterable": False, 
                    "sortable": False, 
                    "facetable": False 
                },
                { 
                    "name": "conteudo", 
                    "type": "Edm.String", 
                    "searchable": True, 
                    "filterable": False, 
                    "sortable": False, 
                    "facetable": False 
                },
                { 
                    "name": "metadata_title", 
                    "type": "Edm.String", 
                    "searchable": True, 
                    "filterable": False, 
                    "sortable": False, 
                    "facetable": False 
                }
            ]
        }
    
    def create_index(self):
        """Cria o índice no Azure Search"""
        response = requests.put(self.url, headers=self.headers, json=self.index_schema)
        
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        
        return True