from discord import Message
from directCommands.directCommands import directCommand
from simpleResponse.simpleResponse import simpleResponse
from psychCommands.psychCommands import psychCommand
from pokerCommands.poker import pokerCommand

async def controller (message: Message, sessions, client) -> None:

    user_message: str = str(message.content)

    if not user_message:
        print("Intents were not enabled")
        return False

    #if the message starts with a question mark, it is a direct command
    #check directCommands folder
    if user_message[0] == '?':
        user_message = user_message[1:]
        await directCommand(message, user_message)

    if user_message[0] == '!':
        user_message = user_message[1:]
        await psychCommand(message, user_message, sessions, client)

    if user_message[0] == '#':
        user_message = user_message[1:]
        await pokerCommand(message, user_message, sessions, client)

    #if the message has no starting tag, it has a few fun responses
    #check simpleResponse folder
    else:
        await simpleResponse(message)

    return True

