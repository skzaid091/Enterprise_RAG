import os
import pymupdf
from dataclasses import dataclass

@dataclass  
class PageContent:
    page_number: int
    text: str
    word_count: int

@dataclass
class PDFDocument:
    file_path: str
    page_count: int
    pages: list[PageContent]   # one per page
    metadata: dict             # title, author, etc from PDF headers
    error: str | None          # None if success


class PDFLoader:
    
    def load(self, pdf_path):

        if not os.path.exists(pdf_path):
            return PDFDocument(
                file_path=pdf_path,
                page_count=0,
                pages=[],
                metadata={},
                error=f"File not found: {pdf_path}"
            )
        
        try:
            doc = pymupdf.open(pdf_path)
            
        except Exception as e:
            return PDFDocument(
                file_path=pdf_path,
                page_count=0,
                pages=[],
                metadata={},
                error=f"Failed to open PDF: {e}"
            )

        # metadata
        raw = doc.metadata
        metadata = {
            "title":   raw.get("title"),
            "author":  raw.get("author"),
            "subject": raw.get("subject"),
        }

        pages = []
        for page in doc:
            text = page.get_text().strip()
            
            pages.append(PageContent(
                page_number=page.number + 1,
                text=text,
                word_count=len(text.split())
            ))

        return PDFDocument(
            file_path=pdf_path,
            page_count=len(doc),
            pages=pages,
            metadata=metadata,
            error=None
        )


    def load_documents(self, documents):
        processed_documents = []
        
        for document_path in documents:
            processed_documents.append(
                self.load(document_path)
            )

        return processed_documents