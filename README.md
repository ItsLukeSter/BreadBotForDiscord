# BreadBotForDiscord Bot Template

Follow these steps to get your own instance of Bread Bot running:
1. Create the Bot Application

Go to the Discord Developer Portal by clicking [here.](https://discord.com/developers/applications)

Click "New Application" and name it bread.bot.

Go to the "Bot" tab on the left.

Click "Add Bot" and confirm.

Under the "Token" section, click "Reset Token" and copy the token immediately. Keep this token secret!

Enable "MESSAGE CONTENT INTENT" further down on the same page.

2. Download the Files

Go to the Releases page by clicking [here.](https://github.com/the-awesome-noob/BreadBotForDiscord/releases)

Download botgithubversion.py and requirements.txt from the latest release.

3. Configure and Run

Make sure you have Python installed. If you don't, download it by clicking [here.](https://www.python.org/)

Open your terminal or command prompt in the folder where you downloaded the files.

Install the required library:

pip install -r requirements.txt

Set your Bot Token as an environment variable (replace YOUR_TOKEN_HERE):

Windows (PowerShell): $env:BOT_TOKEN="YOUR_TOKEN_HERE"

Run the bot (replace version_number with the version number (e.g, V9.0) and make sure the filename's match.):

python botgithubversionVversion_number.py
