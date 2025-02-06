import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from controller import controller


load_dotenv()
TOKEN: str = os.getenv("TOKEN")

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


@client.event
async def on_ready() -> None:
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    await controller(message)


def main() -> None:
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()