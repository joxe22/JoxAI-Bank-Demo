# backend/app/services/rag_service.py

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from qdrant_client import QdrantClient

class RAGService:
    def __init__(self):
        # Vector DB (Qdrant)
        self.client = QdrantClient(host="localhost", port=6333)
        self.embeddings = OpenAIEmbeddings()

        # Vector store
        self.vectorstore = Qdrant(
            client=self.client,
            collection_name="banking_knowledge",
            embeddings=self.embeddings
        )

    async def query_knowledge(self, question: str, filters: dict = None):
        """
        Busca en la base de conocimiento vectorial

        Returns:
        {
            "answer": "respuesta generada",
            "sources": [
                {"doc_id": 1, "title": "...", "confidence": 0.95}
            ]
        }
        """
        # Retrieval con filtros (por producto, categoría, etc.)
        docs = self.vectorstore.similarity_search_with_score(
            question,
            k=3,
            filter=filters
        )

        # Generate con LLM
        llm = OpenAI(temperature=0.7)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=self.vectorstore.as_retriever(),
            return_source_documents=True
        )

        result = qa_chain({"query": question})

        return {
            "answer": result["result"],
            "sources": [
                {
                    "doc_id": doc.metadata.get("id"),
                    "title": doc.metadata.get("title"),
                    "confidence": score
                }
                for doc, score in docs
            ],
            "confidence": max([score for _, score in docs])
        }

    async def ingest_document(self, doc_path: str, metadata: dict):
        """
        Ingesta documentos a la base vectorial
        Usado desde Knowledge Base page para añadir artículos
        """
        # Leer documento
        from langchain.document_loaders import PDFLoader
        loader = PDFLoader(doc_path)
        documents = loader.load()

        # Chunking semántico
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_documents(documents)

        # Añadir metadatos
        for chunk in chunks:
            chunk.metadata.update(metadata)

        # Indexar
        self.vectorstore.add_documents(chunks)

        return {"status": "indexed", "chunks": len(chunks)}