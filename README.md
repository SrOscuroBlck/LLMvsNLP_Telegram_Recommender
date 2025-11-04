# Chatbot Comparison: NLP vs LLM

Comparison of traditional NLP chatbot (TF-IDF + Cosine Similarity) vs modern LLM chatbot (OpenAI GPT-5 nano) for gastronomy recommendations in Bogotá, Colombia.

## Project Overview

This project implements and compares two Telegram chatbot architectures for restaurant and dish recommendations:

1. **NLP Bot**: Uses TF-IDF vectorization and cosine similarity to match user queries against a predefined corpus of Q&A pairs
2. **LLM Bot**: Uses OpenAI's GPT-5 nano model for natural language understanding and personalized recommendations with conversation context

## Project Structure

```
EntregaFinalAnalisisDatos/
├── src/
│   ├── common/          # Shared utilities
│   ├── nlp_bot/         # Traditional NLP chatbot
│   ├── llm_bot/         # LLM-based chatbot
│   └── analysis/        # Comparative analysis
├── data/                # Corpus and prompts
├── results/             # Analysis results
├── docs/                # Documentation
├── report/              # LaTeX report
├── run_nlp_bot.py       # Run NLP bot
└── run_llm_bot.py       # Run LLM bot
```

## Setup

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your tokens and API keys
```

## Running the Bots

### NLP Bot
```bash
python run_nlp_bot.py
```

### LLM Bot
```bash
python run_llm_bot.py
```

## Bot Commands

- `/start` - Start conversation
- `/help` - Show available commands
- `/reset` - Clear conversation history (LLM bot only)

## Technologies

- **python-telegram-bot 20.7** - Telegram bot framework
- **scikit-learn 1.3.2** - TF-IDF vectorization and cosine similarity
- **OpenAI API (openai 1.3.5)** - GPT-5 nano language model
- **Pydantic 2.5.0** - Data validation and configuration management
- **Docker & Docker Compose** - Containerized deployment

## Docker Deployment

### Quick Start
```bash
# Build and run both bots
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop bots
docker-compose down
```

See [docs/docker_guide.md](docs/docker_guide.md) for complete deployment documentation.

## Authors

Universidad - Análisis de Datos Final Project
# LLMvsNLP_Telegram_Recommender
