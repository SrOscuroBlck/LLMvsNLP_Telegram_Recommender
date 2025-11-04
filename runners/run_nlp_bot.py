#!/usr/bin/env python3

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.common.config import load_nlp_bot_config
from src.common.logger import setup_logger
from src.nlp_bot.bot import NLPBot


def main():
    try:
        config = load_nlp_bot_config()
        setup_logger("nlp_bot", config.log_level)
        
        bot = NLPBot(config)
        bot.run()
        
    except KeyboardInterrupt:
        print("\n🛑 NLP Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting NLP Bot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
