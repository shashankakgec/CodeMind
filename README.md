# ⚡ CodeMind IDE

> A research-team software-engineering project. Source presence is not proof of end-to-end operation, offline operation, or security validation. See [the implementation and evidence audit](docs/RESEARCH_IMPLEMENTATION_STATUS.md).

![CodeMind IDE](https://img.shields.io/badge/version-2.0.0-blue)
![React](https://img.shields.io/badge/React-18-61dafb)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)
![Gemini](https://img.shields.io/badge/AI-Gemini_2.5_Flash-orange)

## 🎯 Features

### 💻 IDE Workspace & Files
- **Code search & Line-Jumping** — Embedding-based code search is implemented as a separate index; it is not the same as the exact AST search in the minimal research prototype.
- **Complexity Analyzer** — Detailed maintainability indexes, Halstead metrics, and cyclomatic complexity scoring.
- **Drag-and-Drop File System** — High-performance file tree navigation supporting instant drag-and-drop workspace uploads.

### 🤖 Intelligent AI Engine
- **AI Code Review** — Cognitive bug scanning, security audits, and performance analysis with custom scorecards.
- **Auto-Fix** — One-click autonomous in-editor code patching and patch applications.
- **Explain Code** — Natural language structural breakdowns, architectural explanations, and execution flow analysis.
- **Generate Tests** — Automated, high-coverage unit test suite generation for standard frameworks.
- **Bug classifier integration** — Calls a remote Hugging Face Inference API; local CodeBERT inference and verified benchmark metrics are not established by this integration.
- **Review memory** — Exact code-hash and recent same-language review retrieval; this path is not project-isolated neural RAG. A separate JSON embedding index supports code search.

### 📊 Runtime & Visualizations
- **Code execution** — Restricted Docker execution code with an OnlineCompiler.io fallback when Docker is unavailable. The fallback sends code to an external service; the current Docker options do not establish a hardened security sandbox.
- **Python execution tracing** — Tracing and visualization modules are present in source; their safety and end-to-end correctness have not been independently validated.
- **Algorithm Visualizer** — Animated step-by-step visualizations of 14 key sorting, graph, and recursion algorithms.

## 🧠 Algorithm Visualizer

| Category | Algorithms |
|---|---|
| Sorting | Bubble, Insertion, Selection, Merge, Quick Sort |
| Searching | Linear Search, Binary Search |
| Graph | BFS, DFS |
| Recursion | Fibonacci, Factorial |
| Data Structures | Stack, Queue, Linked List |

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Monaco Editor (`@monaco-editor/react`), CSS Modules, Vite |
| Backend | FastAPI, Python 3.11+, SQLite, Docker where available; OnlineCompiler.io API fallback (remote), Pydantic |
| AI | Google Gemini 2.5 Flash, Hugging Face Inference API (remote); optional SentenceTransformers embeddings, JSON Vector Store |
| Styling | Custom cyberpunk design system with dark mode |

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional; execution behaviour differs when unavailable)
- Free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 1. Run the Backend
```bash
cd backend
python -m venv venv

# Activate Virtual Environment (Windows)
venv\Scripts\activate
# Activate Virtual Environment (macOS/Linux)
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env and paste your GEMINI_API_KEY

uvicorn backend.main:app --reload --port 8000
```

### 2. Run the Frontend
```bash
cd frontend
npm install
npm run dev
```
Open **`http://localhost:5173`** in your browser.

---

## 🔑 Environment Variables

### Backend (`backend/.env`):
```env
GEMINI_API_KEY=your_gemini_api_key_here
MAX_EXECUTION_STEPS=500     # Limit for variable tracer steps (default: 500)
MAX_EXECUTION_TIMEOUT=10    # Execution timeout limit in seconds (default: 10)

# Production fallbacks (Render cloud environment)
ONLINE_COMPILER_KEY=your_onlinecompiler_io_api_key_here
HF_TOKEN=your_huggingface_inference_token_here
HF_MODEL_REPO=Monkey3770/Codebert-bug-classifier
```

### Frontend (`frontend/.env` - Optional):
```env
VITE_API_URL=http://localhost:8000  # Leave blank to automatically use local fallback
```

---

## 📁 Project Structure

```text
codemind-ide/
├── backend/
│   ├── data/                # SQLite DBs (Reviews, RAG Memory) & JSON vector store
│   ├── models/              # Model-related assets (verify availability and provenance)
│   ├── main.py              # FastAPI entry point
│   ├── models.py            # Pydantic schemas for requests/responses
│   ├── routers/ai.py        # API endpoints for AI and visualization
│   └── services/
│       ├── llm.py           # Gemini AI integration (Review, Fix, Explain)
│       ├── test.py          # Automated unit test generation framework
│       ├── code_tracer.py   # Python execution tracing module (not security-validated)
│       ├── code_executor.py # Restricted Docker execution and remote fallback
│       ├── code_indexer.py  # Semantic search indexing (JSON Vector Store)
│       ├── rag_pipeline.py  # Exact/recent review-memory retrieval
│       ├── complexity_analyzer.py # Static code complexity analysis 
│       └── review_history.py # SQLite service for storing code reviews
└── frontend/
    ├── package.json         # Vite and React dependencies
    ├── vite.config.js       # Vite configuration
    └── src/
        ├── App.jsx          # Main IDE application layout
        ├── components/      # React components (Editor, FileExplorer, Panels)
        ├── hooks/           # Custom React hooks (useAI, useEditor, useCodeVisualizer)
        ├── utils/           # Helper utilities (Monaco markers)
        └── styles/          # Global styles and themes
```

---

## 🤝 Contributing
Contributions are welcome! Please feel free to open issues or submit pull requests for new features, bug reports, and enhancements.

---

## License
No LICENSE file is currently present in this repository. Do not assume MIT licensing until the research-team maintainers add and confirm the applicable license.

## Privacy and research status
Gemini, Hugging Face Inference API, and OnlineCompiler.io are remote services. Code or prompts sent through these integrations leave the local machine. Do not describe a deployment as strict-offline while any remote provider or fallback is enabled. The paper's separate minimal Python API prototype and its four tests are not this full-stack repository and must not be conflated with it. No Devign/CodeBERT benchmark, measured RAG improvement, end-to-end usability result, strict-offline verification, or Docker security result is currently claimed.

See [docs/RESEARCH_IMPLEMENTATION_STATUS.md](docs/RESEARCH_IMPLEMENTATION_STATUS.md) for the source audit and remaining validation checklist.
