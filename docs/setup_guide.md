# Setup Guide - Sabores de Bogotá Chatbots

This guide will help you set up both gastronomy recommendation chatbots (NLP and LLM versions).

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Telegram account
- OpenAI API key (for LLM bot)

## Step 1: Create Virtual Environment

```bash
cd EntregaFinalAnalisisDatos
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your tokens:
```
NLP_BOT_TOKEN=your_telegram_bot_token_for_nlp_bot
LLM_BOT_TOKEN=your_telegram_bot_token_for_llm_bot
OPENAI_API_KEY=your_openai_api_key
```

### How to Get Telegram Bot Tokens

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create bot
4. Copy the token provided
5. Repeat for second bot (you need 2 tokens - one for each bot)

### How to Get OpenAI API Key

1. Go to https://platform.openai.com/
2. Create account or log in
3. Go to API keys section
4. Create new secret key
5. Copy the key

## Step 4: Run the Bots

### Run NLP Bot:
```bash
python run_nlp_bot.py
```

### Run LLM Bot (in another terminal):
```bash
python run_llm_bot.py
```

## Testing the Bots

1. Open Telegram
2. Search for your bot by name
3. Start conversation with `/start`
4. Try asking questions:
   - "¿Cuál es tu horario?"
   - "¿Dónde están ubicados?"
   - "¿Decoran bodas?"
   - "¿Cuánto cuesta?"

## Troubleshooting

**Import errors:**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

**Bot not responding:**
- Check that token is correct in `.env`
- Make sure bot is running (check terminal output)
- Verify internet connection

**OpenAI errors:**
- Verify API key is correct
- Check you have credits in your OpenAI account
- Check API rate limits

## Project Structure

```
EntregaFinalAnalisisDatos/
├── src/
│   ├── common/          # Shared utilities (config, logger, exceptions)
│   ├── nlp_bot/         # NLP bot with TF-IDF
│   ├── llm_bot/         # LLM bot with OpenAI
│   └── analysis/        # Comparison tools
├── data/
│   ├── corpus/          # Q&A knowledge base
│   └── prompts/         # LLM system prompts
├── run_nlp_bot.py       # NLP bot entry point
└── run_llm_bot.py       # LLM bot entry point
```
