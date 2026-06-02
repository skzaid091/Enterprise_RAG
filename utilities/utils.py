def retrieval_evaluater(rag, evaluation_dataset, retriever_type):

    if retriever_type == "faiss":
        active_retriever = rag.retrieve_with_faiss

    elif retriever_type == "bm25":
        active_retriever = rag.retrieve_with_bm25

    elif retriever_type == "hybrid":
        active_retriever = rag.retrieve_with_hybrid

    avg_score = 0
    for sample in evaluation_dataset:

        results = active_retriever(sample["question"])
        
        score = score_answer(
            results["context"],
            sample["expected_keywords"]
        )


        avg_score += score["score"]

    print("AVERAGE RETRIEVAL SCORE - ", avg_score / len(evaluation_dataset))


def score_answer(answer, expected_keywords):
    answer = answer.lower()

    matched_keywords = []
    for keyword in expected_keywords:

        if keyword.lower() in answer:
            matched_keywords.append(keyword)

    score = len(matched_keywords) / len(expected_keywords)

    return {
        "score": round(score, 2),
        "matched_keywords": matched_keywords,
        "missing_keywords": [
            kw for kw in expected_keywords
            if kw not in matched_keywords
        ]
    }