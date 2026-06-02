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
    print("\nRunning Retrieval Evaluation...\n")

    rag.evaluate_retrieval()

    input("\nPress Enter to return to the main menu...")


def main():
    while True:
        print("\n===== Enterprise RAG =====")
        print("1. Chat with Chatbot")
        print("2. Retrieval Evaluation")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            chat_with_bot()

        elif choice == "2":
            run_retrieval_evaluation()

        elif choice == "0":
            print("\nGoodbye!\n")
            break

        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()