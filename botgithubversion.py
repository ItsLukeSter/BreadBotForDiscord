import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.loop.create_task(hourly_on_the_hour())

async def hourly_on_the_hour():
    while True:
        now = datetime.now()

        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

        wait_time = (next_hour - now).total_seconds()
        await asyncio.sleep(wait_time)

        channel = bot.get_channel(1456866585741361235)
        if channel:
            await channel.send("🌌 A celestial baguette cracks the sky... (Another hour has passed)")

        await asyncio.sleep(3600)

import random

@bot.command()
async def givemebread(ctx):
    breads = ["🍞 White Bread", "🥖 Baguette", "🥯 Bagel", "🍞 Rye", "🥐 Croissant"]
    legendary = "✨🍞⭐ Legendary Sourbread"
    if random.randint(1, 20) == 1:
        chosen = legendary
    else:
        chosen = random.choice(breads)
    await ctx.send(f"{chosen} — fresh and warm!")

@bot.command()
async def givemecheese(ctx):
    await ctx.send("🧀Cheesy cheese!")

@bot.command()
async def givemesandwich(ctx):
    breads = ["🍞 White Bread", "🥖 Baguette", "🥯 Bagel", "🍞 Rye", "🥐 Croissant", "✨🍞⭐ Legendary Sourbread"]
    cheeses = ["🧀 Cheddar", "🧀 Brie", "🧀 Gouda", "🧀 Swiss", "🧀 Mozzarella", "🌟🧀 Mythical Mooncheese"]

    bread = random.choice(breads)
    cheese = random.choice(cheeses)

    sandwich = f"{bread} + {cheese}"
    msg = await ctx.send(f"🥪 Your sandwich is ready: {sandwich}!")

    if bread == "✨🍞⭐ Legendary Sourbread" and cheese == "🌟🧀 Mythical Mooncheese":
        await msg.add_reaction("👑")
        await ctx.send("🌌 You’ve discovered the rarest sandwich in the universe!")

@bot.command()
async def givemespaghettimeatballs(ctx):
    sauces = ["🍅 Tomato Sauce", "🧄 Garlic Sauce", "🌶️ Spicy Arrabbiata", "🧀 Creamy Alfredo"]
    meatballs = ["🥩 Beef Meatballs", "🐔 Chicken Meatballs", "🌱 Veggie Meatballs", "🔥 Inferno Meatballs"]
    extras = ["🧀 Parmesan", "🌿 Basil", "🍄 Mushrooms", "🫒 Olives"]

    sauce = random.choice(sauces)
    ball = random.choice(meatballs)
    extra = random.choice(extras)

    await ctx.send(f"🍝 Your spaghetti is ready: {sauce} + {ball} + {extra}!")

@bot.command()
async def feedme(ctx):
    foods = [
        "🍕", "🍔", "🍟", "🌭", "🍿", "🥪", "🍣", "🍜", "🍝", "🥗",
        "🍩", "🍪", "🍰", "🍦", "🍉", "🍇", "🍓", "🍒", "🥑", "🌮",
        "🍗", "🥟", "🥞", "🧇", "🍤", "🍛", "🍙", "🍧", "🥨", "🍭"
    ]

    await ctx.send(f"{random.choice(foods)} Eat up!")

@bot.command()
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
    )
    await ctx.send(menu)

@bot.command()
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

@bot.command()
async def givemesoda(ctx):
    sodas = ["🥤 Cola", "🧃 Orange Soda", "🥤 Root Beer", "🧋 Bubble Tea", "🥤 Lemon-Lime"]
    await ctx.send(f"{random.choice(sodas)} — fizzy and refreshing!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command doesn't exist, here's a bread! 🍞")
    else:
      raise error

import os
bot.run(os.getenv("BOT_TOKEN"))