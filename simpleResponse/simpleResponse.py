from discord import Message, File

async def simpleResponse(message: Message):

    content = message.content.lower()

    if content == "hello":
        await message.channel.send("Shalom!")

    elif content == "hello there":
        await message.channel.send("General Kenobi!")

    elif "how are you" in content:
        await message.channel.send("I'm doing great!")

    elif content.startswith("hi ") or content.endswith(" hi") or content == "hi" or " hi " in content:
        await message.channel.send("FINALLY!! Someone is here")
        await message.channel.send("I was getting bored, and all I could do was")
        await message.channel.send(file = File("media/milk_burst.gif"))

    elif "heil hitler" in content:
        await message.channel.send(file = File("media/heil.gif"))

    elif "shalom" in content:
        await message.channel.send("😋🧱")

    elif "allahu akbar" in content:
        await message.channel.send(file = File("media/aha.gif"))