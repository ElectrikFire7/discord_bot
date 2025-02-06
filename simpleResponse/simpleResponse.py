from discord import Message, File

async def simpleResponse(message: Message):

    content = message.content.lower()

    if content == "hello":
        await message.channel.send("Hello!")

    elif content == "hello there":
        await message.channel.send("General Kenobi!")

    elif "how are you" in content:
        await message.channel.send("I'm doing great!")

    elif ("hi " in content) or (" hi" in content) or content == "hi":
        await message.channel.send("FINALLY!! Someone is here")
        await message.channel.send("I was getting bored, and all I could do was")
        await message.channel.send(file = File("media\milk_burst.gif"))