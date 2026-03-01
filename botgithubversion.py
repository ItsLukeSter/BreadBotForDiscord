# ======================================================================================================================================
#  DO NOT REMOVE THESE LINES
#  Made by the-awesome-noob (github.com/the-awesome-noob)
#  Discord: @bread12231223
#  I am not responsible for any issues caused by this bot.
#  Have fun doing anything with this bots code, however please credit me and do not claim it as your own or make malicous changes to it.
#  I have added comments to help you understand the code.
#  © the-awesome-noob 2026
# ======================================================================================================================================
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
# Dictionary to track study session start times
session_start = {}

# GLOBAL COOLDOWN: 3 seconds for every command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Hey there buddy, you are sending messages WAY too fast. Calm down with a bread 🍞")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("That command doesn't exist, here's a bread! 🍞")
    else:
        print(error)


# Event: runs when the bot successfully logs in
@bot.event
async def on_ready():
    bot.start_time = datetime.now()
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
        channel = bot.get_channel(1462469406645944361) # Replace with your channel ID
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


# Command: !pickle
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def pickle(ctx):
    await ctx.send("🥒 Pickle")


# Command: !whomadeyou
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def whomadeyou(ctx):
    await ctx.send("I was baked in the oven by <@1363752887674732688>")


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
    breads = ["🍞 White Bread", "🥖 Baguette", "🥯 Bagel", "🍞 Rye", "🥐 Croissant", "✨🍞⭐ Legendary Sourbread", "🌌🍞🤖 Holographic Bread", "💎🍞 Diamond Bread", "🌈🍞 Rainbow Bread"]
    cheeses = ["🧀 Cheddar", "🧀 Brie", "🧀 Gouda", "🧀 Swiss", "🧀 Mozzarella", "🌟🧀 Mythical Mooncheese", "🌈🧀 Rainbow Cheese"]

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

# Command: Shows the bot's command menu (FIXED INDENTATION)
@bot.command(aliases=["cmds"])
@commands.cooldown(1, 3, commands.BucketType.user)
async def bakerymenu(ctx):
    embed = discord.Embed(
        title="🥖 BREAD BOT MENU 🧀",
        description="Here’s everything I can cook for you in **Version 9.0**:",
        color=discord.Color.gold()
    )

    embed.add_field(
        name="🍞 Main Kitchen",
        value=(
            "`!givemebread` – Get a random bread\n"
            "`!givemecheese` – Cheese time\n"
            "`!givemesandwich` – Bread + cheese combo\n"
            "`!givemespaghettimeatballs` – Pasta masterpiece\n"
            "`!feedme` – Random food emoji snack\n"
            "`!givemesoda` – Fizzy drink surprise\n"
            "`!givememorebread` – More bread than you need\n"
            "`!cook [food]` – Cook something specific\n"
        ),
        inline=False
    )

    embed.add_field(
        name="🎲 Bakery Games",
        value=(
            "`!number` – Random number 1–10\n"
            "`!letter` – Random letter\n"
            "`!emoji` – Random emoji\n"
            "`!recipe` – Get a random baking recipe\n"
        ),
        inline=False
    )

    embed.add_field(
        name="⚔️ Fun & Interaction",
        value=(
            "`!foodfight @user` – Battle someone\n"
            "`!toast @user` – Roast someone\n"
            "`!flavor [text]` – Flavor your text\n"
            "`!countdown [sec]` – Start a timer\n"
        ),
        inline=False
    )

    embed.add_field(
        name="📚 Study System",
        value=(
            "`!study` – Starts a study session\n"
            "`!end` – Ends the study session\n"
        ),
        inline=False
    )

    embed.add_field(
        name="⚙️ Utility",
        value=(
            "`!uptime` – Bot uptime\n"
            "`!version` – Show bot version\n"
            "`!whomadeyou` – Creator info\n"
        ),
        inline=False
    )

    embed.set_footer(text="Use !bakerymenu or !cmds anytime to see this menu again! (I also may or may not have a secret command 🤫)")

    await ctx.send(embed=embed)


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
    await ctx.send("🍞 bread.bot **V 9.0**, Python Edition")


# Command: Secret command that makes the bot say "Shhh.. 🤫"
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def secretbread(ctx):
    await ctx.send("Shhh.. 🤫")

# Command: Sends a random letter from the alphabet
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def letter(ctx):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    await ctx.send(f"{random.choice(letters)}")


# Command: Sends a random number from 1 to 10
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def number(ctx):
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    await ctx.send(f"{random.choice(numbers)}")


