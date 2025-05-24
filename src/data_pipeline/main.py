from data_collector import LGPDDataCollector
from data_processor import LGPDDataProcessor
from data_chunking import LGPDChunking

if __name__ == "__main__":
    collector = LGPDDataCollector()
    if collector.execute():
        print("Dados da LGPD coletados e salvos com sucesso!")
    else:
        print("Falha na coleta dos dados da LGPD.")

    processor = LGPDDataProcessor()
    if processor.execute():
        print("Dados da LGPD processados e salvos com sucesso!")
    else:
        print("Falha no processamento dos dados da LGPD.")

    chunking = LGPDChunking()
    if chunking.execute():
        print("Chunking de dados realizado e salvo com sucesso!")
    else:
        print("Falha no chunking dos dados da LGPD.")