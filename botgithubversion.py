# ==================================
#  DO NOT REMOVE THESE LINES
# © 2026 the-awesome-noob
# Licensed under the MIT License
# Contact: @bread12231223 on Discord
# ==================================
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
# Import sqlite3 for persistent database storage of XP
import sqlite3
# Import math for mathematical formulas in level calculation
import math

# Enable default Discord intents
intents = discord.Intents.default()
# Allow the bot to read message content (required for commands)
intents.message_content = True

# Create the bot instance with "!" as the command prefix
bot = commands.Bot(command_prefix="!", intents=intents)
# Dictionary to track study session start times
session_start = {}

# --- DATABASE SETUP ---
def init_db():
    # Connect to database file
    conn = sqlite3.connect('bread_data.db')
    c = conn.cursor()
    # Create table to store XP if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                  (user_id INTEGER PRIMARY KEY, xp INTEGER DEFAULT 0)''')
    # Table for daily claims
    c.execute('''CREATE TABLE IF NOT EXISTS daily_claims 
                  (user_id INTEGER PRIMARY KEY, last_claim TEXT)''')
    conn.commit()
    conn.close()

# --- SHOP DATABASE SETUP ---
def init_shop_db():
    conn = sqlite3.connect('bread_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS shop 
                  (item_name TEXT PRIMARY KEY, cost INTEGER)''')
    # Add some default items
    c.execute("INSERT OR IGNORE INTO shop VALUES ('Massive Chips Emoji', 500)")
    c.execute("INSERT OR IGNORE INTO shop VALUES ('Massive Bread Emoji', 100)")
    conn.commit()
    conn.close()

# --- HELPER FUNCTIONS ---
def get_user_xp(user_id):
    # Connect and fetch user XP
    conn = sqlite3.connect('bread_data.db')
    c = conn.cursor()
    c.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
    data = c.fetchone()
    conn.close()
    return data[0] if data else 0

def add_xp(user_id, xp_amount):
    # Connect and update user XP
    conn = sqlite3.connect('bread_data.db')
    c = conn.cursor()
    # Insert user if they don't exist, otherwise ignore
    c.execute("INSERT OR IGNORE INTO users (user_id, xp) VALUES (?, 0)", (user_id,))
    # Update user XP
    c.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_amount, user_id))
    conn.commit()
    conn.close()

def xp_to_level(xp):
    # Formula: level = floor(sqrt(xp) / 10) + 1
    return math.floor(math.sqrt(xp) / 10) + 1

# --- LEADERBOARD HELPER ---
def get_leaderboard():
    conn = sqlite3.connect('bread_data.db')
    c = conn.cursor()
    c.execute("SELECT user_id, xp FROM users ORDER BY xp DESC LIMIT 5")
    data = c.fetchall()
    conn.close()
    return data

# GLOBAL COOLDOWN: 3 seconds for every command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            "Hey there buddy, you are sending messages WAY too fast. Calm down with a bread 🍞"
        )
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("That command doesn't exist, here's a bread! 🍞")
    else:
        print(error)

# Event: runs when the bot successfully logs in
@bot.event
async def on_ready():
    init_db()  # Initialize database when bot starts
    init_shop_db() # Initialize shop database
    bot.start_time = datetime.now() # type: ignore
    print(f"Logged in as {bot.user}")
    # Start the hourly background task
    asyncio.create_task(hourly_on_the_hour())

# Event: triggers on every message to handle XP gain
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Gain 5-10 XP per message sent
    xp_gain = random.randint(5, 10)
    add_xp(message.author.id, xp_gain)

    # Process commands
    await bot.process_commands(message)


# Background task: sends a message every hour on the hour
async def hourly_on_the_hour():
    await bot.wait_until_ready()
    while True:
        now = datetime.now()

        # Calculate the next exact hour
        next_hour = (now + timedelta(hours=1)).replace(minute=0,
                                                       second=0,
                                                       microsecond=0)

        # Calculate how many seconds to wait
        wait_time = (next_hour - now).total_seconds()
        await asyncio.sleep(wait_time)

        # Get the channel by ID
        channel = bot.get_channel(
            1462469406645944361)  # Replace with your channel ID

        # FIX: Check if channel is a TextChannel to resolve send() error
        if isinstance(channel, discord.TextChannel):
            await channel.send(
                "🌌 A celestial baguette cracks the sky... (Another hour has passed)"
            )


# Command: gives the user a random bread
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def givemebread(ctx):
    breads = [
        "🍞 White Bread", "🥖 Baguette", "🥯 Bagel", "🍞 Rye", "🥐 Croissant",
        "🌌🍞🤖 Holographic Bread"
    ]
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
    breads = [
        "🍞 White Bread", "🥖 Baguette", "🥯 Bagel", "🍞 Rye", "🥐 Croissant",
        "✨🍞⭐ Legendary Sourbread", "🌌🍞🤖 Holographic Bread", "💎🍞 Diamond Bread",
        "🌈🍞 Rainbow Bread"
    ]
    cheeses = [
        "🧀 Cheddar", "🧀 Brie", "🧀 Gouda", "🧀 Swiss", "🧀 Mozzarella",
        "🌟🧀 Mythical Mooncheese", "🌈🧀 Rainbow Cheese"
    ]

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
        await ctx.send(
            "🌈✨ You created the **RAINBOW SANDWICH** — a 0.5% miracle!")

    elif rarity == "legendary":
        await msg.add_reaction("👑")
        await ctx.send("🌌 You’ve discovered the **Legendary Cosmic Sandwich**!"
                       )


# Command: random spaghetti + meatballs combo
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def givemespaghettimeatballs(ctx):
    sauces = [
        "🍅 Tomato Sauce", "🧄 Garlic Sauce", "🌶️ Spicy Arrabbiata",
        "🧀 Creamy Alfredo"
    ]
    meatballs = [
        "🥩 Beef Meatballs", "🐔 Chicken Meatballs", "🌱 Veggie Meatballs",
        "🔥 Inferno Meatballs"
    ]
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
                "🍕", "🍔", "🍟", "🌭", "🍿", "🥪", "🍣", "🍜", "🍝", "🥗", "🍩", "🍪", "🍰", "🍦",
                "🍉", "🍇", "🍓", "🍒", "🥑", "🌮", "🍗", "🥟", "🥞", "🧇", "🍤", "🍛", "🍙", "🍧",
                "🥨", "🍭", "🍫", "🍬", "🍮", "🍱", "🥘", "🥙", "🥚", "🍌", "🥝", "🥜"
            ]

            await ctx.send(f"{random.choice(foods)} Eat up!")


        # Command: Shows the bot's command menu
        @bot.command(aliases=["cmds"])
        @commands.cooldown(1, 3, commands.BucketType.user)
        async def bakerymenu(ctx):
            embed = discord.Embed(
                title="🥖 BREAD BOT MENU 🧀",
                description="Here’s everything I can cook for you:",
                color=discord.Color.gold()
            )

            embed.add_field(
                name="🍞 Main Kitchen",
                value=(
                    "`!givemebread` – Get a random bread\n"
                    "`!dailybread` – Claim daily XP\n"
                    "`!bakebread` – Bake bread for XP\n"
                    "`!givemecheese` – Cheese time\n"
                    "`!givemesandwich` – Bread + cheese combo\n"
                    "`!givemespaghettimeatballs` – Pasta masterpiece\n"
                    "`!feedme` – Random food emoji snack\n"
                    "`!givemesoda` – Fizzy drink surprise\n"
                    "`!givememorebread` – More bread than you need\n"
                    "`!cook [food]` – Cook something specific\n"
                    "`!exoticbake` – Bake a rare bread\n"
                    "`!givemechips` – Get some crunchy chips\n"
                    "`!eatbread` – Nom nom\n"
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
                    "`!bakeryshop` – Spend XP on goodies\n"
                    "`!bakerquiz` – Test your knowledge!\n"
                    "`!gamblebread` – Risk your bread\n"
                    "`!topping` – Find a topping\n"
                    "`!breadrps` – Rock Paper Scissors\n"
                    "`!pickle` – Just a pickle\n"
                ),
                inline=False
            )

            embed.add_field(
                name="⚔️ Fun & Interaction",
                value=(
                    "`!foodfight @user` – Battle someone\n"
                    "`!stealbread @user` – Steal XP from others\n"
                    "`!toast @user` – Roast someone\n"
                    "`!flavor [text]` – Flavor your text\n"
                    "`!countdown [sec]` – Start a timer\n"
                    "`!breadmarry @user` – Marry another baker!\n"
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
                    "`!breadlevel` – Check your level\n"
                    "`!leaderboard` – See top bakers\n"
                    "`!nextbake` – Time until next celestial hour\n"
                    "`!breadpoem` – Get a small poem\n"
                    "`!magicbreadball [question]` – Ask the oracle\n"
                ),
                inline=False
            )

            embed.set_footer(
                text="Use !bakerymenu or !cmds anytime to see this menu again! (I also may or may not have a secret command 🤫)"
            )

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
        f"{winner} won the food fight!")


# Command: gives a random soda
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def givemesoda(ctx):
    sodas = [
        "🥤 Cola", "🧃 Orange Soda", "🥤 Root Beer", "🧋 Bubble Tea",
        "🥤 Lemon-Lime"
    ]
    await ctx.send(f"{random.choice(sodas)} — fizzy and refreshing!")


# Command: shows the bot version
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def version(ctx):
    await ctx.send("🍞 bread.bot **V 10.0**, Python Edition")


# Command: Secret command that makes the bot say "Shhh.. 🤫"
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def secretbread(ctx):
    await ctx.send("Shhh.. 🤫")


# Command: Sends a random letter from the alphabet
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def letter(ctx):
    letters = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
        "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
    ]
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
    breads = [
        "🍞", "🍞🍞", "🍞🍞🍞", "🍞🍞🍞🍞", "🍞🍞🍞🍞🍞", "🍞🍞🍞🍞🍞🍞", "🍞🍞🍞🍞🍞🍞🍞", "🍞🍞🍞🍞🍞🍞🍞🍞",
        "🍞🍞🍞🍞🍞🍞🍞🍞🍞", "🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞"
    ]
    await ctx.send(random.choice(breads))


# Command: Sends a random emoji
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def emoji(ctx):
    emojis = [
        "😀", "😂", "😍", "😎", "😡", "😢", "😴", "😇", "😈", "😭", "😱", "😳", "😵", "😷",
        "😸", "😹", "😺", "😻", "😼", "😽", "😾", "😿", "🙀", "🙁", "🙂", "🙃", "🙄", "🙅",
        "🙆", "🙇", "🙈", "🙉", "🙊", "🙋", "🙌", "🙍", "🙎", "🙏", "🚶", "🚷", "🚸", "🚹",
        "🚺", "🚻", "🚼", "🚽", "🚾"
    ]
    await ctx.send(random.choice(emojis))


# Command: Shows the bot's uptime
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def uptime(ctx):
    # Using type: ignore here to handle the Pyright error
    delta = datetime.now() - bot.start_time # type: ignore
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    await ctx.send(
        f"🕒 Uptime is {days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)"
    )


# Command: Starts a study session
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def study(ctx):
    # CHECK: See if the user already has a session running
    if ctx.author.id in session_start:
        await ctx.send(
            "🚫 You already have a study session running! Use `!end` before starting a new one."
        )
        return  # This stops the command so the time doesn't get overwritten

    # If the check passes, store the current time
    session_start[ctx.author.id] = datetime.now()
    await ctx.send(
        "📖 Study session started! Focus hard. Use `!end` whenever you are finished!"
    )


# Command: Ends the study session
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def end(ctx):
    # Remove user from dictionary and capture their start time
    start = session_start.pop(ctx.author.id, None)

    # If the user wasn't in the dictionary, they didn't have a session active
    if start is None:
        await ctx.send(
            "You don't have an active study session. Type `!study` to start one!"
        )
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


# Command: Gives a rare bread from a themed list
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def exoticbake(ctx):
    exotic_breads = [
        "🌋🍞 Volcanic Crust Bread", "🌌🍞 Holographic Baguette",
        "✨🍞⭐ Stardust Sourdough", "💎🍞 Diamond-Crusted Roll",
        "☁️🍞 Cloud-Fluff Brioche"
    ]
    await ctx.send(
        f"🧪 **Exotic Experiment Successful!** You baked: **{random.choice(exotic_breads)}**!"
    )


# Command: Play a quick game of rock, paper, scissors (Bread Edition)
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def breadrps(ctx, choice: str):
    choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(choices)
    user_choice = choice.lower()

    if user_choice not in choices:
        await ctx.send("Please choose rock, paper, or scissors!")
        return

    result = ""
    if user_choice == bot_choice:
        result = "It's a tie! 🍞"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "paper" and bot_choice == "rock") or \
         (user_choice == "scissors" and bot_choice == "paper"):
        result = "You win! 🏆"
    else:
        result = "I win! Better luck next time. 🤖"

    await ctx.send(f"I chose **{bot_choice}**. {result}")


# Command: Get a random bread topping
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def topping(ctx):
    toppings = [
        "Butter 🧈", "Jam 🍓", "Peanut Butter 🥜", "Honey 🍯",
        "Garlic Spread 🧄", "Cream Cheese ⚪"
    ]
    await ctx.send(f"Your bread needs: **{random.choice(toppings)}**")


# Command: Calculate the time until the next celestial hour
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def nextbake(ctx):
    now = datetime.now()
    next_hour = (now + timedelta(hours=1)).replace(minute=0,
                                                   second=0,
                                                   microsecond=0)
    remaining = next_hour - now
    minutes = remaining.seconds // 60
    await ctx.send(f"⏳ Next celestial baguette arrives in **{minutes} minutes**!"
                   )


# Command: Gamble your bread emoji
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def gamblebread(ctx):
    if random.random() < 0.5:
        await ctx.send("🎲 **Double Bread!** 🍞🍞")
    else:
        await ctx.send("🎲 **Burnt Bread...** 🍞💥 (Lost it all!)")


# Command: Creates a tiny poem about bread
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def breadpoem(ctx):
    nouns = ["loaf", "crust", "slice", "baguette"]
    adjectives = ["golden", "warm", "fluffy", "tasty"]
    poem = f"Oh, {random.choice(adjectives)} {random.choice(nouns)},\nGiving joy to all the town!"
    await ctx.send(f"📜 **Poem of the Bakery:**\n{poem}")


# Command: Check your bread level
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def breadlevel(ctx):
    # Fetch XP from database
    xp = get_user_xp(ctx.author.id)
    # Calculate level from XP
    level = xp_to_level(xp)

    # Calculate XP needed for next level
    next_level_xp = ((level) * 10)**2
    xp_needed = next_level_xp - xp

    await ctx.send(
        f"📈 **{ctx.author.display_name}**, your current Bread Master Level is: **{level}**!\n"
        f"📊 **Total XP:** {xp} | **XP for next level:** {xp_needed}"
    )

# Command: Show the top 5 bakers
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def leaderboard(ctx):
    data = get_leaderboard()
    description = ""
    for i, (user_id, xp) in enumerate(data):
        user = bot.get_user(user_id)
        name = user.name if user else f"User {user_id}"
        description += f"**{i+1}.** {name} - {xp} XP\n"

    embed = discord.Embed(title="🏆 Top Bakers", description=description, color=discord.Color.gold())
    await ctx.send(embed=embed)


# Command: Set a bread-themed status (Admin only)
@bot.command()
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def setstatus(ctx, *, status: str):
    await bot.change_presence(activity=discord.Game(name=status))
    await ctx.send(f"Status changed to: {status}")


# Command: Ask the magic breadball a question
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def magicbreadball(ctx, *, question):
    responses = [
        "Yes, definitely! 🍞", "Ask again later... 🥖",
        "Don't count on it 🥯", "Absolutely not! 🥐"
    ]
    await ctx.send(
        f"❓ Question: {question}\n🔮 Magic Breadball says: **{random.choice(responses)}**"
    )


# Command: Shows the bakery shop
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def bakeryshop(ctx):
    conn = sqlite3.connect('bread_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM shop")
    items = c.fetchall()
    conn.close()

    embed = discord.Embed(title="🏪 Bakery Shop", description="Spend your hard-earned XP! Use `!buy [item name]`", color=discord.Color.green())
    for item, cost in items:
        embed.add_field(name=item, value=f"Cost: {cost} XP", inline=False)

    await ctx.send(embed=embed)

    # Command: Buy an item from the shop
    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def buy(ctx, *, item_name):
        conn = sqlite3.connect('bread_data.db')
        c = conn.cursor()
        c.execute("SELECT cost FROM shop WHERE item_name = ?", (item_name,))
        item = c.fetchone()

        if not item:
            await ctx.send("That item doesn't exist in the shop!")
            conn.close()
            return

        cost = item[0]
        user_xp = get_user_xp(ctx.author.id)

        if user_xp < cost:
            await ctx.send(f"You don't have enough XP! You need {cost - user_xp} more XP.")
            conn.close()
            return

        # Deduct XP
        add_xp(ctx.author.id, -cost)
        await ctx.send(f"✅ You successfully bought **{item_name}** for {cost} XP!")

        # --- NEW: GIVE ITEM ---
        if item_name == "Massive Chips Emoji":
            await ctx.send("🍟🍟🍟🍟🍟")
        elif item_name == "Massive Bread Emoji":
            await ctx.send("🍞🍞🍞🍞🍞")

        conn.close()

# Command: Quiz
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def bakerquiz(ctx):
    questions = {
        "What is the main ingredient in bread?": "flour",
        "Which ingredient makes bread rise?": "yeast",
        "What do you call a bread maker?": "baker"
    }

    question, answer = random.choice(list(questions.items()))
    await ctx.send(f"❓ **Quiz Time!** {question}")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        response = await bot.wait_for('message', check=check, timeout=15.0)
        if response.content.lower() == answer:
            add_xp(ctx.author.id, 50)
            await ctx.send("✅ Correct! You earned 50 XP!")
        else:
            await ctx.send(f"❌ Wrong! The answer was {answer}.")
    except asyncio.TimeoutError:
        await ctx.send(f"⏰ Time up! The answer was {answer}.")

# Command: Claim daily XP
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def dailybread(ctx):
    user_id = ctx.author.id
    now = datetime.now()

    conn = sqlite3.connect('bread_data.db')
    c = conn.cursor()
    c.execute("SELECT last_claim FROM daily_claims WHERE user_id = ?", (user_id,))
    data = c.fetchone()

    if data:
        last_claim = datetime.fromisoformat(data[0])
        if now - last_claim < timedelta(hours=24):
            remaining = timedelta(hours=24) - (now - last_claim)
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            await ctx.send(f"⏳ You have already claimed your daily bread! Come back in **{hours}h {minutes}m**.")
            conn.close()
            return

    # Claim successful
    xp_gain = 250
    add_xp(user_id, xp_gain)
    c.execute("INSERT OR REPLACE INTO daily_claims VALUES (?, ?)", (user_id, now.isoformat()))
    conn.commit()
    conn.close()
    await ctx.send(f"🥖 **Daily Bread Claimed!** You received **{xp_gain} XP**!")

# Command: Steal XP from another user
@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user) # 1 minute cooldown
async def stealbread(ctx, target: discord.Member):
    if target.bot:
        await ctx.send("🤖 You cannot steal from fellow bots!")
        return
    if target.id == ctx.author.id:
        await ctx.send("🤔 Stealing from yourself? That's not how this works.")
        return

    target_xp = get_user_xp(target.id)
    if target_xp < 50:
        await ctx.send(f"🥖 {target.display_name} doesn't have enough bread to steal!")
        return

    # 50% chance to succeed
    if random.random() < 0.5:
        steal_amount = random.randint(10, 50)
        add_xp(ctx.author.id, steal_amount)
        add_xp(target.id, -steal_amount)
        await ctx.send(f"🥷 **Success!** You stole **{steal_amount} XP** from {target.mention}!")
    else:
        # Penalty for failing
        fail_penalty = 20
        add_xp(ctx.author.id, -fail_penalty)
        await ctx.send(f"👮 **Caught!** You failed to steal from {target.mention} and lost **{fail_penalty} XP** in the process!")

# Command: Bake bread for XP
@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def bakebread(ctx):
    await ctx.send("⏲️ Putting ingredients into the oven... (Wait 5 seconds)")
    await asyncio.sleep(5)

    outcome = random.random()

    if outcome < 0.1: # 10% chance to burn
        await ctx.send("🔥 **Oh no!** The bread is burnt! (No XP gained)")
    elif outcome < 0.6: # 50% chance to succeed
        add_xp(ctx.author.id, 50)
        await ctx.send("🍞 **Nice!** You baked some decent bread. (+50 XP)")
    elif outcome < 0.95: # 35% chance to excel
        add_xp(ctx.author.id, 100)
        await ctx.send("🥖 **Fantastic!** A perfect baguette! (+100 XP)")
    else: # 5% chance to go legendary
        add_xp(ctx.author.id, 500)
        await ctx.send("✨ **LEGENDARY BREAD!** The bakery smells heavenly! (+500 XP)")

# Command: Gives a random chip with rarities
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def givemechips(ctx):
    # Define chip rarities
    normal_chips = ["🥔 Classic Potato", "🥨 Crunchy Pretzel", "🧀 Cheddar Nachos"]
    rare_chips = ["🌶️ Hot Chili Chips", "🌮 Spicy Taco"]
    legendary_chips = ["🌌💎 Galactic Sea Salt & Vinegar Chips"]

    # Roll for rarity (80% normal, 15% rare, 5% legendary)
    roll = random.random()
    if roll < 0.80:
        chosen = random.choice(normal_chips)
        rarity = "Normal"
    elif roll < 0.95:
        chosen = random.choice(rare_chips)
        rarity = "Rare"
    else:
        chosen = random.choice(legendary_chips)
        rarity = "LEGENDARY"

    await ctx.send(f"🛍️ You opened a bag of chips and found: **{chosen}** ({rarity})!")

# Command: Eat a bread
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def eatbread(ctx):
    await ctx.send("🍞 *Nom nom nom* You ate a bread.")


# Load the bot token from environment variables
token = os.getenv("BOT_TOKEN")
if not token:
    raise RuntimeError("BOT_TOKEN not found in environment variables.")

# Start the bot
bot.run(token)
