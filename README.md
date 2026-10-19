# Discord-SpamBot

An discord bot for spam on any server with no permissions.

# SETUP

- Python (PIP)
  - Open cmd and go to the project folder using CD on windows or linux and run the following command.
  - pip install -r requirements.txt
    - (Only is discord pip req.)

- Discord Developer Portal
  - 1- Go to: https://discord.com/developers/applications
  - 2- Create new application.
  - 3- Go to bot options (in the bot) and enable messages, presence, and server intents.
  - 4- Go to the install option and copy the installation link using the option (Discord Provide Link).
    - Example: https://discord.com/oauth2/authorize?client_id=BOTID
  - 5- Paste it into any Discord or web channel and add it to your apps.
  - 6- Create a `.env` file in the project folder and add `DISCORD_TOKEN=YOUR_BOT_TOKEN`.
  - 7- Add your Discord user ID to the `.env` file as `OWNER_IDS=YOUR_DISCORD_USER_ID`. Multiple owner IDs can be comma-separated.
  - 8- Once you've done all this and added the app to your Discord account, use `/spam`, `/sendembed`, or `/sendmessage`.

The `/spam` command sends the message stored in `PREDEFINED_MESSAGE` in `bot.py` five times. `/sendembed` and `/sendmessage` require premium access and accept between 1 and 30 messages.

Owners can use `/addpremium`, `/removepremium`, and `/addowner`. Premium users and added owners are stored in `bot_access.json`.

# DISCLAIMER  

- For educational purposes only. The author is not responsible for any misuse of this content.
- In order for the bot to be able to spam on that channel, it must be enabled "Use external applications". This comes by default in any discord channel. Be careful with this on your Discord server.# Discord-SpamBot

An discord bot for spam on any server with no permissions.

# SETUP

- Python (PIP)
  - Open cmd and go to the project folder using CD on windows or linux and run the following command.
  - pip install -r requirements.txt
    - (Only is discord pip req.)

- Discord Developer Portal
  - 1- Go to: https://discord.com/developers/applications
  - 2- Create new application.
  - 3- Go to bot options (in the bot) and enable messages, presence, and server intents.
  - 4- Go to the install option and copy the installation link using the option (Discord Provide Link).
    - Example: https://discord.com/oauth2/authorize?client_id=BOTID
  - 5- Paste it into any Discord or web channel and add it to your apps.
  - 6- Create a `.env` file in the project folder and add `DISCORD_TOKEN=YOUR_BOT_TOKEN`.
  - 7- Once you've done all this and added the app to your Discord account, simply go to a random channel on Discord server you want and run /spamcustom `THE_TEXT_YOU_WANT`, /spamfixed, or /sendembed.

The `/spamfixed` command sends the message stored in `PREDEFINED_MESSAGE` in `bot.py` five times. Edit that constant to change the message.

# DISCLAIMER  

- For educational purposes only. The author is not responsible for any misuse of this content.
- In order for the bot to be able to spam on that channel, it must be enabled "Use external applications". This comes by default in any discord channel. Be careful with this on your Discord server.
