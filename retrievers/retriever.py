class Retriever:

    def __init__(self, embedding_service, vector_store, top_k=3):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.top_k = top_k


    def get_new_chunks(self, chunk, avalaible_chunks):
        new_chunks = []
        doc_id = chunk[0]
        chunk_id = chunk[1]

        for offset in [-1, 1]:
            key = (doc_id, chunk_id + offset)

            if key in avalaible_chunks:
                new_chunks.append(key)
                
        return new_chunks

    def retrieve(self, query):
        query_embedding = self.embedding_service.embed_query(query)

        results = self.vector_store.search(
            query_embedding,
            self.top_k
        )

        chunks = [res["chunk"] for res in results]

        new_chunks = []
        avalaible_chunks = self.vector_store.chunks.keys()
        
        for chunk in chunks:
            new_chunks.extend(
                self.get_new_chunks(chunk, avalaible_chunks)
            )

        seen = set()
        unique_chunks = []

        for chunk in chunks + new_chunks:
            if chunk not in seen:
                seen.add(chunk)
                unique_chunks.append(chunk)

        chunks = unique_chunks
        chunks.sort(
            key=lambda x: (x[0], x[1])
        )

        final_results = []
        for chunk in chunks:

            final_results.append(
                self.vector_store.chunks[chunk]
            )
            
        return final_results