import os

from sentence_transformers import SentenceTransformer
from sentence_transformers.cross_encoder import CrossEncoder


def create_directories():
    os.makedirs("models/embeddings", exist_ok=True)
    os.makedirs("models/rerankers", exist_ok=True)


def model_exists(model_path):
    return os.path.exists(
        os.path.join(model_path, "config.json")
    )


def download_embedding_model():

    model_name = "BAAI/bge-base-en-v1.5"
    save_path = "models/embeddings/bge-base-en-v1.5"

    if model_exists(save_path):
        print(f"Embedding model already exists: {save_path}")
        return

    print(f"Downloading {model_name}...")

    model = SentenceTransformer(model_name)
    model.save(save_path)

    print(f"Saved embedding model to {save_path}")


def download_reranker_models():

    rerankers = [
        (
            "cross-encoder/ms-marco-MiniLM-L-6-v2",
            "models/rerankers/ms-marco-MiniLM-L-6-v2"
        ),
        (
            "BAAI/bge-reranker-base",
            "models/rerankers/bge-reranker-base"
        )
    ]

    for model_name, save_path in rerankers:

        if model_exists(save_path):
            print(f"Reranker already exists: {save_path}")
            continue

        print(f"Downloading {model_name}...")

        model = CrossEncoder(model_name)
        model.save(save_path)

        print(f"Saved to {save_path}")


def download_prerequisites():

    create_directories()
    download_embedding_model()
    download_reranker_models()

    print("\nSetup completed successfully.")