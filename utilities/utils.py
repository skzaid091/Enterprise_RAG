import json
from tqdm import tqdm

def retrieval_evaluator(rag, evaluation_data_path, retriever_type):

    if retriever_type == "faiss":
        active_retriever = rag.retrieve_with_faiss

    elif retriever_type == "bm25":
        active_retriever = rag.retrieve_with_bm25

    elif retriever_type == "hybrid":
        active_retriever = rag.retrieve_with_hybrid

    with open(evaluation_data_path, "r") as file:
        evaluation_dataset = json.load(file)

    avg_score = 0
    for sample in evaluation_dataset:

        context, _ = active_retriever(sample["question"])
        
        score = answer_recall_score(context, sample["expected_keywords"])
        avg_score += score

    print("AVERAGE RETRIEVAL SCORE - ", avg_score / len(evaluation_dataset))


def answer_recall_score(answer, expected_keywords):
    answer = answer.lower()

    matched_keywords = []
    for keyword in expected_keywords:

        if keyword.lower() in answer:
            matched_keywords.append(keyword)

    score = len(matched_keywords) / len(expected_keywords)

    return round(score, 2)


def answer_evaluator(rag, evaluation_data_path):
    with open(evaluation_data_path, "r") as file:
        evaluation_dataset = json.load(file)
    
    avg_score = 0
    for sample in tqdm(evaluation_dataset, desc="Evaluating Answers",  unit="question"):
        response = rag.ask(
            (sample["question"]), 
            hide_auto_regressive_output=True
        )

        answer = response["answer"]
        score = answer_recall_score(
            answer,
            sample["expected_keywords"]
        )

        avg_score += score
    
    print(
        "\nAVERAGE ANSWER SCORE - ",
        round(avg_score / len(evaluation_dataset), 4), 
        "\n"
    )