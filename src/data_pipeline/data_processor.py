import re
import json
from bs4 import BeautifulSoup

class LGPDDataProcessor:
    def __init__(self, input_path : str="data/raw/lgpd_raw.html", output_path : str ="data/processed/lgpd_processed.json"):
        self.input_path = input_path
        self.output_path = output_path
        self.html_content = None
        self.clean_text = None
        self.artigos = []
    
    def seleciona_texto_html(self):
        """Lê o arquivo HTML e extrai apenas o texto relevante"""
        with open(self.input_path, "r", encoding="utf-8") as file:
            self.html_content = BeautifulSoup(file, "html.parser")
        
        for tag in self.html_content(["script", "style", "head", "footer", "meta", "noscript", "s", "strike"]):
            tag.decompose()
        
        for elem in self.html_content.find_all(style=lambda value: value and 'line-through' in value):
            elem.decompose()
        
        return self.html_content.get_text(separator="\n")
    
    def limpa_texto(self, text):
        """Realiza a limpeza do texto e extrai artigos"""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        self.clean_text = "\n".join(lines)
        
        # Extrai capítulos, seções e artigos
        pattern = re.compile(r"(CAPÍTULO [IVXLCDM]+.*?|Seção .*?|Art\. ?\d+[\-A-Za-z]*[º.]?.*?)\n", re.IGNORECASE)
        splits = pattern.split(self.clean_text)
        splits = [s.strip() for s in splits if s.strip()]
        
        # Organiza os artigos
        self.artigos = []
        for i in range(len(splits)):
            if re.match(r"Art\. ?\d+[\-A-Za-z]*[º.]?", splits[i]):
                # Pega apenas o título (Art. Xº ou Art. X.) e deixa o resto como conteúdo
                titulo_match = re.match(r"(Art\. ?\d+[\-A-Za-z]*[º.])", splits[i])
                if titulo_match:
                    artigo = {
                        "titulo": titulo_match.group(1),
                        "conteudo": splits[i][len(titulo_match.group(1)):].strip() + (" " + splits[i+1] if i+1 < len(splits) else "")
                    }
                    self.artigos.append(artigo)
        
        return self.artigos
    
    def salva_json(self):
        """Salva os artigos processados em um arquivo JSON"""
        with open(self.output_path, "w", encoding="utf-8") as file:
            json.dump(self.artigos, file, ensure_ascii=False, indent=2)
    
    def execute(self):
        """Método principal que executa todo o fluxo de processamento"""
        texto_html = self.seleciona_texto_html()
        self.limpa_texto(texto_html)
        self.salva_json()
        
        return True