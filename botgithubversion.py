# ============================================================
#  DO NOT REMOVE THIS LINE
#  Made by ItsLukeSter (github.com/ItsLukeSter)
#  Discord: Hello12231223
#  I am not responsible for any issues caused by this bot.
#  Have fun doing anything with this bots code, however please credit me and do not claim it as your own or make malicous changes to it.
#  I have added comments to help you understand the code.
#  © ItsLukeSter 2026
# ============================================================
# Import the Discord library
import discord
# Import commands extension for creating bot commands
from discord.ext import commands
# Import asyncio for background tasks and sleeping
import asyncio
# Import datetime tools for hourly timing
from datetime import datetime, timedelta
# Import random for random food selection
import random
# Import os to read environment variables (for the bot token)
import os

# Enable default Discord intents
intents = discord.Intents.default()
# Allow the bot to read message content (required for commands)
intents.message_content = True

# Create the bot instance with "!" as the command prefix
bot = commands.Bot(command_prefix="!", intents=intents)


# GLOBAL COOLDOWN: 3 seconds for every command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Hey there buddy, you are sending messages WAY too fast. Calm down with a bread 🍞")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("That command doesn't exist, here's a bread! 🍞")
    else:
        raise error


# Event: runs when the bot successfully logs in
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Start the hourly background task
    asyncio.create_task(hourly_on_the_hour())


# Background task: sends a message every hour on the hour
async def hourly_on_the_hour():
    while True:
        now = datetime.now()

        # Calculate the next exact hour
        next_hour = (now + timedelta(hours=1)).replace(
            minute=0, second=0, microsecond=0
        )

        # Calculate how many seconds to wait
        wait_time = (next_hour - now).total_seconds()
        await asyncio.sleep(wait_time)

        # Get the channel by ID
        channel = bot.get_channel(1456866585741361235)
        if channel:
            await channel.send("🌌 A celestial baguette cracks the sky... (Another hour has passed)")


# Command: gives the user a random bread
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def givemebread(ctx):
    breads = ["🍞 White Bread", "🥖 Baguette", "🥯 Bagel", "🍞 Rye", "🥐 Croissant", "🌌🍞🤖 Holographic Bread"]
    legendary = "✨🍞⭐ Legendary Sourbread"

    # 1-in-20 chance for legendary bread
    if random.randint(1, 20) == 1:
        chosen = legendary
    else:
        chosen = random.choice(breads)

    await ctx.send(f"{chosen} — fresh and warm!")


# NEW COMMAND: !pickle
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def pickle(ctx):
    await ctx.send("🥒 Pickle")


# NEW COMMAND: !whomadeyou
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def whomadeyou(ctx):
    await ctx.send("@Hello12231223")


# Command: gives the user cheese with a small chance of mythical cheese
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def givemecheese(ctx):
    normal_cheese = "🧀 Cheesy cheese! (common)"
    mythical_cheese = "🌙🧀✨ Mythical Mooncheese (RARE!)"

    # 3.5% chance for mythical cheese
    if random.random() < 0.035:
        chosen = mythical_cheese
    else:
        chosen = normal_cheese

    await ctx.send(f"{chosen}")


# Command: creates a sandwich with rarity tiers
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def givemesandwich(ctx):
    breads = ["🍞 White Bread", "🥖 Baguette", "🥯 Bagel", "🍞 Rye", "🥐 Croissant", "🌌🍞🤖 Holographic Bread"]
    cheeses = ["🧀 Cheddar", "🧀 Brie", "🧀 Gouda", "🧀 Swiss", "🧀 Mozzarella", "🌟🧀 Mythical Mooncheese"]

    legendary_bread = "✨🍞⭐ Legendary Sourbread"
    mythical_cheese = "🌟🧀 Mythical Mooncheese"

    rainbow_bread = "🌈🍞 Rainbow Bread"
    rainbow_cheese = "🌈🧀 Rainbow Cheese"

    roll = random.random()

    if roll < 0.005:
        bread = rainbow_bread
        cheese = rainbow_cheese
        rarity = "rainbow"

    elif roll < 0.015:
        bread = legendary_bread
        cheese = mythical_cheese
        rarity = "legendary"

    else:
        bread = random.choice(breads)
        cheese = random.choice(cheeses)
        rarity = "normal"

    sandwich = f"{bread} + {cheese}"
    msg = await ctx.send(f"🥪 Your sandwich is ready: {sandwich}!")

    if rarity == "rainbow":
        await msg.add_reaction("🌈")
        await ctx.send("🌈✨ You created the **RAINBOW SANDWICH** — a 0.5% miracle!")

    elif rarity == "legendary":
        await msg.add_reaction("👑")
        await ctx.send("🌌 You’ve discovered the **Legendary Cosmic Sandwich**!")


