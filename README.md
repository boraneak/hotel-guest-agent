# 🏨 Hotel Guest Agent

An AI-powered Telegram chatbot that answers guest questions across multiple hospitality properties using RAG (Retrieval-Augmented Generation). Built with Python, LangChain, ChromaDB, and Groq.

## Live Demo

🤖 **Telegram Bot:** [@hotel_guest_agent_bot](https://t.me/hotel_guest_agent_bot)
🌐 **API Health:** https://hotel-guest-agent.onrender.com/health

## Demo

![Hotel Guest Agent Demo](assets/demo.gif)

## Architecture

```
Guest (Telegram)
      ↓
Telegram Bot (python-telegram-bot)
      ↓
Router — detects which property the question is about
      ↓
RAG Pipeline — splits, embeds, and retrieves from property knowledge base
      ↓
Groq LLM (llama-3.1-8b-instant) — generates natural language answer
      ↓
Memory — stores conversation history per user session
      ↓
Reply to Guest
```

## Properties Supported

| Property | Type |
|---|---|
| 🏨 Grandview Hotel & Resort | Hotel |
| 🍜 Golden Spoon Restaurant | F&B |
| 🏖️ Azure Beach Resort | Resort |

## Tech Stack

| Layer | Technology |
|---|---|
| Bot interface | python-telegram-bot 21.10 |
| Agent framework | LangChain 0.3.25 |
| LLM | Groq (llama-3.1-8b-instant) |
| Embeddings | ChromaDB DefaultEmbeddingFunction (ONNX) |
| Vector store | ChromaDB 1.0.8 |
| Memory | LangChain ConversationBufferMemory |
| API | FastAPI + Uvicorn |
| Deployment | Render (Python 3.13) |

## Project Structure

```
hotel-guest-agent/
├── data/                    # Property knowledge bases (Markdown)
│   ├── grandview_hotel.md
│   ├── golden_spoon.md
│   └── azure_beach.md
├── agent/
│   ├── __init__.py
│   ├── rag.py               # RAG pipeline — load, split, embed, retrieve, generate
│   ├── router.py            # Property router — keyword-based routing
│   └── memory.py            # Conversation memory — per-user isolation
├── bot/
│   └── telegram_bot.py      # Telegram bot — /start + message handler
├── main.py                  # Entry point — FastAPI + Telegram bot
├── test_rag.py              # Smoke tests for RAG and router
├── .env.example             # Environment variable template
├── .python-version          # Python 3.13.3
├── Dockerfile               # Docker build config
└── requirements.txt
```

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/boraneak/hotel-guest-agent
cd hotel-guest-agent
```

**2. Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**
```bash
cp .env.example .env
# Add your GROQ_API_KEY and TELEGRAM_BOT_TOKEN
```

**5. Run the bot**
```bash
python3 main.py
```

**6. Run tests**
```bash
python3 test_rag.py
```

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Service status |
| `/health` | GET | Health check |

## Key Design Decisions

- **Static RAG over live PMS integration** — optimized for demo reliability; architecture supports live booking system integration as Phase 2
- **Per-user memory isolation** — each guest gets independent conversation history, no cross-contamination between concurrent sessions
- **Keyword-based router** — zero-latency, zero-cost routing per message; ML-based intent classification is a natural Phase 2 upgrade
- **ChromaDB local vector store** — no external vector DB dependency; swappable to Pinecone or Weaviate for production scale
- **Groq LLM** — free tier, sub-second latency, production-quality responses; swappable to OpenAI GPT-4o or Anthropic Claude

## Roadmap

- [ ] Phase 2: Live PMS integration for real-time room availability
- [ ] Phase 2: ML-based intent router replacing keyword matching
- [ ] Phase 3: Multi-language support (Khmer + English)
- [ ] Phase 3: Admin dashboard for knowledge base management
- [ ] Phase 4: Voice message support via Telegram
- [ ] Phase 4: Full booking and reservation flow

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Commit your changes (`git commit -m "feat: add your feature"`)
4. Push to the branch (`git push origin feat/your-feature`)
5. Open a Pull Request

Please make sure your code is formatted with `black` before submitting.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
