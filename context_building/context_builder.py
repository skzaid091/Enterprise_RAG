class ContextBuilder:

    def build_context(self, chunks):

        context = "\n\n".join(
            chunk["text"]
            for chunk in chunks
        )
        
        return context