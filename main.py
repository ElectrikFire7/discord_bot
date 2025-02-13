import os
import threading
from flask import Flask, jsonify, redirect
from dotenv import load_dotenv
from discord import Intents, Client, Message, Reaction, User
from controller import controller


load_dotenv()
TOKEN: str = os.getenv("TOKEN")
INVITE_URL = os.getenv("INVITE_URL")

sessions = []

intents: Intents = Intents.default()
intents.members = True
intents.reactions = True
intents.message_content = True
client: Client = Client(intents=intents)

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "running"}), 200

@app.route("/invite", methods=["GET"])
def invite_bot():
    invite_url = f"{INVITE_URL}"
    return redirect(invite_url)


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

@client.event
async def on_disconnect():
    print("Bot has disconnected from Discord!")


def run_flask():
    app.run(host="0.0.0.0", port=5000)

def run_discord_bot():
    if os.environ.get("RUNNING_IN_RENDER"):
        print("Bot is already running, skipping duplicate start.")
        return
    
    os.environ["RUNNING_IN_RENDER"] = "True" 
    client.run(TOKEN)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_discord_bot()