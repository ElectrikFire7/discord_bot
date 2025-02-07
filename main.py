import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, Reaction, User
from controller import controller


load_dotenv()
TOKEN: str = os.getenv("TOKEN")

sessions = []

intents: Intents = Intents.default()
intents.members = True
intents.reactions = True
intents.message_content = True
client: Client = Client(intents=intents)


@client.event
async def on_ready() -> None:
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    await controller(message, sessions, client)

@client.event
async def on_reaction_add(reaction: Reaction, user: User):
    if user.bot:  
        return

    if str(reaction.emoji) == "👍" and reaction.message.content == "React 👍 to join game":
        for session in sessions:
            if session.channel == reaction.message.channel:
                session.add_player(user)

@client.event
async def on_reaction_remove(reaction: Reaction, user: User):
    print(user)
    if user.bot:
        return

    if str(reaction.emoji) == "👍" and reaction.message.content == "React 👍 to join game":
        for session in sessions:
            if session.channel == reaction.message.channel:
                session.remove_player(user)


def main() -> None:
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()