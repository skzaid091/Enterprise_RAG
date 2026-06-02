from loaders.PDF_Loader import PDFLoader
from chunking.chunker import Chunker
from embeddings.embedding_generator import EmbeddingService
from vector_stores.vector_store import FaissStore
from retrievers.retriever import Retriever
from retrievers.bm25_retriever import BM25_Retriever
from context_building.context_builder import ContextBuilder
from llms.llm_service import LLM_Service
from memory.conversation_memory import ConversationMemory
from query_rewriting.query_rewriter import QueryRewriter
from prompts.prompt import Prompt_Generator

from utilities.utils import *


class RAG:

    def __init__(self, config=None):
        if not config:
            print("Please provide configurations.")

        if not config["use_existing_data"]:
            pdf_loader = PDFLoader()
            processed_documents = pdf_loader.load_documents(config["documents"])

            chunker = Chunker()
            chunks = chunker.get_chunks(processed_documents)
        
        self.config = config
        
        self.embedding_service = EmbeddingService(config["embedding_model_path"])
        if not config["use_existing_data"]:
            embeddings = self.embedding_service.embed_documents(chunks)

        self.vector_store = FaissStore(use_existing_data=config["use_existing_data"], embeddings_paths=config["embeddings_data"])
        if not config["use_existing_data"]:
            self.vector_store.add_chunks(chunks, embeddings)

        
        self.retriever = Retriever(self.embedding_service, self.vector_store, config["top_k"])
        self.bm25_retriever = BM25_Retriever(self.vector_store, top_k=config["top_k"])

        retriever_type = config["retriever_type"]
        if retriever_type == "faiss":
            self.active_retriever = self.retrieve_with_faiss

        elif retriever_type == "bm25":
            self.active_retriever = self.retrieve_with_bm25

        elif retriever_type == "hybrid":
            self.active_retriever = self.retrieve_with_hybrid

        self.context_builder = ContextBuilder()

        self.llm_model = LLM_Service(
            config["llm_model"]
        )

        self.memory = ConversationMemory(
            max_history=config["conversation_max_history"]
        )

        self.enable_query_rewriting = config["enable_query_rewriting"]
        self.query_rewriter = QueryRewriter(self.llm_model)

        self.prompt_generator = Prompt_Generator()
    

    def evaluate_retrieval(self):
        if not self.config.get("retrieval_evaluation_data_path"):
            print("Provide the 'retrieval_evaluation_data_path' in config.")
            return
        
        retrieval_evaluater(self, 
                            self.config["retrieval_evaluation_data_path"], 
                            self.config["retriever_type"])
        print("\nRetrieval Evaluation Completed.")


    def build_history_context(self):

        history = self.memory.get_history()

        if not history:
            return ""

        context = ""

        for item in history:

            context += (
                f"User: {item['user']}\n"
                f"Assistant: {item['assistant']}\n\n"
            )

        return context


    def build_prompt(self, query):
        
        history = None
        if not self.enable_query_rewriting:
            history = self.build_history_context()

        query = self.modify_query(query)
        context, sources = self.active_retriever(query)

        prompt = self.prompt_generator.get_rag_prompt(context, query, history=history)

        return prompt, sources


    def get_sources(self, result):
        sources = set()

        for res in result:
            sources.add(
                (
                    res["document_path"],
                    res["start_page"],
                    res["end_page"]
                )
            )

        updated_sources = {}
        for file_path, start_page, end_page in sources:

            if file_path in updated_sources:

                updated_sources[file_path]["start_page"] = min(
                    updated_sources[file_path]["start_page"],
                    start_page
                )

                updated_sources[file_path]["end_page"] = max(
                    updated_sources[file_path]["end_page"],
                    end_page
                )

            else:

                updated_sources[file_path] = {
                    "start_page": start_page,
                    "end_page": end_page
                }

        final_sources = []
        for file_path, pages in updated_sources.items():

            final_sources.append({
                "source_file": file_path.split("/")[-1],
                "pages": [pages["start_page"], pages["end_page"]]
            })

        return final_sources


    def ask(self, query):
        prompt, sources = self.build_prompt(query)
        response = self.llm_model.generate(prompt)

        self.memory.add_interaction(query, response)

        answer = {
            "answer": response, 
            "sources": sources
        }

        return answer


    def retrieve_with_faiss(self, query):
        result = self.retriever.retrieve(query)
        sources = self.get_sources(result)
        context = self.context_builder.build_context(result)

        return context, sources


    def retrieve_with_bm25(self, query):

        result = self.bm25_retriever.retrieve(query)
        sources = self.get_sources(result)
        context = self.context_builder.build_context(result)

        return context, sources


    def retrieve_with_hybrid(self, query):

        faiss_results = self.retriever.retrieve(query)
        bm25_results = self.bm25_retriever.retrieve(query)

        merged_results = faiss_results + bm25_results

        seen = set()
        unique_results = []

        for result in merged_results:

            key = (
                result["document_path"],
                result["start_page"],
                result["end_page"],
                result["text"]
            )

            if key not in seen:
                seen.add(key)
                unique_results.append(result)

        sources = self.get_sources(unique_results)

        context = self.context_builder.build_context(
            unique_results
        )

        return context, sources


    def modify_query(self, query):

        if self.enable_query_rewriting:
            history = self.build_history_context()

            rewritten_query = self.query_rewriter.rewrite(
                history,
                query
            )

            return rewritten_query
        
        return query