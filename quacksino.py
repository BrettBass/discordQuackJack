from redbot.core import commands, Config
import discord
import random
from typing import Optional
import asyncio
import time, datetime
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate
from .quackjack import *
from .quacklette import *

class quacksino(commands.Cog):
	__author__=["Wtfitsaduck"]
	__version__=["5.4.9"]

	def __init__(self, bot):
		self.bot = bot
		self.config = Config.get_conf(self, identifier=361823859125642)
		self.config.register_member(quacks = 10, interest_cooldown_target = 0, banned = False, force_registartion=True)
		self.config.register_guild(cooldown_target = 0, gambachannels=[], force_registration=True)
		self.loop = bot.loop
		self.game_session_active = {}

	@commands.group(aliases=["qs"])
	async def quacksino(self, ctx):
		pass
	
	@quacksino.command(usage="<User>", aliases=["ban"])
	async def blacklist(self, ctx, user:discord.Member):
		"""
		Blacklist a user from gambling
		"""
		await self.config.member(user).banned.set(True)
		await ctx.reply(f"Blacklisted {user.name}")

	@quacksino.command(usage="<User>")
	async def whitelist(self, ctx, user:discord.Member):
		"""
		Whitelist a user from gambling
		"""
		await self.config.member(user).banned.set(False)
		await ctx.reply(f"Whitelisted {user.name}")
	@quacksino.group()
	async def gambachannels(self, ctx):
		pass
		
	@gambachannels.command(usage="<text channels (space seperated)>")
	async def add(self, ctx, *channels: discord.TextChannel):
		"""
		Remove gamba channels
		"""
		gambachannels = await self.config.guild(ctx.guild).gambachannels()
		channels_added= ""
		for channel in channels:
			gambachannels.append(channel.name)
			channels_added += f" {channel.name}"
		await self.config.guild(ctx.guild).gambachannels.set(gambachannels)
		await ctx.reply(f"Added`{channels_added}` to gamba channel list")

	@gambachannels.command(usage="<text channels (space seperated)>")
	async def remove(self, ctx, *channels: discord.TextChannel):
		"""
		Remove gamba channels
		"""
		notfound_list = ""
		channels_removed = ""
		gambachannels = await self.config.guild(ctx.guild).gambachannels()
		for channel in channels:
			try:
				gambachannels.remove(channel.name)
				channels_removed += f" {channel.name}"
			except:
				notfound_list += f" {channel.name}"
		await self.config.guild(ctx.guild).gambachannels.set(gambachannels)
		await ctx.reply(f"Removed`{channels_removed}` from gamba channel list")
		if len(notfound_list) > 0:
			await ctx.send(f"channel{'s' if len(notfound_list) >1 else ''}`{notfound_list}` {'was' if len(notfound_list == 1) else 'were'} not in the whitelist.")
	@gambachannels.command()
	async def list(self, ctx):
		"""
		List current gamba channels
		"""
		gambachannels = await self.config.guild(ctx.guild).gambachannels()
		channel_list_string = ""
		for channel in gambachannels:
			channel_list_string += f"{channel} "
		await ctx.reply(f"Current gamba channel{'s are' if len(gambachannels) >1 else 'is'} `{channel_list_string}`")

	async def invalid_channel(self, ctx):
		if ctx.channel.name not in await self.config.guild(ctx.guild).gambachannels():
			await ctx.message.delete()
			await ctx.author.send("<:cuttingdownoneggplants:893273818364276736>")
			return True
		else:return False

	def reset_check(author):
		def innercheck(message):
			if message.author != author:return False
			if message.content.lower() == "confirm":return True
			if message.content.lower() == "cancel":return True
		return innercheck
	
	@quacksino.command()
	async def resetall(self, ctx):
		msg = await ctx.reply("Are you sure you want to reset ***__all__*** user quacks in this server? [Confirm/Cancel]")
		try:
			response = await self.bot.wait_for("message", check=quacksino.reset_check(ctx.author), timeout=60)
		except asyncio.TimeoutError:
			await msg.edit(content="Timed out.")

		if response.content.lower() == "confirm":
			await self.config.clear_all_members()
			await self.config.guild(ctx.guild).cooldown_target.set(0)
			await ctx.send("Reset all members to starting points.")
		elif response.content.lower() == "cancel":
			await msg.edit(content="Canceled.")
			return
	@quacksino.command()
	async def test(self, ctx):
		data = await self.config.all_members(ctx.guild)
		users_count = {}
		for key in data:
			user_id_list[key] = self.config.memeber(ctx.guild.get_member(key)).quacks()
		

		#data = data.items(0:1)

		await ctx.send(data)
	@quacksino.command()
	async def nextcard(self, ctx, player: Optional[discord.Member]):
		if player is None:
			player = ctx.author

		try:
			nextcard = deck[player.id][-1]
		except:
			await ctx.reply(f"{player.name} does not have a session active.")
			return
		await ctx.reply(nextcard)

	@commands.group(autohelp=False, invoke_without_command=True, aliases=["q"])
	async def quack(self, ctx):
		"Quack"
		if await self.loop.create_task(quacksino.invalid_channel(self,ctx)):return
		elif await self.config.member(ctx.author).banned():return
		cooldown_target = await self.config.guild(ctx.guild).cooldown_target()
		time_remaining = round(cooldown_target - time.time())

		if time_remaining > 0:
			await ctx.reply(f"Time remaining: {datetime.timedelta(seconds=time_remaining)}")
			return

		cooldown_target = (random.randint(1800, 3600) + time.time())
		time_remaining = round(cooldown_target - time.time())
		await self.config.guild(ctx.guild).cooldown_target.set(cooldown_target)

		await ctx.reply(file=discord.File("/home/redbot/.local/share/Red-DiscordBot/data/default/cogs/CogManager/cogs/quacksino/quack.gif"))
		user_quack_counter = await self.config.member(ctx.author).quacks()
		user_quack_counter += 5
		await self.config.member(ctx.author).quacks.set(user_quack_counter)
	
		self.loop.create_task(quacksino.quacks(self, ctx, ctx.author))

	async def paybot(self, ctx, amount: int):
		bot_member = ctx.guild.get_member(self.bot.user.id)
		bot_quacks = await self.config.member(bot_member).quacks()
		await self.config.member(bot_member).quacks.set(bot_quacks + amount)

	@commands.command("quacks", usage="<optional: quacker> <optional: server ID>")
	async def quacks(self, ctx, quacker: Optional[discord.Member]):
		"""
		Find out how many quacks you or
		your friends (or enemies) have
		"""
		if await self.config.member(ctx.author).banned():return
		elif await self.loop.create_task(quacksino.invalid_channel(self,ctx)):return

		if ctx.guild is None:
			await ctx.reply("Unavailable in DM's")
			return

		if quacker is None:quacker = ctx.author
		elif quacker is int:quacker = await self.bot.fetch_member(quacker)
			

		colors = [0xb00b69, 0xff0303, 0xffe70a, 0xc2ff0a, 0x0aff1f, 0x0affeb, 0x0a47ff, 0x7141b5, 0xff00f2]
		selected_color = random.choice(colors)
		embed = discord.Embed(description="Quacker Count:", colour=selected_color)

		user_quack_counter = await self.config.member(quacker).quacks()

		if user_quack_counter == 0:
			await ctx.reply(f"{quacker.name} has no quacks")
			return
		if user_quack_counter < 0:
			await ctx.reply("This motha fucka's in the negatives lol")
		embed.add_field(name=quacker.name, value=user_quack_counter)
		await ctx.reply(embed=embed)

	@quack.command(aliases=["lb"])
	async def leaderboards(self, ctx):
		pass

	@quack.command()
	async def bank(self, ctx):
		"""
		Get your daily interest by using QuackBank™
		"""
		if await self.config.member(ctx.author).banned():return
		elif await self.loop.create_task(quacksino.invalid_channel(self,ctx)):return
		interest_cooldown_target = await self.config.member(ctx.author).interest_cooldown_target()
		time_remaining = round(interest_cooldown_target - time.time())
		user_quacks = await self.config.member(ctx.author).quacks()

		if time_remaining > 0:
				await ctx.reply(f"Come back in {datetime.timedelta(seconds=time_remaining)} for your interest.")
				return

		interest_cooldown_target = (86400 + time.time())
		await self.config.member(ctx.author).interest_cooldown_target.set(interest_cooldown_target)

		rate = random.randint(5, 10)
		interest = int(user_quacks * (rate /100))
		if interest == 0:interest = 1

		user_quacks += interest
		await self.config.member(ctx.author).quacks.set(user_quacks)
		await ctx.reply(f"{interest} {'quack has' if interest == 1 else 'quacks have'} been added to your account. Today's interest was {rate}%. Thank you for trusting QuackBank™")

	@quacksino.command(usage="<User> <Quack count>")
	async def setquacks(self, ctx, quacker: discord.Member, quacks: int):
		if ctx.guild is None:
			await ctx.send("Unavailable in DM's")
			return
		await self.config.member(quacker).quacks.set(quacks)
		await ctx.reply("Done")

	@quacksino.command(aliases=["gq"])
	async def givequacks(self, ctx, quacker: discord.Member, quack_amount: int):
		await self.config.member(quacker).quacks.set(await self.config.member(quacker).quacks() + quack_amount)
		await ctx.reply(f"Gave {quack_amount} quack{'' if quack_amount ==1 else 's'} to {quacker.name}")

	@quack.command(usage="<User> <Amount>", aliases=["spreadit", "p"],autohelp=False)
	async def pay(self, ctx, recipient: discord.Member, amount: int):
		"""
		Pay a user some of your hard earned quacks
		"""
		try:
			if self.game_session_active[ctx.author.id]:
				await ctx.reply("Can't send quacks right now.")
				return
		except:
			pass
		try:
			if self.game_session_active[recipient.id]:
				await ctx.reply("Can't send quacks right now")
				return
		except:
			pass
		if await self.config.member(ctx.author).banned():return
		elif await self.loop.create_task(quacksino.invalid_channel(self, ctx)):return
		if recipient is int:
			recipient = await self.bot.fetch_member(recipient)

		user_quack_counter = await self.config.member(ctx.author).quacks()
		recipient_quack_counter = await self.config.member(recipient).quacks()

		if recipient.id == ctx.author.id:
			await ctx.reply("You can't pay yourself dingus.")
			return
		if amount <= 0:
			await ctx.reply("Amount must be more than 0")
			return
		if amount > user_quack_counter:
			await ctx.reply("You don't have that many quacks chief.")
			self.loop.create_task(quacksino.quacks(self, ctx, ctx.author))
			return

		self.game_session_active[ctx.author.id] = True

		warning_msg = await ctx.reply(f"Are you sure you want to send {amount} quack{'s' if amount > 1 else ''} to {recipient.name}? {'9% tax will be deducted for amounts 50 and over.' if amount >= 50 else ''}")
		pred = ReactionPredicate.yes_or_no(warning_msg, ctx.author)
		start_adding_reactions(warning_msg, ReactionPredicate.YES_OR_NO_EMOJIS)

		try:
			await self.bot.wait_for("reaction_add", check=pred, timeout=30)
		except asyncio.TimeoutError:
			await warning_msg.edit(content="Transaction timed out")
			await warning_msg.clear_reactions()
			self.game_session_active[ctx.author.id] = False
			return
		if not pred.result:
			await warning_msg.reply("Transaction cancelled.")
			self.game_session_active[ctx.author.id] = False
			return 
		tax = 0
		if amount >= 50:
			tax = int(amount * 0.09)
			amount -= tax
			await self.loop.create_task(quacksino.paybot(self, ctx, tax))

		recipient_quack_counter += amount
		user_quack_counter -= amount + tax
		await self.config.member(ctx.author).quacks.set(user_quack_counter)
		await self.config.member(recipient).quacks.set(recipient_quack_counter)
		await ctx.reply(f"paid {recipient.name} {amount} {'quack' if amount == 1 else 'quacks'}.")
		self.game_session_active[ctx.author.id] = False

	@quack.command(usage="<Heads/Tails> <amount>", aliases=["f"], autohelp=False)
	async def flip(self, ctx, choice: str, bet_amount: Optional[int]):
		"""
		Gamble your quacks with a coinflip.
		"""
		if await self.loop.create_task(quacksino.invalid_channel(self,ctx)):return
		elif await self.config.member(ctx.author).banned():return
		user_quacks = await self.config.member(ctx.author).quacks()
		
		if ctx.guild is None:
			await ctx.reply("Unavailable in dm's")
			return
		if bet_amount is None:
			if user_quacks <5:
				if user_quacks == 0:
					await ctx.reply("You have no quacks.")
					return
				else:					
					bet_amount = user_quacks
			else:
				bet_amount = 5
				
		if bet_amount > user_quacks:
			await ctx.reply("Not enough quacks!")
			return
		if bet_amount <= 0:
			await ctx.reply("Amount can't be 0 or less")
			return
		elif bet_amount > 150:
			await ctx.reply("150 quacks max bet")
			return
		
		shorthand_choice = choice[0].lower()
		if shorthand_choice != "h" and shorthand_choice != "t":
			await ctx.reply(f"[h]eads or [t]ails")
			return

		flip = random.choice(["heads","tails"])
		
		if shorthand_choice == flip[0]:
			user_quacks += bet_amount
			await self.loop.create_task(quacksino.paybot(self, ctx, 0-bet_amount))
		else:
			user_quacks -= bet_amount
			await self.loop.create_task(quacksino.paybot(self, ctx, bet_amount))
		
		await ctx.reply(f"It's {flip}!")
		await self.config.member(ctx.author).quacks.set(user_quacks)

	@quack.command(usage="<bet amount>", aliases=["j"], autohelp=False)
	async def jack(self, ctx, bet_amount: Optional[int]):
		"""
		Blackjack with quacks!
		"""
		if await self.loop.create_task(quacksino.invalid_channel(self,ctx)):return
		elif await self.config.member(ctx.author).banned():return
		try:
			if self.game_session_active[ctx.author.id]:
				await ctx.reply("You already have a game instance active!")
				return
		except KeyError:
			pass

		if ctx.guild is None:
			await ctx.reply("Unavailable in dm's")
			return

		user_quacks = await self.config.member(ctx.author).quacks()

		if bet_amount is None:
			if user_quacks <5:
				if user_quacks == 0:
					await ctx.reply("You have no quacks.")
					return
				else:					
					bet_amount = user_quacks
			else:
				bet_amount = 5

		if bet_amount > user_quacks:
			await ctx.reply("Not enough quacks!")
			return
		elif bet_amount <= 0:
			await ctx.reply("Amount can't be 0 or less")
			return
		elif bet_amount > 150:
			await ctx.reply("150 quacks max bet")
			return

		player = ctx.author.id
		player_hand[player] = []
		dealer_hand[player] = []
		player_bust[player] = False
		dealer_bust[player] = False
		player_blackjack[player] = False
		player_surrendered[player] = False
		player_doubled[player] = False
		hit_count[player] = 0

		self.game_session_active[player] = True
		deck[player] = list(range(2,15))*4
		random.shuffle(deck[player])
		
		player_hand_message[player] = await ctx.reply(f"Your hand: ")
		dealer_hand_message[player] = await ctx.reply(f"Dealer is showing: ")

		for i in range(2):
			await player_hand_message[player].edit(content=f"{player_hand_message[player].content}  {quackjack.hit(player_hand[player], deck[player])}")
			await asyncio.sleep(0.4)
		await asyncio.sleep(0.4)
		await player_hand_message[player].edit(content=f"{player_hand_message[player].content}, total: {quackjack.total(player_hand[player])}")
		await asyncio.sleep(0.4)

		if quackjack.total(player_hand[player]) == 21:
			await ctx.send(f"Blackjack! You win {bet_amount * 2} quacks.")
			player_blackjack[player] = True
			await self.config.member(ctx.author).quacks.set(user_quacks + (bet_amount * 2))
			await self.loop.create_task(quacksino.paybot(self, ctx, 2*(0-bet_amount)))
			self.game_session_active[ctx.author.id] = False
			return
		await dealer_hand_message[player].edit(content=f"{dealer_hand_message[player].content}  {quackjack.hit(dealer_hand[player], deck[player])}")
		await asyncio.sleep(0.4)
		
		await dealer_hand_message[player].edit(content=f"{dealer_hand_message[player].content}, total: {quackjack.total(dealer_hand[player])}")
		
		
		while not player_blackjack[player]:
			if hit_count[player] == 0:await player_hand_message[player].reply("Hit, stand, surrender, or double?")
			elif hit_count[player] == 1:await player_hand_message[player].reply("Hit or stand?")
			try:
				msg = await self.bot.wait_for("message", check=quackjack.check(ctx.author), timeout=15)
			except asyncio.TimeoutError:
				await ctx.send("Standing. . .")
				break
			if msg.content.lower() == "hit":
				await player_hand_message[player].edit(content=(f"{player_hand_message[player].content.split(', ')[0]}  {quackjack.hit(player_hand[player], deck[player])}, total: {quackjack.total(player_hand[player])}"))
				hit_count[player] += 1

			elif msg.content.lower() == "double":
				if user_quacks >= (bet_amount*2):
					await player_hand_message[player].reply("Doubled down.")
					await player_hand_message[player].edit(content=(f"{player_hand_message[player].content.split(', ')[0]}  {quackjack.hit(player_hand[player], deck[player])}, total: {quackjack.total(player_hand[player])}"))
					bet_amount = bet_amount * 2
					player_doubled[player] = True
				else:
					await ctx.send("You do not have enough quacks to double down.")
					hit_count[player] += 1
			elif msg.content.lower() == "surrender":
				if bet_amount == 1:
					await ctx.send("Can't surrender on 1 quack")
					hit_count[player] += 1
				else:
					bet_amount = int(bet_amount/2)
					player_surrendered[player] = True
					break
			else:break

			if quackjack.total(player_hand[player]) == 21:
				break
			elif quackjack.total(player_hand[player]) >21:
				player_bust[player] = True
				break
			if player_doubled[player]:
				break

		if player_bust[player]:
			await ctx.send(f"You're bust!, you lose {bet_amount} {'quack' if bet_amount ==1 else 'quacks'}")
			await self.config.member(ctx.author).quacks.set(user_quacks - bet_amount)
			await self.loop.create_task(quacksino.paybot(self, ctx, bet_amount))
			self.game_session_active[player] = False
			return
		elif player_surrendered[player]:
			await ctx.send(f"You surrendered, you lose {bet_amount} {'quack' if bet_amount == 1 else 'quacks'}")
			await self.config.member(ctx.author).quacks.set(user_quacks - bet_amount)
			self.game_session_active[player] = False
			return

		if not player_bust[player] and not player_blackjack[player]:
			await dealer_hand_message[player].reply("Dealer is playing. . .")

			while quackjack.total(dealer_hand[player]) < 17:
				await asyncio.sleep(1)
				await dealer_hand_message[player].edit(content=(f"{dealer_hand_message[player].content.split(', ')[0]}  {quackjack.hit(dealer_hand[player], deck[player])}, total: {quackjack.total(dealer_hand[player])}"))
				if quackjack.total(dealer_hand[player]) > 21:
					dealer_bust[player] = True
					break

		if dealer_bust[player]:
			await ctx.send(f"House is bust, you win {bet_amount} {'quack' if bet_amount ==1 else 'quacks'}.")
			await self.config.member(ctx.author).quacks.set(user_quacks + bet_amount)
			await self.loop.create_task(quacksino.paybot(self, ctx, 0-bet_amount))
			self.game_session_active[player] = False
			return
		if quackjack.total(dealer_hand[player]) == quackjack.total(player_hand[player]):
			await ctx.send("Pushed, points unchanged.")
		elif quackjack.total(player_hand[player]) > quackjack.total(dealer_hand[player]):
			await ctx.send(f"You win {bet_amount} {'quack' if bet_amount ==1 else 'quacks'}.")
			await self.config.member(ctx.author).quacks.set(user_quacks + bet_amount)
			await self.loop.create_task(quacksino.paybot(self, ctx, 0-bet_amount))

		elif quackjack.total(player_hand[player]) < quackjack.total(dealer_hand[player]):
			await ctx.send(f"House wins, you lose {bet_amount} {'quack' if bet_amount ==1 else 'quacks'}.")
			await self.config.member(ctx.author).quacks.set(user_quacks - bet_amount)
			await self.loop.create_task(quacksino.paybot(self, ctx, bet_amount))
		else:
			await ctx.send("something weird happened. Points unchanged.")
		self.game_session_active[player] = False

	@quack.command(usage="<Opponent> <Bet Amount>", aliases=["jduel", "jd"], autohelp=False)
	async def jackduel(self, ctx, opponent: discord.Member, bet_amount: int):
		"""
		Challenge someone to a game of quackjack
		"""
		# CHECKS
		if await self.loop.create_task(quacksino.invalid_channel(self,ctx)):return
		elif await self.config.member(ctx.author).banned():return
		challenger = ctx.author
		
		try:
			if self.game_session_active[challenger.id]:
				await ctx.reply("You already have a game instance active!")
				return
		except KeyError:
			pass

		challenger_quacks = await self.config.member(challenger).quacks()
		opponent_quacks = await self.config.member(opponent).quacks()

		if bet_amount > challenger_quacks:
			await ctx.reply("You do not have that many quacks!")
			return
		elif bet_amount <= 0:
			await ctx.reply("Amount can't be 0 or less")
			return
		if opponent.id == self.bot.user.id:
			await self.loop.create_task(quacksino.jack(self, ctx, bet_amount))
			return
		try:
			if self.game_session_active[opponent.id]:
				await ctx.reply(f"{opponent.name} already has a quackjack instance active!")
				return
		except KeyError:
			pass
		
		if bet_amount > opponent_quacks:
			await ctx.reply(f"{opponent.name} does not have that many quacks")
			return
		#END CHECKS
		self.game_session_active[challenger.id] = True
		self.game_session_active[opponent.id] = True
		challenge_message = await ctx.send(f"{opponent.mention}! You have been challenged to a 1 v 1 against {challenger.mention} for {bet_amount} {'quack' if bet_amount ==1 else 'quacks'}. Do you accept or deny?")
		try:
			response = await self.bot.wait_for("message", check=quackjack.duelcheck(opponent), timeout=30)
		except asyncio.TimeoutError:
			await challenge_message.edit(content=f"{opponent.name} did not respond.")
			self.game_session_active[challenger.id] = False
			self.game_session_active[opponent.id] = False
			return
		if response.content.lower() == "deny":
			await challenge_message.edit(content=f"{opponent.name} denied the challege cuz they're a pussy.")
			self.game_session_active[challenger.id] = False
			self.game_session_active[opponent.id] = False
			return
		
		# VAR INIT
		deck[challenger.id] = list(range(2,15))*4
		random.shuffle(deck[challenger.id])
		player_hand[challenger.id] = []
		player_hand[opponent.id] = []
		hit_count[challenger.id] = 1
		hit_count[opponent.id] = 1
		player_bust[challenger.id] = False
		player_bust[opponent.id] = False
		player_blackjack[challenger.id] = False
		player_blackjack[opponent.id] = False
		# END VAR INIT

		challenger_hand_message = await ctx.send(f"{challenger.name}'s hand: ")
		opponent_hand_message = await ctx.send(f"{opponent.name}'s hand: ")

		for i in range(2):
			await asyncio.sleep(0.4)
			await challenger_hand_message.edit(content=f"{challenger_hand_message.content}  {quackjack.hit(player_hand[challenger.id], deck[challenger.id])}")
			await asyncio.sleep(0.4)
			await opponent_hand_message.edit(content=f"{opponent_hand_message.content}  {quackjack.hit(player_hand[opponent.id], deck[challenger.id])}")

		await challenger_hand_message.edit(content=f"{challenger_hand_message.content}, total: {quackjack.total(player_hand[challenger.id])}")
		await opponent_hand_message.edit(content=f"{opponent_hand_message.content}, total: {quackjack.total(player_hand[opponent.id])}")

		if quackjack.total(player_hand[challenger.id]) == 21 and quackjack.total(player_hand[opponent.id]) == 21:
			await ctx.send(f"Both players hit a blackjack! awarding both players {bet_amount} quack{'' if bet_amount == 1 else 's'}.")
			await self.config.member(challenger).quacks.set(challenger_quacks + bet_amount)
			await self.config.member(opponent).quacks.set(opponent_quacks + bet_amount)
			self.game_session_active[challenger.id] = False
			self.game_session_active[opponent.id] = False
			return
		elif quackjack.total(player_hand[challenger.id]) == 21:
			await ctx.send(f"{challenger.name} hit a blackjack!")
			player_blackjack[challenger.id] = True
		elif quackjack.total(player_hand[opponent.id]) == 21:
			await ctx.send(f"{opponent.name} hit a blackjack!")
			player_blackjack[opponent.id] = True

		await challenger_hand_message.reply(f"{challenger.name} is playing. Hit or stand?")

		await self.loop.create_task(quackjack.against_player(self, ctx, challenger, challenger_hand_message, challenger.id))

		if player_bust[challenger.id]:
			await ctx.send(f"{challenger.name} is bust! {opponent.name} wins the {bet_amount} {'quack' if bet_amount ==1 else 'quacks'}")
			await self.config.member(challenger).quacks.set(challenger_quacks - bet_amount)
			await self.config.member(opponent).quacks.set(opponent_quacks + bet_amount)
			self.game_session_active[challenger.id] = False
			self.game_session_active[opponent.id] = False
			return

		await opponent_hand_message.reply(f"{opponent.name} is playing. Hit or stand?")

		await self.loop.create_task(quackjack.against_player(self, ctx, opponent, opponent_hand_message, challenger.id))

		if player_bust[opponent.id]:
			await ctx.send(f"{opponent.name} is bust! {challenger.name} wins the {bet_amount} {'quack' if bet_amount ==1 else 'quacks'}")
			await self.config.member(challenger).quacks.set(challenger_quacks + bet_amount)
			await self.config.member(opponent).quacks.set(opponent_quacks - bet_amount)
			self.game_session_active[challenger.id] = False
			self.game_session_active[opponent.id] = False
			return
		
		if quackjack.total(player_hand[challenger.id]) == quackjack.total(player_hand[opponent.id]):
			await ctx.send("Pushed; points unchanged.")
		elif quackjack.total(player_hand[challenger.id]) > quackjack.total(player_hand[opponent.id]):
			await ctx.send(f"{challenger.name} wins the {bet_amount} {'quack' if bet_amount ==1 else 'quacks'}.")
			await self.config.member(challenger).quacks.set(challenger_quacks + bet_amount)
			await self.config.member(opponent).quacks.set(opponent_quacks - bet_amount)
		elif quackjack.total(player_hand[opponent.id]) > quackjack.total(player_hand[challenger.id]):
			await ctx.send(f"{opponent.name} wins the {bet_amount} {'quack' if bet_amount ==1 else 'quacks'}.")
			await self.config.member(challenger).quacks.set(challenger_quacks - bet_amount)
			await self.config.member(opponent).quacks.set(opponent_quacks + bet_amount)
		else:
			await ctx.send("something weird happened. Points unchanged.")

		self.game_session_active[challenger.id] = False
		self.game_session_active[opponent.id] = False