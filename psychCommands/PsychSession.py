import random

class PsychSession:
    def __init__(self, channel, host):
        self.channel = channel
        self.host = host
        self.players = []
        self.playing = False
        self.responses = {}
        
    def add_player(self, user):
        player = Player(user)
        self.players.append(player)


    def remove_player(self, user):
        for player in self.players:
            if player.user == user:
                self.players.remove(player)
                del player
                break

    def generate_prompt(self):
        try:
            with open("psychCommands\prompts.txt", "r", encoding="utf-8") as file:
                prompts = file.readlines()
                if not prompts:
                    return "No prompts available."

                prompt = random.choice(prompts).strip()

                while "<player>" in prompt and self.players:
                    prompt = prompt.replace("<player>", random.choice(self.players).user.display_name, 1)

                return prompt
        except FileNotFoundError:
            return "Error: prompts.txt not found."



class Player:
    def __init__(self, user):
        self.user = user
        self.points = 0

    def add_points(self, points):
        self.points += points