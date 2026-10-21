from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage , SystemMessage 

load_dotenv()

persist_directory = "db/chroma_db"

# load embedding and store vector
embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory = persist_directory,
    embedding_function= embedding_model,
    collection_metadata={"hnsw:space":"cosine"}
)

# search for relevent document
query = "What was NVIDIA's first graphics accelerator called?"

retriever = db.as_retriever(search_kwargs = {"k" : 5})

# retriever = db.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs = {
#         "k":5,
#         "score_threshold":0.3#only return chunks with cosine similarity of >0.3 
#     }
# )

relevant_docs = retriever.invoke(query) 

print(f"User Queary : {query}")
#daiplay results
print("-- contex --")
for i,doc in enumerate(relevant_docs ,1 ):
    print(f"Document {i}: \n{doc.page_content}\n")

# combine the queary and the relevant document content
combined_input = f"""based on the following document , please answer this question {query}

Documents:
{chr(10).join([f"- {doc.page_content}" for doc in relevant_docs])}

"Please provide a clear, helpful answer using only the information from these documents. If you can't find the answer in the documents, say "I don't have enough information to answer that question based on the provided documents."
"""

# Create a ChatOpenAI model
model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0.0,
)
# Define the messages for the model
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content=combined_input),
]

# Invoke the model with the combined input
result = model.invoke(messages)

# Display the full result and content only

# Extract text cleanly whether it returns a string or list of dicts
if isinstance(result.content, list):
    output_text = "".join([part.get("text", "") for part in result.content if isinstance(part, dict)])
else:
    output_text = result.content

print("\n--- Generated Response ---")
print(output_text)
# print("Full result:")
# print(result)
# print("Content only:")
# print(result.content)


# 1. "What was NVIDIA's first graphics accelerator called?"
# 2. "Which company did NVIDIA acquire to enter the mobile processor market?"
# 3. "What was Microsoft's first hardware product release?"
# 4. "How much did Microsoft pay to acquire GitHub?"
# 5. "In what year did Tesla begin production of the Roadster?"
# 6. "Who succeeded Ze'ev Drori as CEO in October 2008?"
# 7. "What was the name of the autonomous spaceport drone ship that achieved the first successful sea landing?"
# 8. "What was the original name of Microsoft before it became Microsoft?"
