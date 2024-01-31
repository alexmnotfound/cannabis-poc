import sys
import logging
sys.path.append("..")  # Add the parent directory to sys.path
from config.settings import TELEGRAM_API_TOKEN
from bot.my_main_bot import MyMainBot

# Configure path

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Adjust as needed (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Bot started")
    bot = MyMainBot(TELEGRAM_API_TOKEN)
    bot.run()


if __name__ == '__main__':
    main()
