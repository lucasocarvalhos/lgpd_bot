import os
from dotenv import load_dotenv
import json
import requests
from time import sleep

class ChunkIndexing:
    def __init__(self, json_path="data/processed/lgpd_chunks.json", batch_size=100):
        load_dotenv()
        
        self.search_service_name = os.environ.get("AZURE_SEARCH_SERVICE_NAME")
        self.api_key = os.environ.get("AZURE_SEARCH_API_KEY")
        self.index_name = os.environ.get("AZURE_SEARCH_INDEX_NAME")
        self.json_path = json_path
        self.batch_size = batch_size
        
        # Configurar URL e headers
        self.url = f"https://{self.search_service_name}.search.windows.net/indexes/{self.index_name}/docs/index?api-version=2023-07-01-Preview"
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        
    def load_chunks(self):
        """Carrega os chunks do arquivo JSON"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.chunks = json.load(f)
        print(f"{len(self.chunks)} chunks carregados para indexação...")
        return self.chunks
    
    def prepare_batch(self, batch):
        """Prepara um lote de documentos para indexação"""
        return [
            {
                "@search.action": "upload",
                "id": doc["id"],
                "conteudo": doc["text"],
                "metadata_title": doc["metadata"]
            }
            for doc in batch
        ]
    
    def index_chunks(self):
        """Indexa os chunks em lotes no Azure Search"""
        if not hasattr(self, 'chunks'):
            self.load_chunks()
            
        for i in range(0, len(self.chunks), self.batch_size):
            batch = self.chunks[i:i+self.batch_size]
            actions = self.prepare_batch(batch)
            payload = {"value": actions}
            
            response = requests.post(self.url, headers=self.headers, json=payload)
            
            print(f"Lote {i//self.batch_size + 1}: Status {response.status_code}")
            if response.status_code >= 400:
                print("Erro:", response.text)
                break
            else:
                print("OK")
            
            sleep(0.5)  # Evitar throttling
            
        return response.status_code 