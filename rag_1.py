import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.embeddings import Embeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()
api_key = os.getenv("GAMINI_API")
if not api_key:
    raise RuntimeError("GAMINI_API is missing in your .env file")

client = genai.Client(api_key=api_key)


class GeminiEmbeddings(Embeddings):
    def __init__(self, client, model="gemini-embedding-2"):
        self.client = client
        self.model = model



    def embed_documents(self, texts):
     vectors = []
     for t in texts:
        resp = self.client.models.embed_content(model=self.model, contents=t)
        vectors.append(resp.embeddings[0].values)
     return vectors
 

    def embed_query(self, text):
        resp = self.client.models.embed_content(model=self.model, contents=text)
        return resp.embeddings[0].values


pdf_path = Path(__file__).parent / "Freight_Forecasting_Team_Overview.pdf"
docs = PyPDFLoader(file_path=str(pdf_path)).load()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks= text_splitter.split_documents(docs)
print(len(docs))
print(len(chunks))


embedding = GeminiEmbeddings(client)

# vector_store = QdrantVectorStore.from_documents(
#     documents=docs,
#     embedding=embedding,
#     url="http://localhost:6333",
#     collection_name="learn_rag",
# )

retriver= QdrantVectorStore.from_existing_collection(
    embedding=embedding,
    url="http://localhost:6333",
   collection_name="learn_rag",
)

retriver_chunk = retriver.similarity_search(
   query="what is vessel??",
)

syestem_prompt = f"""
        You are an helpfull AI assistant who  responds base on the avialabe context.
        conext: {retriver_chunk}
    """

print("added successfully")