import ollama

class LLM_Service:

    def __init__(self, model):
        self.model = model

    def generate(self, prompt):

        stream = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=True
        )

        response = ""

        for chunk in stream:
            token = chunk["message"]["content"]

            print(
                token,
                end="",
                flush=True
            )

            response += token

        print()  # newline after streaming

        return response