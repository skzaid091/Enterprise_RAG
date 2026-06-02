from groq import Groq


class LLM_Service:

    def __init__(self, api_key, model):
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate(self, prompt, hide_auto_regressive_output=True):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content