from dataclasses import dataclass

@dataclass
class Chunk:
    chunk_id: int

    document_id: int
    document_path: str
    
    start_page: int
    end_page: int
    
    text: str

@dataclass
class PositionedWord:
    word: str
    page_number: int


class Chunker:

    def __init__(self, chunk_size=150, overlap=50):
        
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.step = chunk_size - overlap
        

    def get_chunks(self, processed_documents):
        processed_chunks = []

        document_id = 1
        for processed_document in processed_documents:
            positioned_words = []
            
            for page in processed_document.pages:
                words = page.text.split()
            
                for word in words:
                    positioned_words.append(
                        PositionedWord(
                            word = word,
                            page_number = page.page_number
                        )
                    )

            start = 0
            chunk_id = 1

            chunks = []
            while start < len(positioned_words):
    
                chunk_words = positioned_words[start : start + self.chunk_size]
                chunk_text = " ".join(word.word for word in chunk_words)
            
                page_numbers = [word.page_number for word in chunk_words]
                
                chunks.append(
                    Chunk(
                        chunk_id = chunk_id,

                        document_id = document_id,
                        document_path = processed_document.file_path,
    
                        start_page = page_numbers[0],
                        end_page = page_numbers[-1],
    
                        text = chunk_text
                    )
                )
    
                start = start + self.step
                chunk_id += 1

            processed_chunks.extend(chunks)
            document_id += 1

        return processed_chunks