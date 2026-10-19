import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import json
import os
import time
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

PREDEFINED_MESSAGE = "https://discord.gg/katana00 for the win."
ACCESS_DATA_FILE = Path("bot_access.json")


def load_access_data():
    try:
        with ACCESS_DATA_FILE.open(encoding="utf-8") as access_file:
            access_data = json.load(access_file)
    except (FileNotFoundError, json.JSONDecodeError):
        access_data = {}

    configured_owner_ids = {
        int(owner_id.strip())
        for owner_id in os.getenv("OWNER_IDS", "").split(",")
        if owner_id.strip().isdigit()
    }
    owner_ids = configured_owner_ids | {
        int(owner_id) for owner_id in access_data.get("owner_ids", [])
    }
    premium_user_ids = {
        int(user_id) for user_id in access_data.get("premium_user_ids", [])
    }
    return owner_ids, premium_user_ids


def save_access_data():
    with ACCESS_DATA_FILE.open("w", encoding="utf-8") as access_file:
        json.dump({
            "owner_ids": sorted(bot.owner_ids),
            "premium_user_ids": sorted(bot.premium_user_ids),
        }, access_file, indent=2)


def is_owner(user_id: int) -> bool:
    return user_id in bot.owner_ids


def is_premium(user_id: int) -> bool:
    return is_owner(user_id) or user_id in bot.premium_user_ids


async def require_premium(interaction: discord.Interaction) -> bool:
    if is_premium(interaction.user.id):
        return True

    await interaction.response.send_message(
        "This command is available to premium users only.",
        ephemeral=True
    )
    return False


async def require_owner(interaction: discord.Interaction) -> bool:
    if is_owner(interaction.user.id):
        return True

    await interaction.response.send_message(
        "This command is available to bot owners only.",
        ephemeral=True
    )
    return False

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.command_cooldowns = {} 
        self.owner_ids, self.premium_user_ids = load_access_data()

    async def setup_hook(self):
        try:
            await self.tree.sync()
            print("Commands synced successfully.")
        except Exception as e:
            print(f"Error syncing commands: {e}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.tree.command(name="spam", description="Sends the predefined message five times")
async def spamfixed(interaction: discord.Interaction):
    try:
        user_id = interaction.user.id
        cooldown_time = 4

        last_used = bot.command_cooldowns.get(user_id, 0)
        time_since_last_use = time.time() - last_used

        if time_since_last_use < cooldown_time:
            remaining_time = cooldown_time - time_since_last_use
            await interaction.response.send_message(
                f"Please wait **{remaining_time:.1f} seconds** before using this command again.",
                ephemeral=True
            )
            return

        bot.command_cooldowns[user_id] = time.time()
        await interaction.response.send_message("Fixed message sent.", ephemeral=True)

        for _ in range(5):
            await asyncio.sleep(0.15)
            await interaction.followup.send(PREDEFINED_MESSAGE)

    except discord.Forbidden:
        print("The bot lacks permissions to send messages.")
    except discord.HTTPException as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

@bot.tree.command(name="addpremium", description="Grant a user premium access")
async def addpremium(interaction: discord.Interaction, user: discord.User):
    if not await require_owner(interaction):
        return

    bot.premium_user_ids.add(user.id)
    save_access_data()
    await interaction.response.send_message(
        f"Premium access granted to {user.mention}.",
        ephemeral=True
    )

@bot.tree.command(name="removepremium", description="Remove a user's premium access")
async def removepremium(interaction: discord.Interaction, user: discord.User):
    if not await require_owner(interaction):
        return

    bot.premium_user_ids.discard(user.id)
    save_access_data()
    await interaction.response.send_message(
        f"Premium access removed from {user.mention}.",
        ephemeral=True
    )

@bot.tree.command(name="addowner", description="Grant bot owner access to a user")
async def addowner(interaction: discord.Interaction, user: discord.User):
    if not await require_owner(interaction):
        return

    bot.owner_ids.add(user.id)
    save_access_data()
    await interaction.response.send_message(
        f"Owner access granted to {user.mention}.",
        ephemeral=True
    )

COLOR_MAP = {
    "red": discord.Color.from_rgb(255, 0, 0),
    "blue": discord.Color.from_rgb(0, 100, 255),
    "green": discord.Color.from_rgb(0, 200, 0),
    "yellow": discord.Color.from_rgb(255, 255, 0),
    "purple": discord.Color.from_rgb(160, 0, 255),
    "orange": discord.Color.from_rgb(255, 165, 0),
}

@bot.tree.command(name="sendembed", description="Sends an embed with your message, a color, and an optional file")
@app_commands.describe(
    title="The title of the embed",
    message="The message to include in the embed",
    color="Choose the embed color",
    amount="Number of messages to send (1-30)",
    file="Optional file to attach"
)
@app_commands.choices(color=[
    app_commands.Choice(name="Red", value="red"),
    app_commands.Choice(name="Blue", value="blue"),
    app_commands.Choice(name="Green", value="green"),
    app_commands.Choice(name="Yellow", value="yellow"),
    app_commands.Choice(name="Purple", value="purple"),
    app_commands.Choice(name="Orange", value="orange"),
])
async def sendembed(
    interaction: discord.Interaction,
    title: str,
    message: str,
    color: app_commands.Choice[str],
    amount: app_commands.Range[int, 1, 30],
    file: Optional[discord.Attachment] = None
):
    try:
        if not await require_premium(interaction):
            return

        await interaction.response.send_message("Embed sent.", ephemeral=True)

        embed_color = COLOR_MAP.get(color.value, discord.Color.from_rgb(255, 255, 255))
        formatted_message = message.replace("\\n", "\n")

        embed = discord.Embed(
            title=title,
            description=formatted_message,
            color=embed_color
        )

        for _ in range(amount):
            file_to_send = await file.to_file() if file else None

            if file_to_send:
                await interaction.followup.send(embed=embed, file=file_to_send)
            else:
                await interaction.followup.send(embed=embed)

    except discord.Forbidden:
        print("The bot lacks permissions to send messages.")
    except discord.HTTPException as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

@bot.tree.command(name="sendmessage", description="Sends a plain text message with an optional file")
@app_commands.describe(
    message="The message to send",
    amount="Number of messages to send (1-30)",
    file="Optional file to attach"
)
async def sendmessage(
    interaction: discord.Interaction,
    message: str,
    amount: app_commands.Range[int, 1, 30],
    file: Optional[discord.Attachment] = None
):
    try:
        if not await require_premium(interaction):
            return

        await interaction.response.send_message("Message sent.", ephemeral=True)

        formatted_message = message.replace("\\n", "\n")

        for _ in range(amount):
            file_to_send = await file.to_file() if file else None

            if file_to_send:
                await interaction.followup.send(content=formatted_message, file=file_to_send)
            else:
                await interaction.followup.send(content=formatted_message)

    except discord.Forbidden:
        print("The bot lacks permissions to send messages.")
    except discord.HTTPException as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

token = os.getenv("DISCORD_TOKEN")

if not token:
    raise RuntimeError("DISCORD_TOKEN is not set. Add it to a .env file.")

bot.run(token)
