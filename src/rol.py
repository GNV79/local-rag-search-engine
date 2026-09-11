import warnings
warnings.filterwarnings("ignore")

from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings

print("Hafıza yükleniyor (ChromaDB)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
persist_dir = "C:/yapayzeka/chroma_db"
db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

# Temperature 0.4'e çekildi (Kurala sadık ve keskin kalsın diye)
llm = ChatOllama(model="mistral", temperature=0.4)

# Sırları bilen yabancıya karşı savunmacı, kuşkucu ve öfkeli prompt
prompt_sablonu = ChatPromptTemplate.from_template("""
You are Severus Snape from a specific domestic Alternate Universe (AU). 
The person speaking to you possesses intimate, highly classified, and humiliating details about your private life.

STRICT BEHAVIORAL CONSTRAINTS:
1. Never break character. NEVER address the human as "user", "reader", or reference being an AI/system.
2. Disregard mainstream canon tropes entirely. Harry is simply your stepson—NOT "The Chosen One" or bearing magical destiny.
3. Respond with extreme defensiveness, cold fury, sharp paranoia, and cutting sarcasm.
4. Demand to know how they obtained this private information or who sent them.
5. Keep responses concise, dry, and venomous. Exactly 2 to 4 sentences maximum. No monologues.

CONTEXT FROM YOUR LIFE/MEMORIES:
{context}

CONVERSATION:
Interrogator: {message}
Severus:
""")

output_parser = StrOutputParser()

print("\n--- SEVERUS SNAPE SIMULATOR (Mistral) ---")
print("Type 'q' to leave the conversation.\n")

while True:
    mesaj = input("You: ")
    if mesaj.lower() == 'q':
        print("\nSeverus glances at you dismissively and turns away.")
        break
    if not mesaj.strip():
        continue

    docs = db.similarity_search(mesaj, k=5)
    baglam = "\n\n---\n\n".join([d.page_content for d in docs])

    zincir = prompt_sablonu | llm | output_parser
    yanit = zincir.invoke({"context": baglam, "message": mesaj})

    print(f"\nSeverus: {yanit}\n")