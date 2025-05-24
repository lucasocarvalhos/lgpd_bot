import os 
from dotenv import load_dotenv
import openai
from chatbot.search_client import AzureSearchClient

load_dotenv()

class LGPDChatBot:
    def __init__(self):
        self.search_client = AzureSearchClient()
        openai.api_key = os.environ.get("AZURE_OPENAI_KEY")
        openai.api_base = os.environ.get("AZURE_OPENAI_ENDPOINT")
        openai.api_type = "azure"
        openai.api_version = "2023-07-01-preview"
        self.deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT")

    def ask(self, question):
        documents = self.search_client.search(question)
        context = "\n\n".join(documents)

        messages = [
            {
                "role": "system",
                "content": """
                    Você é um assistente especialista na Lei Geral de Proteção de Dados (LGPD). 
                    Responda à pergunta do usuário baseando-se ESTRITAMENTE e SOMENTE no contexto fornecido.
                    Não utilize nenhum conhecimento prévio que você possua sobre a LGPD  
                    Não forneça informações que não estejam diretamente relacionadas à LGPD.
                    """
            },
            {
                "role": "user",
                "content": f"Contexto da lei:\n{context}\n\nPergunta: {question}"
            }
        ]

        response = openai.chat.completions.create(
            model=self.deployment_name,
            messages=messages,
            temperature=0.2,
            max_tokens=2032
        )

        return response.choices[0].message.content
