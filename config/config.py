config = {
    "documents": [
    "data/uploads/2017_attention_is_all_you_need_Paper.pdf", 
    "data/uploads/NEURAL_MACHINE_TRANSLATION.pdf"
    ],

    "retrieval_evaluation_data_path": "../data/evaluation/retrieval/research_paper_data.json",

    "chunk_size": 500, 
    "overlap": 50,

    "use_existing_data": True,
    
    "embeddings_data": {
        "index_file_path": "../data/indexes/enterprise_rag.index",
        "chunks_file_path": "../data/metadata/chunks.pkl",
        "knowledge_base_path": "../data/metadata/knowledge_base.pkl"
    },

    "llm_model" :"qwen2.5:3b",
    "embedding_model_path": "../models/embeddings/bge-base-en-v1.5",

    "top_k": 5,
    "retriever_type": "hybrid",

    "conversation_max_history": 5,

    "enable_query_rewriting": True
}   