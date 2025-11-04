# Docker Deployment Guide

## Prerequisites

- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)
- Your `.env` file configured with tokens and API keys

## Quick Start

### 1. Build and Run Both Bots

```bash
docker-compose up --build
```

This will:
- Build Docker images for both NLP and LLM bots
- Start both containers
- Keep them running with auto-restart

### 2. Run Bots in Background (Detached Mode)

```bash
docker-compose up -d --build
```

### 3. View Logs

**All bots:**
```bash
docker-compose logs -f
```

**NLP bot only:**
```bash
docker-compose logs -f nlp-bot
```

**LLM bot only:**
```bash
docker-compose logs -f llm-bot
```

### 4. Stop Bots

```bash
docker-compose down
```

### 5. Restart Bots

```bash
docker-compose restart
```

## Individual Bot Management

### Run Only NLP Bot

```bash
docker-compose up nlp-bot
```

### Run Only LLM Bot

```bash
docker-compose up llm-bot
```

### Rebuild Specific Bot

```bash
docker-compose build nlp-bot
docker-compose up -d nlp-bot
```

## Troubleshooting

### Check Bot Status

```bash
docker-compose ps
```

### View Real-time Logs

```bash
docker-compose logs -f nlp-bot
docker-compose logs -f llm-bot
```

### Restart a Specific Bot

```bash
docker-compose restart nlp-bot
# or
docker-compose restart llm-bot
```

### Remove All Containers and Rebuild

```bash
docker-compose down
docker-compose up --build
```

### Access Container Shell (for debugging)

```bash
docker exec -it chatbot-nlp /bin/bash
# or
docker exec -it chatbot-llm /bin/bash
```

## Environment Variables

The bots use these environment variables from `.env`:

**NLP Bot:**
- `NLP_BOT_TOKEN` - Telegram bot token
- `SIMILARITY_THRESHOLD` - Minimum similarity score (0.0-1.0)
- `LOG_LEVEL` - Logging level (INFO, DEBUG, WARNING, ERROR)

**LLM Bot:**
- `LLM_BOT_TOKEN` - Telegram bot token
- `OPENAI_API_KEY` - OpenAI API key
- `OPENAI_MODEL` - Model to use (gpt-5-nano)
- `OPENAI_TEMPERATURE` - Response creativity (0.0-2.0)
- `OPENAI_MAX_TOKENS` - Maximum response length
- `MAX_CONVERSATION_HISTORY` - Messages to keep in history
- `LOG_LEVEL` - Logging level

## Production Deployment

### Using Docker Compose (Recommended)

1. **Set up server** (Ubuntu/Debian):
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y
```

2. **Deploy application**:
```bash
# Clone/upload your project
cd /opt/chatbot-project

# Configure .env file
nano .env

# Start bots in background
docker-compose up -d --build

# Check logs
docker-compose logs -f
```

3. **Set up auto-restart** (already configured):
The `restart: unless-stopped` policy ensures bots restart automatically after crashes or server reboots.

4. **Monitor bots**:
```bash
# Check status
docker-compose ps

# View logs
docker-compose logs --tail=100 nlp-bot
docker-compose logs --tail=100 llm-bot
```

## Resource Management

### View Resource Usage

```bash
docker stats chatbot-nlp chatbot-llm
```

### Set Resource Limits

Edit `docker-compose.yml` to add resource limits:

```yaml
services:
  nlp-bot:
    # ... existing config
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## Backup and Maintenance

### Backup Results Directory

```bash
tar -czf results-backup-$(date +%Y%m%d).tar.gz results/
```

### Update Bots

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Clean Up Old Images

```bash
docker image prune -a
```

## Common Issues

**Issue: "Port already in use"**
- Solution: Telegram bots don't use ports, so this shouldn't happen. If it does, check for other processes.

**Issue: "Cannot connect to OpenAI API"**
- Check API key in `.env`
- Verify internet connection in container: `docker exec chatbot-llm ping -c 3 api.openai.com`

**Issue: "Bot not responding on Telegram"**
- Check logs: `docker-compose logs -f llm-bot` or `docker-compose logs -f nlp-bot`
- Verify token in `.env`
- Ensure container is running: `docker-compose ps`

**Issue: "Out of memory"**
- Increase Docker memory limit in Docker Desktop settings
- Add memory limits to docker-compose.yml

## Best Practices

1. **Always use `.env` for secrets** - Never commit tokens/API keys to git
2. **Monitor logs regularly** - Use `docker-compose logs -f` to catch issues early
3. **Set up health checks** - Bots will auto-restart on failure
4. **Back up results** - Export analysis results regularly
5. **Update dependencies** - Rebuild images when updating requirements.txt

## Testing Deployment

After deployment, test both bots:

1. Open Telegram
2. Search for your NLP bot by username
3. Send `/start` and test with questions
4. Repeat for LLM bot
5. Verify responses and check logs for errors

## Scaling

To run multiple instances (load balancing):

```bash
docker-compose up --scale nlp-bot=3 --scale llm-bot=2
```

**Note:** This works if your Telegram bot tokens support multiple instances.
