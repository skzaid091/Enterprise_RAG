class ConversationMemory:

    def __init__(self, max_history=5):
        self.max_history = max_history
        self.history = []


    def add_interaction(self, user_query, assistant_response):

        self.history.append({
            "user": user_query,
            "assistant": assistant_response
        })

        if len(self.history) > self.max_history:
            self.history.pop(0)


    def get_history(self):
        return self.history


    def clear_memory(self):
        self.history.clear()