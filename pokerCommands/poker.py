import discord
from discord import Message
import asyncio
import random
from collections import Counter
from itertools import combinations

CARD_SUITS = ["♠", "♥", "♦", "♣"]
CARD_VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

class PokerGame:
    def __init__(self, channel, host):
        self.channel = channel
        self.host = host
        self.players = []
        self.deck = self.create_deck()
        self.pot = 0
        self.playing = False
        self.hands = {}
        self.max_bet = 0
        self.table = []
        self.table_turn = 0
    
    def create_deck(self):
        return [f"{value}{suit}" for value in CARD_VALUES for suit in CARD_SUITS]
    
    def shuffle_deck(self):
        random.shuffle(self.deck)
    
    def add_player(self, user):
        if user not in [player.user for player in self.players]:
            self.players.append(Player(user))
    
    def deal_cards(self):
        self.shuffle_deck()
        self.hands = {player: [self.deck.pop(), self.deck.pop()] for player in self.players}
    
    def remove_player(self, user):
        self.players = [player for player in self.players if player.user != user]
    
    def reset_game(self):
        self.deck = self.create_deck()
        self.pot = 0
        self.playing = False
        self.hands = {}

    def best_hand(self, player_hand):
        """Evaluates the best 5-card hand from player's two hole cards and 5 community cards."""
        all_cards = player_hand + self.table
        best_rank = (0, [])  # (hand ranking score, best hand combination)
        
        for combo in combinations(all_cards, 5):
            rank = self.evaluate_hand(combo)
            if rank[0] > best_rank[0]:
                best_rank = rank
        
        return best_rank
    
    def evaluate_hand(self, hand):
        """Returns a tuple (rank, sorted_hand) where rank is an integer representing the hand's strength."""
        
        rank_values = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
            "J": 11, "Q": 12, "K": 13, "A": 14  # Ace is high by default
        }

        values = sorted([rank_values[card[:-1]] for card in hand], reverse=True)
        suits = [card[1] for card in hand]
        value_counts = Counter(values)
        
        # Sorting by frequency first, then by card rank (descending)
        sorted_counts = sorted(value_counts.items(), key=lambda x: (-x[1], -x[0]))

        is_flush = len(set(suits)) == 1
        is_straight = len(value_counts) == 5 and max(values) - min(values) == 4
        
        # Check for A-2-3-4-5 straight
        if set(values) == {14, 2, 3, 4, 5}:  
            is_straight = True  
            values = [5, 4, 3, 2, 1]  # Adjust values for proper ranking

        if is_straight and is_flush:
            return (9, values)  # Straight flush
        elif sorted_counts[0][1] == 4:
            return (8, [sorted_counts[0][0]] * 4 + [sorted_counts[1][0]])  # Four of a kind
        elif sorted_counts[0][1] == 3 and sorted_counts[1][1] == 2:
            return (7, [sorted_counts[0][0]] * 3 + [sorted_counts[1][0]] * 2)  # Full house
        elif is_flush:
            return (6, values)  # Flush
        elif is_straight:
            return (5, values)  # Straight
        elif sorted_counts[0][1] == 3:
            return (4, [sorted_counts[0][0]] * 3 + list(sorted_counts[1][0:2]))  # Three of a kind
        elif sorted_counts[0][1] == 2 and sorted_counts[1][1] == 2:
            return (3, [sorted_counts[0][0]] * 2 + [sorted_counts[1][0]] * 2 + list([sorted_counts[2][0]]))  # Two pair
        elif sorted_counts[0][1] == 2:
            return (2, [sorted_counts[0][0]] * 2 + list(sorted_counts[1][0:3]))  # One pair
        else:
            return (1, values)  # High card
        
    def hand_rank_name(self, rank):
        """Returns the name of a hand rank."""
        rank_names = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"]
        return rank_names[rank-1]
    






class Player:
    def __init__(self, user):
        self.user = user
        self.chips = 10000
        self.bet = 0
        self.all_in = False
        self.fold = False
    
    def place_bet(self, amount):
        self.chips -= amount
        self.bet += amount