# Command: random spaghetti + meatballs combo
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def givemespaghettimeatballs(ctx):
    sauces = ["🍅 Tomato Sauce", "🧄 Garlic Sauce", "🌶️ Spicy Arrabbiata", "🧀 Creamy Alfredo"]
    meatballs = ["🥩 Beef Meatballs", "🐔 Chicken Meatballs", "🌱 Veggie Meatballs", "🔥 Inferno Meatballs"]
    extras = ["🧀 Parmesan", "🌿 Basil", "🍄 Mushrooms", "🫒 Olives"]

    sauce = random.choice(sauces)
    ball = random.choice(meatballs)
    extra = random.choice(extras)

    await ctx.send(f"🍝 Your spaghetti is ready: {sauce} + {ball} + {extra}!")


# Command: gives a random food emoji
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def feedme(ctx):
    foods = [
        "🍕", "🍔", "🍟", "🌭", "🍿", "🥪", "🍣", "🍜", "🍝", "🥗",
        "🍩", "🍪", "🍰", "🍦", "🍉", "🍇", "🍓", "🍒", "🥑", "🌮",
        "🍗", "🥟", "🥞", "🧇", "🍤", "🍛", "🍙", "🍧", "🥨", "🍭",
        "🍫", "🍬", "🍮", "🍱", "🥘", "🥙", "🥚", "🍌", "🥝", "🥜"
    ]

    await ctx.send(f"{random.choice(foods)} Eat up!")


# Command: shows the bot's menu
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def bakerymenu(ctx):
    menu = (
        "**🥖 BREAD BOT MENU 🧀**\n"
        "Here’s what I can cook for you:\n\n"
        "🍞 `!givemebread` – Get a random bread\n"
        "🧀 `!givemecheese` – Cheese time\n"
        "🥪 `!givemesandwich` – Bread + cheese combo\n"
        "🍝 `!givemespaghettimeatballs` – Pasta masterpiece\n"
        "🍽️ `!feedme` – Random food emoji snack\n"
        "🥤 `!givemesoda` – Fizzy drink surprise\n"
        "⚔️ `!foodfight @user [--weapon 🍕]` – Battle someone with food\n"
        "🥒 `!pickle` – Pickle\n"
        "🤖 `!whomadeyou` – Creator info\n"
    )
    await ctx.send(menu)


# Command: food fight between two users
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def foodfight(ctx, target: discord.Member, *, weapon=None):
    foods = ["🍕", "🍔", "🍣", "🍩", "🍗", "🍜", "🌮", "🍟", "🥪", "🍝"]

    if weapon is None:
        weapon = random.choice(foods)
    else:
        weapon = weapon.replace("--weapon", "").strip()
        if weapon == "":
            weapon = random.choice(foods)

    winner = random.choice([ctx.author.mention, target.mention])

    await ctx.send(
        f"{ctx.author.mention} attacks {target.mention} with {weapon}!\n"
        f"{winner} won the food fight!"
    )


# Command: gives a random soda
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def givemesoda(ctx):
    sodas = ["🥤 Cola", "🧃 Orange Soda", "🥤 Root Beer", "🧋 Bubble Tea", "🥤 Lemon-Lime"]
    await ctx.send(f"{random.choice(sodas)} — fizzy and refreshing!")


# Command: shows the bot version
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def version(ctx):
    await ctx.send("🍞 bread.bot **V 3.0**, Python Edition")


# Load the bot token from environment variables
token = os.getenv("BOT_TOKEN")
if not token:
    raise RuntimeError("BOT_TOKEN not found in environment variables.")

# Start the bot
bot.run(token) 
