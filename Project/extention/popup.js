// Replace with your Hugging Face API key
const HUGGINGFACE_API_KEY = 'hf_your_api_key';

// DOM elements
const chatEl = document.getElementById('chat');
const inputEl = document.getElementById('input');
const sendBtn = document.getElementById('sendBtn');

let conversationHistory = [];
let qaChain = null;

// Append message to chat window
function appendMessage(text, sender) {
  const msg = document.createElement('div');
  msg.className = 'message ' + sender;
  msg.textContent = text;
  chatEl.appendChild(msg);
  chatEl.scrollTop = chatEl.scrollHeight;
}

// Fetch visible text from the current active tab
async function fetchPageText() {
  return new Promise((resolve, reject) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (!tabs[0]) {
        reject('No active tab found');
        return;
      }
      chrome.scripting.executeScript(
        {
          target: { tabId: tabs[0].id },
          func: () => {
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
              acceptNode: (node) => {
                if (!node.parentElement) return NodeFilter.FILTER_REJECT;
                const style = window.getComputedStyle(node.parentElement);
                if (style.display === 'none' || style.visibility === 'hidden') return NodeFilter.FILTER_REJECT;
                if (node.textContent.trim() === '') return NodeFilter.FILTER_REJECT;
                return NodeFilter.FILTER_ACCEPT;
              }
            });
            let node;
            let text = '';
            while ((node = walker.nextNode())) {
              text += node.textContent + ' ';
            }
            return text.trim();
          }
        },
        (results) => {
          if (chrome.runtime.lastError) {
            reject(chrome.runtime.lastError.message);
            return;
          }
          resolve(results[0].result);
        }
      );
    });
  });
}

// Initialize LangChain QA chain with page text using Hugging Face embeddings and LLM
async function initializeChain(pageText) {
  const { Document } = window.langchain.document;
  const { HuggingFaceEmbeddings } = window.langchain.embeddings;
  const { FAISS } = window.langchain.vectorstores;
  const { RetrievalQAChain } = window.langchain.chains;
  const { HuggingFaceInference } = window.langchain.llms;

  // Create document from page text
  const docs = [new Document({ pageContent: pageText })];

  // Create Hugging Face embeddings instance
  const embeddings = new HuggingFaceEmbeddings({
    modelName: "sentence-transformers/all-MiniLM-L6-v2",
    apiKey: HUGGINGFACE_API_KEY
  });

  // Create vector store from documents
  const vectorStore = await FAISS.fromDocuments(docs, embeddings);

  // Create retriever
  const retriever = vectorStore.asRetriever();

  // Initialize Hugging Face LLM for Q&A
  const llm = new HuggingFaceInference({
    model: "google/flan-t5-xl",
    apiKey: HUGGINGFACE_API_KEY
  });

  // Create Retrieval QA chain
  qaChain = RetrievalQAChain.fromLLM(llm, retriever);
}

// Handle user question input
async function handleUserInput(question) {
  if (!qaChain) {
    appendMessage("Loading page content and initializing model, please wait...", "bot");
    try {
      const pageText = await fetchPageText();
      await initializeChain(pageText);
    } catch (err) {
      appendMessage("Error fetching page content: " + err, "bot");
      return;
    }
  }

  appendMessage(question, "user");
  conversationHistory.push({ sender: 'user', text: question });

  try {
    const answer = await qaChain.call({ query: question });
    appendMessage(answer.text, "bot");
    conversationHistory.push({ sender: 'bot', text: answer.text });
  } catch (err) {
    appendMessage("Error getting answer: " + err.message, "bot");
  }
}

// Event listeners
sendBtn.addEventListener('click', async () => {
  const question = inputEl.value.trim();
  if (!question) return;
  inputEl.value = '';
  await handleUserInput(question);
});

inputEl.addEventListener('keydown', async (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    sendBtn.click();
  }
});
