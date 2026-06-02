import ollama

class LLM_Service:

    def __init__(self, model):
        self.model = model

    def generate(self, prompt, hide_auto_regressive_output=False):

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

            if not hide_auto_regressive_output:

                print(
                    token,
                    end="",
                    flush=True
                )

            response += token

        if not hide_auto_regressive_output:
            print()

        return response