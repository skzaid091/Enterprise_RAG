from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self, model_path, top_k=5):

        self.model = CrossEncoder(model_path)
        self.top_k = top_k


    def rerank(self, query, results):

        pairs = [
            (query, result["text"])
            for result in results
        ]

        scores = self.model.predict(pairs)

        ranked_results = sorted(
            zip(scores, results),
            key=lambda x: x[0],
            reverse=True
        )

        return [
            result
            for _, result
            in ranked_results[:self.top_k]
        ]