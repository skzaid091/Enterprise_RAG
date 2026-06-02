from RAG.rag import RAG
from config.config import config

rag = RAG(config=config)

answer = rag.ask("What is Self Attention in Transformer?")

print("\nANSWER : ", answer, "\n")