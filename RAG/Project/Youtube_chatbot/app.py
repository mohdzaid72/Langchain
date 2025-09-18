import yt_dlp
import requests
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma,FAISS
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
load_dotenv()

# ----------------- STEP 1: Fetch transcript -----------------
def get_transcript(video_url, lang='en'):
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [lang],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        subtitles = info.get('automatic_captions') or info.get('subtitles')
        if not subtitles or lang not in subtitles:
            print("⚠️ No subtitles found for this video.")
            return [], ""

        sub_url = subtitles[lang][0]['url']
        response = requests.get(sub_url)
        content_type = response.headers.get('Content-Type', '')

        transcript_list = []

        if 'json' in content_type or response.text.strip().startswith('{'):
            data = json.loads(response.text)
            for event in data.get('events', []):
                segs = event.get('segs', [])
                line = ''.join(seg.get('utf8', '') for seg in segs)
                if line.strip():
                    transcript_list.append({'text': line.strip()})
        else:
            lines = response.text.splitlines()
            for line in lines:
                if line.strip() and not line.startswith(('WEBVTT', '00:', '-->')):
                    transcript_list.append({'text': line.strip()})

        transcript = " ".join([entry['text'] for entry in transcript_list])
        return transcript_list, transcript

# ----------------- STEP 2: Load and Split Transcript -----------------
video_url = "https://www.youtube.com/watch?v=Gfr50f6ZBvo"
transcript_list, transcript = get_transcript(video_url)

if not transcript:
    print("⚠️ Transcript could not be fetched. Exiting.")
    exit()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.create_documents([transcript])

print(f"✅ Transcript length: {len(transcript)} characters")
print(f"✅ Created {len(chunks)} chunks for embeddings.")

# ----------------- STEP 3: Embed and Store in Chroma -----------------
embedding_model = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
"""
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="chroma_db",
    persist_directory=None  # in-memory
)
"""
vector_store=FAISS.from_documents(chunks,embedding_model)

print(vector_store.index_to_docstore_id)

print(f"✅ Stored {len(vector_store.get()['documents'])} documents in vector store.")

# ----------------- STEP 4: Query with MMR Search -----------------
query = "what is deepmind?"
results = vector_store.max_marginal_relevance_search(
    query=query,
    k=3,
    fetch_k=10,
    lambda_mult=0.5
)

print("\n🔎 Query:", query)
if not results:
    print("⚠️ No results found.")
else:
    for i, doc in enumerate(results, start=1):
        print(f"\nRank {i}")
        print("Content:", doc.page_content[:250], "...")

# ----------------- STEP 5: RAG with HuggingFace LLM -----------------
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-large",
    model_kwargs={"temperature": 0.5}
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vector_store.as_retriever(),
    return_source_documents=True
)

response = qa_chain.run(query)
print("\n🧠 LLM Response:\n", response)