async def pokerCommand(message: Message, user_message: str, sessions, client) -> None:
    
    if user_message == "new":
        if any(session.channel == message.channel for session in sessions):
            await message.channel.send("A poker game is already running in this channel.")
            return
        
        poker_game = PokerGame(message.channel, message.author)
        sessions.append(poker_game)
        
        
        sent_message = await message.channel.send("React 👍 to join game")  
        await sent_message.add_reaction("👍")

    elif user_message == "players":
        for session in sessions:
            if session.channel == message.channel:
                await message.channel.send(f"Players: {', '.join([player.user.name for player in session.players])}")
                return
        await message.channel.send("No poker game running in this channel.")

    if user_message == "start":
        
        pokerGame = None
        for session in sessions:
            if session.channel == message.channel:
                if session.host != message.author:
                    await message.channel.send("Only the host can start the game.")
                    return
                
                    # if len(session.players) < 2:
                    #     await message.channel.send("At least two players are needed to start.")
                    #     return

                
                pokerGame = session

                if pokerGame.playing:
                    await message.channel.send("Round already started")
                    return
                
                break
                
        pokerGame.playing = True
        pokerGame.deal_cards()
        for player in pokerGame.players:
            await player.user.send(f"Your hand: {', '.join(pokerGame.hands[player])}\nAmount left: {player.chips}")
        await message.channel.send("Cards dealt! Players, check your DMs.\nReply with '#bet <amount>' to place a bet.\nReply with '#fold' to fold.\n Reply with #match to match current bet")
        return
    
    if user_message.startswith("bet "):
        pokerGame = next((session for session in sessions if session.channel == message.channel), None)
        if pokerGame is None:
            await message.channel.send("No poker game running in this channel.")
            return
        

        
        try: 
            amount = int(user_message.split()[1])
            
            player = next((player for player in pokerGame.players if player.user.name == message.author.name), None)

            if player is None:
                await message.channel.send("You are not in the game.")
                return
            
            if player not in pokerGame.hands:
                await message.channel.send("You have not been dealt cards this sequence.")
                return
            
            elif player.fold:
                await message.channel.send("You have folded.")
                return
            
            elif player.all_in:
                await message.channel.send("You are all in.")
                return
            
            elif amount + player.bet > player.chips:
                await message.channel.send(f"{message.author.mention} Insufficient chips. You can do #bet-all or #bet <amount> again\nCurrent bet is: " + str(player.bet) + "\nCurrent chips: " + str(player.chips))
                return
            
            elif amount + player.bet < pokerGame.max_bet:
                await message.channel.send(f"{message.author.mention} Bet must be at least {pokerGame.max_bet - player.bet}.\n You can #match or #bet-all")
                return
            
            player.bet += amount
            pokerGame.max_bet = player.bet

            await message.channel.send(f"{message.author.mention} has placed a total bet of {player.bet}.")
            return
        
        except ValueError:
            await message.channel.send("Invalid bet amount.")
            return
        
    if user_message == "fold":

        pokerGame = next((session for session in sessions if session.channel == message.channel), None)
        if pokerGame is None:
            await message.channel.send("No poker game running in this channel.")
            return
        
        player = next((player for player in pokerGame.players if player.user.name == message.author.name), None)
        if player is None:
            await message.channel.send("You are not in the game.")
            return
        
        if player not in pokerGame.hands:
            await message.channel.send("You have not been dealt cards this sequence.")
            return
        
        player.fold = True
        await message.channel.send(f"{message.author.mention} has folded.")
        return
    
    if user_message == "match":
        pokerGame = next((session for session in sessions if session.channel == message.channel), None)
        if pokerGame is None:
            await message.channel.send("No poker game running in this channel.")
            return
        
        player = next((player for player in pokerGame.players if player.user.name == message.author.name), None)
        if player is None:
            await message.channel.send("You are not in the game.")
            return
        
        if player not in pokerGame.hands:
            await message.channel.send("You have not been dealt cards this sequence.")
            return
        
        if player.fold:
            await message.channel.send("You have folded.")
            return
        
        if player.bet == pokerGame.max_bet:
            await message.channel.send("You have already matched the bet.")
            return
        
        if player.bet + player.chips < pokerGame.max_bet:
            player.all_in = True
            await message.channel.send(f"{message.author.mention} is all in.")
            return
        
        player.bet = pokerGame.max_bet
        await message.channel.send(f"{message.author.mention} has matched the bet.")
        return
    
    if user_message == "bet-all":
        pokerGame = next((session for session in sessions if session.channel == message.channel), None)
        if pokerGame is None:
            await message.channel.send("No poker game running in this channel.")
            return
        
        player = next((player for player in pokerGame.players if player.user.name == message.author.name), None)
        if player is None:
            await message.channel.send("You are not in the game.")
            return
        
        if player not in pokerGame.hands:
            await message.channel.send("You have not been dealt cards this sequence.")
            return
        
        if player.fold:
            await message.channel.send("You have folded.")
            return
        
        if player.chips > pokerGame.max_bet:
            pokerGame.max_bet = player.chips

        player.all_in = True
        await message.channel.send(f"{message.author.mention} is all in.\nCurrent bet is: " + pokerGame.max_bet)
        return


    if user_message == "next":
        pokerGame = next((session for session in sessions if session.channel == message.channel), None)
        if pokerGame is None:
            await message.channel.send("No poker game running in this channel.")
            return
        
        if not pokerGame.playing:
            await message.channel.send("No game in progress.")
            return
        
        if message.author != pokerGame.host:
            await message.channel.send("Only the host can start the next round.")
            return
        
        all_players_ready = True   
        not_ready_message = ""

        for player in pokerGame.players:
            if not player.fold and not player.all_in and player.bet < pokerGame.max_bet:
                not_ready_message += f"{player.user.mention} needs to match the bet or fold.\n"
                all_players_ready = False

        if not all_players_ready:
            await message.channel.send(not_ready_message)
            return
        
        if pokerGame.table_turn == 0:
            pokerGame.table = [pokerGame.deck.pop() for _ in range(3)]
            await message.channel.send(f"**Table cards:** {', '.join(pokerGame.table)}")
            pokerGame.table_turn += 1
            return
        
        elif pokerGame.table_turn == 1:
            pokerGame.table.append(pokerGame.deck.pop())
            await message.channel.send(f"**Table cards:** {', '.join(pokerGame.table)}")
            pokerGame.table_turn += 1
            return
        
        elif pokerGame.table_turn == 2:
            pokerGame.table.append(pokerGame.deck.pop())
            await message.channel.send(f"**Table cards:** {', '.join(pokerGame.table)}")
            pokerGame.table_turn += 1
            return
        
        else:
            await message.channel.send("All table cards have been dealt. Use #showdown")
        
    if user_message == "showdown":
        pokerGame = next((session for session in sessions if session.channel == message.channel), None)
        if pokerGame is None:
            await message.channel.send("No poker game running in this channel.")
            return
        
        if not pokerGame.playing:
            await message.channel.send("No game in progress.")
            return
        
        if message.author != pokerGame.host:
            await message.channel.send("Only the host can start the showdown.")
            return
        
        if pokerGame.table_turn < 2:
            await message.channel.send("At least 3 table cards are needed for a showdown.")
            return
        
        all_players_ready = True
        not_ready_message = ""    
        
        for player in pokerGame.players:
            if not player.fold and not player.all_in and player.bet < pokerGame.max_bet:
                not_ready_message += f"{player.user.mention} needs to match the bet or fold.\n"
                all_players_ready = False

        if not all_players_ready:
            await message.channel.send(not_ready_message)
            return
        
        hand_ranks = {}

        for player in pokerGame.players:
            if player not in pokerGame.hands:
                player.bet = 0
                player.all_in = False
                player.fold = False
                continue
            
            player.chips -= player.bet
            pokerGame.pot += player.bet
            
            if not player.fold:
                hand_ranks[player] = pokerGame.best_hand(pokerGame.hands[player] + pokerGame.table)

            player.bet = 0
            player.all_in = False
            player.fold = False

        best_rank = max(hand_ranks.values(), key=lambda x: x[0])
        winners = [player for player, rank in hand_ranks.items() if rank == best_rank]

        if len(winners) == 1:
            winner = winners[0]
            winner.chips += pokerGame.pot
            await message.channel.send(f"{winner.user.mention} wins the pot of {pokerGame.pot} with a {pokerGame.hand_rank_name(best_rank[0])}!")

        else:
            for winner in winners:
                winner.chips += pokerGame.pot // len(winners)
            
            await message.channel.send(f"Split pot! Winners: {', '.join([winner.user.mention for winner in winners])}")

        pokerGame.reset_game()

        status = ""

        for player in pokerGame.players:
            status = status + f"\n{player.user.display_name} Amount left: {player.chips}"

        await message.channel.send(f"**Player status:**{status}")

        return
    
    if user_message == "end":
        pokerGame = next((session for session in sessions if session.channel == message.channel), None)
        if pokerGame is None:
            await message.channel.send("No poker game running in this channel.")
            return
        
        if message.author != pokerGame.host:
            await message.channel.send("Only the host can end the game.")
            return
        
        for player in pokerGame.players:
            del player
        
        sessions.remove(pokerGame)
        await message.channel.send("Game session ended.")
        return