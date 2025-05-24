from create_index import CreateIndex
from chunk_indexing import ChunkIndexing


if __name__ == "__main__":
    create_index = CreateIndex()
    if create_index.create_index():
        print("Índice criado com sucesso no Azure Cognitive Search!")
    else:
        print("Falha na criação dos índices no Azure Cognitive Search.")

    chunk_indexing = ChunkIndexing()
    if chunk_indexing.index_chunks():
        print("Índices populados com os chunks com sucesso no Azure Cognitive Sarch!")
    else:
        print("Falha na população dos índices com os chunks no Azure Cognitive Search.")