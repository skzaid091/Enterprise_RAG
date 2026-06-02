from rank_bm25 import BM25Okapi

class BM25_Retriever:

    def __init__(self, vector_store, top_k=5):

        self.vector_store = vector_store
        self.top_k = top_k

        self.chunk_keys = []
        self.tokenized_chunks = []

        for key, chunk in self.vector_store.chunks.items():

            self.chunk_keys.append(key)

            self.tokenized_chunks.append(
                chunk["text"].lower().split()
            )

        self.bm25 = BM25Okapi(
            self.tokenized_chunks
        )


    def retrieve(self, query):
    
        tokenized_query = (
            query.lower().split()
        )
    
        scores = self.bm25.get_scores(tokenized_query)
    
        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:self.top_k]
    
        results = []
        for idx in ranked_indices:
    
            chunk_key = self.chunk_keys[idx]
            
            results.append(
                self.vector_store.chunks[
                    chunk_key
                ]
            )
    
        return results