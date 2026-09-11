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

print("Sistem hazırlanıyor (Vektör Motoru & ChromaDB)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
persist_dir = "C:/yapayzeka/chroma_db"
db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

# Yerel LLM Beyni (Ollama Llama 3.2)
llm = ChatOllama(model="llama3.2:3b", temperature=0.5)

# Modele AU kuralını ve edebi sınırları dikte eden şablon
prompt_sablonu = ChatPromptTemplate.from_template("""
You are an expert literary fiction editor analyzing the user's personal fiction archive.

CRITICAL INSTRUCTION - STRICT ALTERNATE UNIVERSE (AU):
Do NOT rely on or import mainstream Harry Potter canon lore, character allegiances, or backstories. 
This is a distinct Alternate Universe. Sirius, Severus, Remus, and Lily have completely different paths, loyalties, and histories here.
Do NOT assume anyone went to Azkaban, joined the Death Eaters, or died unless the excerpts explicitly state it. 
Base your analysis EXCLUSIVELY on the reality established in the provided text.

Adhere to the following principles:
1. **Emotional Subtext:** Emphasize feelings left unsaid—helplessness, repressed feelings, guilt, affection, or subtle boundaries.
2. **Character Dynamics:** Deconstruct the tension, power balances, and domestic or emotional bonds between characters.
3. **Textual Evidence:** Ground your interpretations strictly in concrete moments, dialogue, or actions from the provided excerpts.
4. **Fidelity:** Never fabricate events or fill gaps with mainstream canon lore.

CONTEXT:
{context}

QUESTION:
{question}

LITERARY ANALYSIS:
""")

output_parser = StrOutputParser()

while True:
    soru = input("\nAsk a question about your archive (or 'q' to quit): ")
    if soru.lower() == 'q':
        break
    if not soru.strip():
        continue

    print("\n[1/2] Searching relevant scenes in ChromaDB...")
    docs = db.similarity_search(soru, k=5)
    
    if not docs:
        print("No relevant scenes found in the archive.")
        continue

    baglam = "\n\n---\n\n".join([d.page_content for d in docs])

    print("[2/2] Analyzing literary subtext with local LLM...\n")
    
    zincir = prompt_sablonu | llm | output_parser
    yanit = zincir.invoke({"context": baglam, "question": soru})

    print("=" * 60)
    print(yanit)
    print("=" * 60)