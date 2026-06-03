import os
import faiss
import pickle
import numpy as np

class FaissStore:
    
    def __init__(self, dim=768, use_existing_data=False, embeddings_paths={}):

        self.index_file_path = embeddings_paths["index_file_path"]
        self.chunks_file_path = embeddings_paths["chunks_file_path"]
        self.knowledge_base_path = embeddings_paths["knowledge_base_path"]

        os.makedirs(os.path.dirname(self.index_file_path),     exist_ok=True)
        os.makedirs(os.path.dirname(self.chunks_file_path),    exist_ok=True)
        os.makedirs(os.path.dirname(self.knowledge_base_path), exist_ok=True)

        self.index = None
        self.chunk_metadata = None
        self.chunks = None
        
        if not use_existing_data:
            for path in [self.index_file_path, self.chunks_file_path, self.knowledge_base_path]:
                if os.path.exists(path):
                    os.remove(path)
                    
            self.index = faiss.IndexFlatIP(dim)
            self.chunk_metadata = []
            self.chunks = {}

        else:
            self.index = faiss.read_index(self.index_file_path)
            with open(self.knowledge_base_path, "rb") as file:
                self.chunk_metadata = list(pickle.load(file))

            with open(self.chunks_file_path, "rb") as file:
                self.chunks = dict(pickle.load(file))

    
    def add_chunks(self, chunks, embeddings):
        embeddings = embeddings.astype(np.float32)
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)

        for chunk_info in chunks:
            self.chunk_metadata.append(
                (chunk_info.document_id, chunk_info.chunk_id)
            )

        self.save(chunks)


    def save(self, chunks):
        faiss.write_index(self.index, self.index_file_path)
        with open(self.knowledge_base_path, 'wb') as file:
            pickle.dump(self.chunk_metadata, file)

        updated_chunks = {}
        for chunk in chunks:
            updated_chunks.update({
                (chunk.document_id, chunk.chunk_id): {
                    "document_path": chunk.document_path, 
                    "start_page": chunk.start_page, 
                    "end_page": chunk.end_page, 
                    "text": chunk.text
                }
            })

        self.chunks.update(updated_chunks)
        with open(self.chunks_file_path, 'wb') as file:
            pickle.dump(self.chunks, file)

    
    def search(self, query_embedding, top_k=5):
        
        query_embedding = query_embedding.reshape(1, -1).astype(np.float32)
        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            results.append({
                "score": float(score),
                "chunk": self.chunk_metadata[idx]
                })

        return results