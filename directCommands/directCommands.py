import discord
from discord import Message
from io import BytesIO
from PIL import Image
from random import randint
import requests


#if you want the bot to generate small fun events, map them to a unique command that starts with "?" and add the function here

async def directCommand(message: Message, message_content: str):
    
    message_content = message_content.lower()

    if message_content == "how big":
        i = randint(1, 10)
        response = "8" + "=" * i + "D"
        await message.channel.send(response)


    elif message_content == "how gay":
        i = randint(0, 100)
        response = str(message.author.mention) + "\nYou are " + str(i) + "%" + " gay"
        await message.channel.send(response)


    elif message_content.startswith("spank"):
        avatar_url = message.author.avatar.url if message.author.avatar else message.author.default_avatar.url
        avatar_response = requests.get(avatar_url)
        if avatar_response.status_code != 200:
            await message.channel.send("Failed to fetch avatar.")
            return
        
        avatar = Image.open(BytesIO(avatar_response.content)).convert("RGBA")
        avatar = avatar.resize((150, 150))
        
        tagged_user = message.mentions[0] if message.mentions else message.author
        tagged_avatar_url = tagged_user.avatar.url if tagged_user.avatar else tagged_user.default_avatar.url
        tagged_avatar_response = requests.get(tagged_avatar_url)

        if tagged_avatar_response.status_code != 200:
            await message.channel.send("Failed to fetch avatar.")
            return

        tagged_avatar = Image.open(BytesIO(tagged_avatar_response.content)).convert("RGBA")
        tagged_avatar = tagged_avatar.resize((150, 150))
        

        try:
            base_image = Image.open("media/dankspank.jpg").convert("RGBA")
        except FileNotFoundError:
            await message.channel.send("Base image not found.")
            return
        
        # Paste avatar onto base image (adjust coordinates as needed)
        base_image.paste(avatar, (220, 5), avatar)
        base_image.paste(tagged_avatar, (330, 200), tagged_avatar)
        
        # Save the edited image to a buffer
        buffer = BytesIO()
        base_image.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Send the edited image
        file = discord.File(buffer, filename="edited_spank.png")
        await message.channel.send(f"{message.author.mention} spanked {tagged_user.mention}", file=file)


    elif message_content == "help":
        response = '''```
Commands:

hello         - bot responds with a hello
hello there   - bot responds with general kenobi
hi            - bot responds with a hi
!new          - bot creates a new psych session
!start        - bot starts the psych round
!stop         - bot stops the psych session
?how big      - ;) try it yourself
?how gay      - ;) try it yourself
?help         - bot responds with a list of commands
```'''

        await message.channel.send(response)