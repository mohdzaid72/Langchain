# 🎥 Q&A System on YouTube Video using LangChain + Hugging Face

An intelligent **Question Answering system** built on top of **LangChain**, **Hugging Face**, and **FAISS**, enabling users to ask natural language questions about any YouTube video and get context-aware answers based on the video’s transcript.

---

## 🚀 Project Overview

This system automatically extracts subtitles or auto-generated transcripts from YouTube videos, processes them into text chunks, embeds them into a **vector store**, and uses a **Retrieval-Augmented Generation (RAG)** pipeline with a **Hugging Face LLM** to answer user queries accurately.

---

## 🧠 Features

- 🧩 **Automatic Transcript Extraction** using `yt_dlp`  
- 🧠 **Semantic Chunking & Embedding** with `RecursiveCharacterTextSplitter` and `HuggingFaceEmbeddings`  
- 🔎 **Efficient Vector Search** with `FAISS` and **MMR (Max Marginal Relevance)** retrieval  
- 💬 **Contextual Q&A** powered by `google/flan-t5-large` via `HuggingFaceEndpoint`  
- ⚙️ **Modular Pipeline** — easy to extend for multiple videos or different models  

---

## 🏗️ Workflow

```
YouTube Video URL
        ↓
Transcript Extraction (yt_dlp)
        ↓
Text Chunking (LangChain)
        ↓
Embeddings (Hugging Face Model)
        ↓
Vector Store (FAISS)
        ↓
Retriever + LLM (RAG Pipeline)
        ↓
Answer Generation
```

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Transcript Extraction** | yt-dlp, requests |
| **Text Processing** | LangChain TextSplitter |
| **Embeddings** | HuggingFaceEmbeddings (`intfloat/multilingual-e5-large`) |
| **Vector Store** | FAISS / Chroma |
| **LLM** | HuggingFaceEndpoint (`google/flan-t5-large`) |
| **Environment Management** | python-dotenv |

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/youtube-video-qa.git
   cd youtube-video-qa
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file and add your Hugging Face API key:
   ```bash
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_key
   ```

---

## ▶️ Usage

1. Open `main.py` (or your file name).  
2. Replace the `video_url` with any valid YouTube video link:
   ```python
   video_url = "https://www.youtube.com/watch?v=Gfr50f6ZBvo"
   ```
3. Run the script:
   ```bash
   python main.py
   ```
4. The system will:
   - Fetch the transcript  
   - Split and embed text  
   - Build FAISS index  
   - Perform retrieval  
   - Generate answers via LLM  

---

## 🧩 Example Output

**Query:**  
```text
what is deepmind?
```

**LLM Response:**  
```text
DeepMind is a research company focusing on artificial intelligence and machine learning, known for projects like AlphaGo and advancements in reinforcement learning.
```

---

## 📦 Requirements

Example `requirements.txt`:
```text
yt_dlp
requests
langchain
langchain_huggingface
langchain_community
faiss-cpu
chromadb
python-dotenv
```

---

## 🔮 Future Enhancements

- Add **Streamlit UI** for interactive chat  
- Integrate **Whisper API** for speech-to-text on videos without subtitles  
- Enable **persistent vector storage** via Chroma or Pinecone  
- Add **multi-video knowledge base** for broader Q&A  

---

## 📜 License

Licensed under the **MIT License** – feel free to use, modify, and share.

---

⭐ **If you found this project interesting, give it a star!**
