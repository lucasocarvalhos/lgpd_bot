import uuid
import json

class LGPDChunking:
    def __init__(self, input_path : str = "data/processed/lgpd_processed.json", output_path : str ="data/processed/lgpd_chunks.json", max_chars=1000):
        self.input_path = input_path
        self.output_path = output_path
        self.max_chars = max_chars
        self.chunks = []

    def aplica_chunking(self):
        with open(self.input_path, "r", encoding="utf-8") as file:
            artigos = json.load(file)

        current_chunk = ""
        metadata = ""

        for artigo in artigos:
            titulo = artigo["titulo"]
            conteudo = artigo["conteudo"]

            artigo_texto = f"{titulo}\n{conteudo}"

            if len(current_chunk) + len(artigo_texto) <= self.max_chars:
                current_chunk += f"\n\n{artigo_texto}"
                metadata += f"\n{titulo}"
            else:
                self.chunks.append({
                    "id": str(uuid.uuid4()),
                    "text": current_chunk.strip(),
                    "metadata": metadata.strip()
                })
                current_chunk = f"{artigo_texto}"
                metadata = titulo

        if current_chunk:
            self.chunks.append({
                "id": str(uuid.uuid4()),
                "text": current_chunk.strip(),
                "metadata": metadata.strip()
            })

    def salva_chunking(self):
        with open(self.output_path, "w", encoding="utf-8") as file:
            json.dump(self.chunks, file, ensure_ascii=False, indent=2)

    def execute(self):
        self.aplica_chunking()
        self.salva_chunking()
        
        return True