import os
import threading, requests, time
from flask import Flask, jsonify, redirect
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message, Reaction, User # type: ignore
from controller import controller
import aiohttp


load_dotenv()
TOKEN: str = os.getenv("TOKEN")
INVITE_URL = os.getenv("INVITE_URL")

sessions = []
status = "running"

intents: Intents = Intents.default()
intents.members = True
intents.reactions = True
intents.message_content = True
client: Client = Client(intents=intents)

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": f"{status}" }), 200

@app.route("/invite", methods=["GET"])
def invite_bot():
    invite_url = f"{INVITE_URL}"
    return redirect(invite_url)


@client.event
async def on_ready() -> None:
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message: Message) -> None:    
    
    #checks rate limit after every message it sends
    if message.author == client.user:
        url = "https://discord.com/api/v10/users/@me"
        headers = {"Authorization": f"Bot {TOKEN}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:

                if(response.status != 200):
                    print("Failed to get bot")
                    print(f"Status Code: {type(response.status)}")
                    return

                limit = response.headers.get('X-RateLimit-Limit')
                remaining = response.headers.get('X-RateLimit-Remaining')
                reset_after = response.headers.get('X-RateLimit-Reset-After')
                reset_time = response.headers.get('X-RateLimit-Reset')

                if(int(remaining) <= 0):
                    print(f"Total Requests Allowed: {limit}")
                    print(f"Requests Remaining: {remaining}")
                    print(f"Resets in: {reset_after} seconds")
                    print(f"Resets at: {time.ctime(float(reset_time))}")
                    status = "rate limited"
                    return

                elif(int(remaining) < 100):
                    print("Rate limit safety reached")
                    status = "rate limit safety reached"
                    return
                
                else:
                    status = "running"
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

def keep_alive():
    url = "https://discord-bot-xy9q.onrender.com/health"
    while True:
        try:
            requests.get(url)
            print("Sent keep-alive ping")
        except:
            print("Failed to send ping")

        time.sleep(780)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    run_discord_bot()