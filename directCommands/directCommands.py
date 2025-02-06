from discord import Message
from random import choice, randint

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