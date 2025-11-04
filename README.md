# Chatbot Comparison: NLP vs LLM

Comparison of traditional NLP chatbot (TF-IDF + Cosine Similarity) vs modern LLM chatbot (OpenAI GPT-5 nano) for gastronomy recommendations in Bogotá, Colombia.

## Project Overview

This project implements and compares two Telegram chatbot architectures for restaurant and dish recommendations:

1. **NLP Bot**: Uses TF-IDF vectorization and cosine similarity to match user queries against a predefined corpus of Q&A pairs
2. **LLM Bot**: Uses OpenAI's GPT-5 nano model for natural language understanding and personalized recommendations with conversation context

## Project Structure

```
EntregaFinalAnalisisDatos/
├── project/                    # Code directory (all functional code)
│   ├── src/
│   │   ├── common/            # Shared utilities (config, logger)
│   │   ├── nlp_bot/           # Traditional NLP chatbot
│   │   ├── llm_bot/           # LLM-based chatbot
│   │   └── analysis/          # Metrics and comparative analysis
│   ├── data/
│   │   ├── corpus/            # Q&A pairs for NLP bot
│   │   └── prompts/           # System prompts for LLM bot
│   ├── tests/                 # Test queries and scenarios
│   ├── docs/                  # Documentation
│   ├── runners/               # Execution scripts
│   │   ├── run_nlp_bot.py    # Run NLP bot
│   │   ├── run_llm_bot.py    # Run LLM bot
│   │   └── run_tests.py      # Direct function testing
│   ├── analysis/              # Analysis scripts
│   │   └── generate_plots.py # Generate comparison visualizations
│   ├── results/               # Test results and metrics (JSON)
│   ├── docker-compose.yml     # Multi-container orchestration
│   ├── Dockerfile.nlp         # NLP bot container
│   ├── Dockerfile.llm         # LLM bot container
│   └── requirements.txt       # Python dependencies
└── report/                     # LaTeX report directory
    └── figures/               # Diagrams and plots (15 images)
```

## Setup

**Note:** All commands should be run from the `project/` directory.

1. Navigate to project directory:
```bash
cd project
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your tokens and API keys
```

Required environment variables:
- `TELEGRAM_TOKEN_NLP` - Telegram bot token for NLP bot
- `TELEGRAM_TOKEN_LLM` - Telegram bot token for LLM bot
- `OPENAI_API_KEY` - OpenAI API key
- `OPENAI_MODEL` - OpenAI model (e.g., "gpt-4o-mini")

## Running the Bots

### Locally (from project/ directory)

**NLP Bot:**
```bash
cd project
python runners/run_nlp_bot.py
```

**LLM Bot:**
```bash
cd project
python runners/run_llm_bot.py
```

### Direct Function Testing (without Telegram)

Test both bots with predefined queries and generate metrics:
```bash
cd project
python runners/run_tests.py
```

This will:
- Run 15 test queries against both bots
- Generate comparison metrics (JSON files in `results/`)
- Calculate accuracy, response times, and keyword matching
- Save detailed results for analysis

## Bot Commands

Both bots support the following commands:
- `/start` - Start conversation and get welcome message
- `/help` - Show available commands and usage instructions
- `/reset` - Clear conversation history (LLM bot only)

## Key Features

### NLP Bot
- **TF-IDF Vectorization** with cosine similarity matching
- **Predefined corpus** of 19 Q&A pairs about Bogotá gastronomy
- **Similarity threshold** of 0.3 for matching
- **Fast response times** (~5-10ms average)
- **Deterministic responses** from corpus

### LLM Bot
- **GPT-5 nano** via OpenAI Responses API
- **Conversation context** maintenance (last 10 messages)
- **System prompt** for gastronomy expert persona
- **Natural language understanding** with contextual responses
- **Dynamic recommendations** based on user preferences

## Technologies

### Core Technologies
- **Python 3.10.13** - Programming language
- **python-telegram-bot 20.7** - Telegram bot framework
- **scikit-learn 1.3.2** - TF-IDF vectorization and cosine similarity
- **OpenAI API (openai 1.3.5)** - GPT-5 nano Responses API
- **Pydantic 2.5.0** - Data validation and configuration management
- **Docker & Docker Compose** - Containerized deployment

### Analysis & Visualization
- **matplotlib 3.8.2** - Plot generation (300 DPI publication quality)
- **numpy 1.26.2** - Numerical computations

### Development Tools
- **python-dotenv 1.0.0** - Environment variable management
- **Custom metrics calculator** - Automated performance analysis

## Docker Deployment

**All Docker commands must be run from the `project/` directory.**

### Quick Start
```bash
cd project

# Build and run both bots
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# View specific bot logs
docker-compose logs -f nlp-bot
docker-compose logs -f llm-bot

# Stop bots
docker-compose down
```

See [docs/docker_guide.md](docs/docker_guide.md) for complete deployment documentation.

## Analysis and Visualization

Generate comparison plots and visualizations:

```bash
cd project
python analysis/generate_plots.py
```

This will generate 10 publication-quality plots (300 DPI) in `results/`:
1. Response time comparison
2. Response time log scale
3. Accuracy by category
4. Accuracy by difficulty
5. Overall metrics comparison
6. Success/failure rates
7. Keyword coverage
8. Category heatmap
9. Query response times
10. Relevance distribution

## Testing Framework

The project includes a comprehensive testing framework with:
- **15 test queries** across 11 categories (recommendations, hours, prices, etc.)
- **3 difficulty levels** (easy, medium, hard)
- **Automated metrics calculation** (accuracy, response time, keyword matching)
- **JSON export** for further analysis

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing documentation.

## Project Deliverables

### Code (project/)
- ✅ Fully functional NLP and LLM chatbots
- ✅ Docker containerization with multi-container deployment
- ✅ Comprehensive testing framework with 15 test queries
- ✅ Automated metrics calculation and visualization generation
- ✅ Clean code structure following SOLID principles

### Report (report/)
- 📄 IEEE format LaTeX document
- 📊 15 figures (5 diagrams + 10 plots at 300 DPI)
- 📚 Estado del arte with 10 academic papers (Scopus 2023-2026)
- 🔬 CRISP-ML methodology documentation
- 📈 Complete comparative analysis with statistical metrics

## Documentation

- [Docker Deployment Guide](docs/docker_guide.md)
- [Setup Guide](docs/setup_guide.md)
- [Testing Guide](TESTING_GUIDE.md)
- [Architecture Overview](docs/architecture.md)

## Repository

**GitHub:** [SrOscuroBlck/LLMvsNLP_Telegram_Recommender](https://github.com/SrOscuroBlck/LLMvsNLP_Telegram_Recommender)

## Author

**Gustavo Adolfo Camargo Pineda**  
Facultad de Ingeniería  
Universidad San Buenaventura Cali  
📧 gaamargop@correo.usbcali.edu.co

---

*Proyecto Final - Análisis de Datos*  
*Universidad San Buenaventura Cali, 2025*
