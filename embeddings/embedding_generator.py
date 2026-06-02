import numpy as np
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer

@dataclass
class Chunk:
    chunk_id: int

    document_id: int
    document_path: str
    
    start_page: int
    end_page: int
    
    text: str
    
@dataclass
class EmbeddedChunk:
    chunk: Chunk
    embedding: np.ndarray



class EmbeddingService:

    def __init__(self, llm_model_path):

        self.embedding_model = SentenceTransformer(
            llm_model_path
        )

    def embed_documents(self, chunks):

        texts = [chunk.text for chunk in chunks]

        embeddings = self.embedding_model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        return embeddings
    

    def embed_query(self, query):

        query = (
            "Represent this sentence for searching relevant passages: "
            + query
        )

        embedding = self.embedding_model.encode(
            query,
            convert_to_numpy=True
        )

        return embedding