import warnings
warnings.filterwarnings("ignore")

from langchain_community.vectorstores import Chroma

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings

print("Hafıza yükleniyor, lütfen bekleyin...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Daha önce kaydettiğimiz ChromaDB'yi doğrudan diskten açıyoruz (tekrar bekleme yok!)
db = Chroma(
    persist_directory="C:/yapayzeka/chroma_db",
    embedding_function=embeddings
)

print("\n" + "="*50)
print("AU ARŞİV ARAMA MOTORU HAZIR!")
print("Çıkmak için 'q' yazıp Enter'a basabilirsiniz.")
print("="*50 + "\n")

while True:
    soru = input("\nNe aramak istiyorsunuz? (İngilizce/Türkçe): ").strip()
    if not soru:
        continue
    if soru.lower() == 'q':
        print("Görüşmek üzere!")
        break

    # En alakalı 3 parçayı getir
    sonuclar = db.similarity_search(soru, k=3)

    print(f"\n--- '{soru}' İÇİN BULUNAN EN ALAKALI PARÇALAR ---")
    for i, doc in enumerate(sonuclar):
        kaynak = doc.metadata.get('source', 'Bilinmeyen Dosya')
        print(f"\n[Sonuç {i+1}] (Kaynak: {kaynak}):")
        print("-" * 40)
        print(doc.page_content.strip())
        print("-" * 40)