from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA  


class PineconeService:
    def __init__(self, host, index_name, namespace, embeddings):
        self.pc = Pinecone()
        self.host = host
        self.index_name = index_name
        self.namespace = namespace
        self.index = self.pc.Index(host=self.host, name=self.index_name)
        self.embeddings = embeddings
        self.vectorstore = PineconeVectorStore(index_name=index_name, namespace=namespace, embedding=embeddings)
        
    def get_total_vector_count(self):
        return self.index.describe_index_stats()['total_vector_count']
    
    def add_documents(self, docs):
        self.vectorstore.add_documents(docs)

    def delete_all_vector(self):
        self.vectorstore.delete(delete_all=True)

    def query(self, query: str):
        results = self.index.query(
            namespace=self.namespace,
            vector=self.embeddings.embed_query(query),
            top_k=10,
            include_metadata=True
        )
        return results
    

