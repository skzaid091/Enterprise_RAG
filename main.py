from RAG.rag import RAG
from config.config import config

rag = RAG(config=config)


def chat_with_bot():
    print("\n--- Chat Mode ---")
    print("Type 'back' to return to the main menu.\n")

    while True:
        query = input("Enter query: ").strip()

        if query.lower() == "back":
            break

        response = rag.ask(query)

        print("\nSources:")
        for source in response["sources"]:
            print(source)

        print("\n" + "=" * 100 + "\n")


def run_retrieval_evaluation():
    print("\nRunning Retrieval Evaluation...")

    print(
        f"Retriever Type      : {config['retriever_type']}\n"
        f"Query Re-writing    : {config['enable_query_rewriting']}\n"
        f"Re-ranking          : {config['enable_reranking']}\n"
    )

    rag.evaluate_retrieval()

    input("\nPress Enter to return to the main menu...")


def run_answer_evaluation():
    print("\nRunning Answer Evaluation...\n")

    rag.evaluate_answers()

    input("\nPress Enter to return to the main menu...")


def show_configuration():

    print("\n--- Current Configuration ---\n")

    print(
        f"Reranking Enabled : "
        f"{config['enable_reranking']}"
    )

    print(
        f"Reranker Top K    : "
        f"{config['reranking_top_k']}"
    )

    print(
        f"Reranker Model    : "
        f"{config['reranker_model_path']}"
    )

    input("\nPress Enter to return to the main menu...")


def main():

    while True:

        print("\n===== Enterprise RAG =====")
        print("1. Chat with Chatbot")
        print("2. Retrieval Evaluation")
        print("3. Answer Evaluation")
        print("4. Show Configuration")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            chat_with_bot()

        elif choice == "2":
            run_retrieval_evaluation()

        elif choice == "3":
            run_answer_evaluation()

        elif choice == "4":
            show_configuration()

        elif choice == "0":
            print("\nGoodbye!\n")
            break

        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()