from twitchio import Client
import time

# === Configuration ===

# ⚠️ IMPORTANT: Replace the values below with your own Twitch credentials.
# Do NOT share your actual token publicly!

TOKEN = 'oauth:YOUR_ACCESS_TOKEN_HERE'   # ← Insert your own OAuth token here
BOT_NICK = 'your_bot_name'                # ← Your bot's Twitch username
CHANNEL = 'channel_to_join'                # ← Channel where the bot should connect
YOUR_USERNAME = 'your_username'            # ← Your Twitch username

RESPONSE_COOLDOWN = 30               # Seconds between responses
last_response_time = 0               # Timestamp of the last response


# === Bot class ===
class TangiaBot(Client):
    def __init__(self):
        # Initialize the Client with the token and channels to join
        super().__init__(token=TOKEN, initial_channels=[CHANNEL])

    async def event_ready(self):
        # Called when the bot has successfully connected
        print(f'{BOT_NICK} is connected and listening in channel #{CHANNEL}.')

    async def event_message(self, message):
        global last_response_time

        # Debug: print incoming messages
        if not message.author:
            print('[System message without author] – ignoring.')
            return

        print(f'[{message.author.name}]: {message.content}')

        # Ignore messages sent by the bot itself
        if message.author.name.lower() == BOT_NICK.lower():
            return

        # React to messages from Tangiabot
        if message.author.name.lower() == "tangiabot":
            content = message.content.lower()

            if "started a tangia dungeon" in content and "use !join" in content:
                
                # If you started the dungeon yourself, do nothing
                if YOUR_USERNAME.lower() in content:
                    print("➡️ Detected own dungeon start – no response sent.")
                    return

                now = time.time()
                if now - last_response_time >= RESPONSE_COOLDOWN:
                    await message.channel.send("!join")
                    print("✅ Sent '!join'.")
                    last_response_time = now
                else:
                    cooldown_left = int(RESPONSE_COOLDOWN - (now - last_response_time))
                    print(f"⏳ Cooldown active: {cooldown_left} seconds left.")


# === Run the bot ===
if __name__ == "__main__":
    bot = TangiaBot()
    bot.run()
