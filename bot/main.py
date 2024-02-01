import sys
sys.path.append("..")  # Add the parent directory to sys.path
import logging, json
from bot.my_main_bot import MyMainBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Adjust as needed (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting bot")
    with open('../credentials.json') as config_file:
        config = json.load(config_file)

    bot = MyMainBot(config)
    bot.run()


if __name__ == '__main__':
    main()
