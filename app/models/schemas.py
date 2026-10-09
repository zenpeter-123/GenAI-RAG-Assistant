from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str = Field(..., description="A felhasználó kérdése", example="Mi a stacionárius eloszlás?")
    top_k: int = Field(default=3, description="Visszaadandó releváns doksi-blokkok száma")

class SourceDocument(BaseModel):
    page_content: str = Field(..., description="A talált szövegrészlet")
    page: Optional[int] = Field(None, description="Oldalszám a PDF-ben")
    source: Optional[str] = Field(None, description="Fájl neve")    
class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceDocument]
    
class IngestResponse(BaseModel):
    filename: str
    num_chunks: int
    message: str