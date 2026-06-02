import os
import subprocess

from sentence_transformers import SentenceTransformer, CrossEncoder


MODELS = {
    "embeddings": [
        (
            "BAAI/bge-base-en-v1.5",
            "../models/embeddings/bge-base-en-v1.5"
        )
    ],

    "rerankers": [
        (
            "cross-encoder/ms-marco-MiniLM-L-6-v2",
            "../models/rerankers/ms-marco-MiniLM-L-6-v2"
        ),
        (
            "BAAI/bge-reranker-base",
            "../models/rerankers/bge-reranker-base"
        )
    ],

    "llms": [
        "qwen2.5:3b"
    ]
}


def download_embedding_models():

    for model_name, save_path in MODELS["embeddings"]:

        if os.path.exists(save_path):
            print(f"Skipping {model_name}")
            continue

        print(f"Downloading {model_name}")

        model = SentenceTransformer(model_name)

        model.save(save_path)

        print(f"Saved -> {save_path}\n")


def download_reranker_models():

    for model_name, save_path in MODELS["rerankers"]:

        if os.path.exists(save_path):
            print(f"Skipping {model_name}")
            continue

        print(f"Downloading {model_name}")

        model = CrossEncoder(model_name)

        model.save(save_path)

        print(f"Saved -> {save_path}\n")


def download_llms():

    for model_name in MODELS["llms"]:

        print(f"Pulling {model_name}")

        subprocess.run(
            ["ollama", "pull", model_name],
            check=True
        )

        print(f"Downloaded -> {model_name}\n")


if __name__ == "__main__":

    download_embedding_models()

    download_reranker_models()

    download_llms()

    print("All models downloaded successfully.")