# Command: Generates a random amount of bread
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def givememorebread(ctx):
    breads = ["🍞", "🍞🍞", "🍞🍞🍞", "🍞🍞🍞🍞", "🍞🍞🍞🍞🍞", "🍞🍞🍞🍞🍞🍞", "🍞🍞🍞🍞🍞🍞🍞", "🍞🍞🍞🍞🍞🍞🍞🍞", "🍞🍞🍞🍞🍞🍞🍞🍞🍞", "🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞"]
    await ctx.send(random.choice(breads))


# Command: Sends a random emoji
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def emoji(ctx):
    emojis = [
        "😀", "😂", "😍", "😎", "😡", "😢", "😴", "😇", "😈", "😭", "😱", "😳",
        "😵", "😷", "😸", "😹", "😺", "😻", "😼", "😽", "😾", "😿", "🙀",
        "🙁", "🙂", "🙃", "🙄", "🙅", "🙆", "🙇", "🙈", "🙉", "🙊", "🙋",
        "🙌", "🙍", "🙎", "🙏", "🚶", "🚷", "🚸", "🚹", "🚺", "🚻", "🚼",
        "🚽", "🚾"
    ]
    await ctx.send(random.choice(emojis))

# Command: Shows the bot's uptime
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def uptime(ctx):
    delta = datetime.now() - bot.start_time
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    await ctx.send(f"🕒 Uptime is {days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)")

# Command: Starts a study session
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def study(ctx):
    # CHECK: See if the user already has a session running
    if ctx.author.id in session_start:
        await ctx.send("🚫 You already have a study session running! Use `!end` before starting a new one.")
        return # This stops the command so the time doesn't get overwritten

    # If the check passes, store the current time
    session_start[ctx.author.id] = datetime.now()
    await ctx.send("📖 Study session started! Focus hard. Use `!end` whenever you are finished!")


# Command: Ends the study session
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def end(ctx):
    # Remove user from dictionary and capture their start time
    start = session_start.pop(ctx.author.id, None)

    # If the user wasn't in the dictionary, they didn't have a session active
    if start is None:
        await ctx.send("You don't have an active study session. Type `!study` to start one!")
        return

    # Calculate time difference between now and the stored start time
    duration = datetime.now() - start
    total_seconds = int(duration.total_seconds())

    # Math to break down total seconds into H/M/S
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # The bot will accurately show how many hours you studied
    await ctx.send(
        f"✅ Session ended! You studied for **{hours} hour(s), {minutes} minute(s) and {seconds} second(s)**. Great work!"
    )

# Command: !countdown
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def countdown(ctx, seconds: int):
    if seconds <= 0:
        await ctx.send("Please provide a positive number of seconds.")
        return
    await ctx.send(f"Countdown started for {seconds} seconds!")
    for i in range(seconds, 0, -1):
        await ctx.send(f"{i}...")
        await asyncio.sleep(1)

    # Send this once the loop finishes
    await ctx.send("Time's up! 🎉")


# Command: Bot cook the requested food
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def cook(ctx, *, food):
    await ctx.send(f"👨‍🍳 Putting **{food}** into the oven... *bzzt*...")
    await asyncio.sleep(2)
    await ctx.send(f"🛎️ Ding! Your **{food}** is ready!")

# Command: Gives a random fake recipe
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def recipe(ctx):
    recipes = [
        "How to make Bread: Take flour, water, and a jetpack. Mix them together and boom! Bread!",
        "How to make a Sandwich: Put bread on bread. Add cheese and add more cheese pickles more cheese some more cheese and top it off with some more cheese",
        "How to make Pizza: Drop cheese on dough then add sauce and sauce and some sauce and add some tomatoes and cheese"
    ]
    await ctx.send(f"📜 **Random Recipe:** {random.choice(recipes)}")

# Command: Roasts a user
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def toast(ctx, target: discord.Member):
    roasts = [
        f"🔥 *Toasts {target.mention}* — You are a tomato",
        f"🔥 *Toasts {target.mention}* — Someone left you in the oven for too long now your burnt haha",
        f"🔥 *Toasts {target.mention}* — Someone forgot to toast you and now they are super duper sad",
        f"🔥 *Toasts {target.mention}* — You are a moldy bread on milk",
        f"🔥 *Toasts {target.mention}* — hello there, you look like a burnt piece of bread"
    ]
    await ctx.send(random.choice(roasts))

# Command: Adds bread emojis around text
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def flavor(ctx, *, text):
    await ctx.send(f"🍞 {text} 🍞")

# Load the bot token from environment variables
token = os.getenv("BOT_TOKEN")
if not token:
    raise RuntimeError("BOT_TOKEN not found in environment variables.")

# Start the bot
bot.run(token)
