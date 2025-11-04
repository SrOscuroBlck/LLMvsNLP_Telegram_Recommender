#!/usr/bin/env python3

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.common.config import load_llm_bot_config
from src.common.logger import setup_logger
from src.llm_bot.bot import LLMBot


def main():
    try:
        config = load_llm_bot_config()
        setup_logger("llm_bot", config.log_level)
        
        bot = LLMBot(config)
        bot.run()
        
    except KeyboardInterrupt:
        print("\n🛑 LLM Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting LLM Bot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
