import warnings
warnings.filterwarnings("ignore")

import glob
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings

print("Vektör motoru hazırlanıyor...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

persist_dir = "C:/yapayzeka/chroma_db"
db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

kaynak_klasoru = "C:/yapayzeka/kaynaklar"
txt_dosyalari = glob.glob(f"{kaynak_klasoru}/*.txt")

if not txt_dosyalari:
    print("HATA: 'kaynaklar' klasöründe dosya yok!")
    exit()

# Veritabanında zaten kayıtlı olan kaynakları kontrol et
mevcut_veriler = db.get()
kayitli_kaynaklar = set()
if mevcut_veriler and "metadatas" in mevcut_veriler and mevcut_veriler["metadatas"]:
    for meta in mevcut_veriler["metadatas"]:
        if meta and "source" in meta:
            kayitli_kaynaklar.add(os.path.normpath(meta["source"]))

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

eklenen_dosya_sayisi = 0

for dosya in txt_dosyalari:
    norm_dosya = os.path.normpath(dosya)
    
    # Dosya zaten veritabanında varsa atla!
    if norm_dosya in kayitli_kaynaklar:
        print(f"[-] Zaten kayıtlı (atlandı): {os.path.basename(dosya)}")
        continue

    print(f"[+] YENİ DOSYA EKLENİYOR: {os.path.basename(dosya)}")
    loader = TextLoader(dosya, encoding="utf-8")
    dokumanlar = loader.load()
    parcalar = text_splitter.split_documents(dokumanlar)
    
    db.add_documents(parcalar)
    eklenen_dosya_sayisi += 1

if eklenen_dosya_sayisi > 0:
    print(f"\nİşlem tamam! {eklenen_dosya_sayisi} yeni dosya veritabanına eklendi.")
else:
    print("\nYeni bir dosya bulunamadı. Veritabanı zaten güncel!")