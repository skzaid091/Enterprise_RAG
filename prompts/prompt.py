class Prompt_Generator:

    def __init__(self):

        self.RAG_PROMPT_without_history = """You are a helpful AI assistant.

        Answer the user's question using only the retrieved context.

        Requirements:
        1. Give a concise answer.
        2. Focus only on information relevant to the question.
        3. Do not include unrelated details.
        4. If the answer is not in the context, say so.
        5. Do not use outside knowledge.

        Retrieved Context:
        {context}

        Question:
        {query}

        Answer:
        """

        self.RAG_PROMPT_with_history = """You are a helpful AI assistant.

        Answer the user's question using only the retrieved context.

        Requirements:
        1. Give a concise answer.
        2. Focus only on information relevant to the question.
        3. Do not include unrelated details.
        4. If the answer is not in the context, say so.
        5. Do not use outside knowledge.

        Conversation History:
        {history}

        Retrieved Context:
        {context}

        Question:
        {query}

        Answer:
        """


    def get_rag_prompt(self, context, query, history=None):
        if history:
            return self.RAG_PROMPT_with_history.format(
                history=history,
                context=context,
                query=query
            )

        return self.RAG_PROMPT_without_history.format(
                history=history,
                context=context,
                query=query
            )