from discord import Message
from random import randint


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