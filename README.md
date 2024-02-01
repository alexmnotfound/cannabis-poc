# Cannabinoid POC AI Assitance with Telegram integration Bot

---

## Purpose
This Telegram Bot serves as a virtual assistant, leveraging GroundX's search functionality and OpenAI's language model to provide users with information on various topics directly through Telegram.

---

The bot uses GroundX API to search for content within a specified project and then employs OpenAI's GPT model to generate a human-like response based on the search results. The integration allows for a seamless flow of information, making it an effective tool for users seeking quick and detailed answers. The project makes use of the python-telegram-bot library for Telegram interactions, groundx for accessing the GroundX API, and openai for generating responses with OpenAI.

This Telegram bot offers a convenient way for users to obtain information and clarifications on the go, directly from their Telegram application.

## Configuration Process
Before running the bot, you need to set up the necessary configuration:

### Credentials
Create a `credentials.json` file inside the parent folder with the following structure, filling in your respective API keys and project information:

```json
{
    "groundx": {
        "api_key": "YOUR_GROUNDX_API_KEY",
        "project_id": "YOUR_GROUNDX_PROJECT_ID",
        "bucket_id": "YOUR_GROUNDX_BUCKET_ID"
    },
    "openai": {
        "api_key": "YOUR_OPENAI_API_KEY"
    },
    "telegram": {
        "api_key": "YOUR_TELEGRAM_API_KEY",
        "authorized_chat_ids": ["CHAT_ID_1", "CHAT_ID_2"]
    }
}
```

Ensure this file is stored securely and is not exposed publicly, as it contains sensitive information.

### Telegram integration

1. Create a Telegram Bot & Get the Token
   * Open your **Telegram** application.
   * Search for `@BotFather` in the search bar (it is a bot provided by Telegram).
   * Start a chat with BotFather by clicking `Start`.
   * Create a **new bot** by sending the following command to **BotFather**: `/newbot`.
   * **BotFather** will ask you to provide a name for your bot. After you answer, it will ask for a username as well. The username must end in `bot`. For example, “MyTestBot” or “my_test_bot”.
   * After completing the bot creation, **BotFather** will provide you with your bot's token. This `token` is a string that looks something like `123456789:AAG90e14-0f8-40183D-18491dDE`.
   * Copy this token and keep it secure. Never share it with anyone.
2. Find Your Chat or Group ID
   * If you haven't done so already during the bot creation process, search for your bot on Telegram (by the username you provided) and start a conversation with it by clicking `Start`.
   * If you want to send messages to a group, add the bot to the group.
   * To get your chat or group ID, use any web browser to navigate to the following URL: `https://api.telegram.org/bot<YourBOTToken>/getUpdates` (replace <YourBOTToken> with the token you received from BotFather).
   * Send a message to the bot or group. You don't have to do this every time, just once to make it appear in the update's page.
   * Refresh the page, and you'll see an array of all your bot’s interactions. Look for the "chat" object in the array; within it, you can find `id`. This number (might be negative for groups) is your chat or group ID.
   * Copy this ID for usage in your script.

--- 

## How to run it
I personally recommend it to run it in a virtual environment, as follows:
1. Open a command prompt or terminal window.
2. Navigate to the directory where you want to create the virtual environment. You can use the `cd` command to change directories.
3. Enter the following command to create a new virtual environment: `python3 -m venv venv`, replacing "venv" with the name you want to give to your virtual environment.
4. Activate the virtual environment by entering the following command (Linux environments): `source venv/bin/activate`
5. Once the virtual environment is activated, you can install Python packages using `pip` as usual. For example, to install the all the packages, 
you can enter the following command: `pip3 install -r requirements.txt`
6. Assuming you're on the project's folder, now you can run `python3 main.py`
7. When you're done using the virtual environment, you can deactivate it by entering the following command: `deactivate`


---

## Additional Information
* Ensure the config.json is in the same directory as main.py.


## References
  * [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
  * [Telegram API](https://core.telegram.org/bots/api)
  * [GroundX API](https://documentation.groundx.ai/r)
  * [OpenAI API](https://platform.openai.com/docs/)
