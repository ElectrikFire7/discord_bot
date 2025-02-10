import discord
from discord import Message
from psychCommands.PsychSession import PsychSession
import asyncio
import random


async def psychCommand(message: Message, user_message: str, sessions, client) -> None:
    
    if user_message == "new":
        if any(session.channel == message.channel for session in sessions):
            await message.channel.send("Game session already exists in this channel")
            return

        psychSession = PsychSession(message.channel, message.author)
        sessions.append(psychSession)
        
        sent_message = await message.channel.send("React 👍 to join game")  
        await sent_message.add_reaction("👍")


    if user_message == "start":
        #checks before sarting a round
        gameSession = None
        for session in sessions:
            if session.channel == message.channel:

                if session.host != message.author:
                    await message.channel.send("Only the host can start the game")
                    return
                
                gameSession = session

                if gameSession.playing:
                    await message.channel.send("Round already started")
                    return
                
                gameSession.playing = True
                break

        if gameSession is None:
            await message.channel.send("No game session found. Use '!new' to create a session")
            return


        #starting round and response collection
        prompt = gameSession.generate_prompt() 
        tasks = []  


        async def ask_player(player):
            """Send prompt to a player and wait for response."""
            try:
                await player.user.send(prompt)

                def check(msg: Message):
                    return msg.author == player.user and isinstance(msg.channel, discord.DMChannel)

                response = await client.wait_for("message", check=check, timeout=30)
                gameSession.responses[player] = response
            except asyncio.TimeoutError:
                gameSession.responses[player] = "No response (timed out)"

        for player in gameSession.players:
            tasks.append(ask_player(player))

        await asyncio.gather(*tasks)


        #shuffle response
        responses_list = list(gameSession.responses.items())  
        random.shuffle(responses_list)
        gameSession.responses = dict(responses_list)


        #map emojis to responses and sent voting message
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        response_summary = ""
        emoji_player_map = {}

        for index, player in enumerate(gameSession.responses.keys()):
            if gameSession.responses[player] == "No response (timed out)":
                response_summary += f"{emojis[index]}   : No response (timed out)\n"
            else:
                response_summary += f"{emojis[index]}   : {gameSession.responses[player].content}\n"
            emoji_player_map[emojis[index]] = player

        vote_message = await message.channel.send(f"{prompt}\n**Vote for the best response:**\n{response_summary}")

        for index, emoji in enumerate(emoji_player_map.keys()):
           await vote_message.add_reaction(emoji)

        await asyncio.sleep(40)

        
        #calculate points and display results
        vote_message = await message.channel.fetch_message(vote_message.id)

        vote_count = {}
        who_voted = ""

        for reaction in vote_message.reactions:
            if reaction.emoji in emoji_player_map.keys():
                vote_count[reaction.emoji] = reaction.count - 1
                who_voted += f"{emoji_player_map[reaction.emoji].user.display_name} :"

                async for reaction_user in reaction.users():
                    if emoji_player_map[reaction.emoji].user == reaction_user:
                        vote_count[reaction.emoji] -= 3

                    who_voted += f" {reaction_user.display_name}"
                who_voted += "\n"                    

        await message.channel.send(f"**Votes:**\n{who_voted}")

        round_results = ""

        for index, emoji in enumerate(emoji_player_map.keys()):
            player = emoji_player_map[emoji]
            player.add_points(vote_count[emoji])
            round_results += f"{player.user.display_name} : {player.points}\n"

        await message.channel.send(f"**Round results:**\n{round_results}")

        await vote_message.delete()

        gameSession.playing = False
        gameSession.responses = {}

    
    if user_message == "stop":
        for session in sessions:
            if session.channel == message.channel:
                sessions.remove(session)
                for player in session.players:
                    del player
                del session
                
                await message.channel.send("Game session ended")
                return
            
    if user_message.startswith("remove"):
        for session in sessions:
            if session.channel == message.channel:
                if session.host != message.author:
                    await message.channel.send("Only the host can remove players")
                    return

                user = message.mentions[0]
                session.remove_player(user)
                await message.channel.send(f"{user.display_name} removed from game")
                return
            
    if user_message == "players":
        for session in sessions:
            if session.channel == message.channel:
                players = ""
                for player in session.players:
                    players += f"{player.user.display_name}\n"
                await message.channel.send(f"**Players:**\n{players}")
                return