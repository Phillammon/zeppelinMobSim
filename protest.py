import random
import math
import statistics

# ASSUMPTIONS
# Players will banish non-Oyster-cultists
# Players will use guaranteed-but-random NCs over clover (or semirare) forced NCs
# Players will choose the NC that removes the most remaining protesters
# If available, cigarette lighters will always be used in combat
# Banishes are also free runs
# Macrometeorite isn't a real thing that exists
# The Nuge is not a real thing that exists
# Meteor lore doesn't give item drop ever
# Players won't skip undesirable NCs, they'll take them but grumble about RNG on /hardcore
# Players don't lose fights
# Clovering for an NC adds it to the noncombat adventure queue

# Lynyrd Strats are hard to code, will give it a shot later

def randomRound(number):
	rounding, integer = math.modf(number)
	output = int(integer if random.random() > rounding else integer + 1)
	return output

class protestSim():
	def __init__(self, itemdrop = 100, clovers = 3, noncom = 10, sleaze = 69, olfaction = True, 
	banishes = 2, nonolfactcopies = 2, whatshisnames = 1, lynyrdness = 3):
		self.itemdrop = itemdrop
		self.clovers = clovers
		self.noncom = noncom
		self.sleaze = sleaze
		self.olfaction = olfaction
		self.nonolfactcopies = nonolfactcopies
		self.banishes = banishes
		self.whatshisnames = whatshisnames
		self.lynyrdness = lynyrdness
	
	def prepareRun(self):
		self.comQueue = []
		self.ncomQueue = []
		self.zoneMonsters = ["Cultist", "Eagle", "Woodsman", "Pilot", "Skinner"]
		self.zoneNCs = ["benchWarrant", "amBush", "fireAbove"]
		self.protesters = 80
		self.turnsspent = 0
		self.remainingBanishes = self.banishes
		self.olfactionUsed = False
		self.remainingClovers = self.clovers
		self.remainingBanishes = self.remainingBanishes
		self.remainingCocktails = self.whatshisnames
		self.lighter = False
		random.seed()
	
	def rollNC(self):
		return (random.randint(1, 100) > (90 - self.noncom))
	
	def runAdv(self):
		if logging:
			print("> Starting turn " + str(self.turnsspent + 1) + " with " + str(self.protesters) + " protesters left")
	#returns true if adventure spent
		if (self.turnsspent % 7 == 0):
			if logging:
				print("> > Mercy noncombat")
			return self.runNCAdv()
		elif (self.remainingClovers > 0):
			if logging:
				print("> > Clover used. " + str(self.remainingClovers - 1) + " clovers remaining.")
			return self.runCloverNC()
		elif (self.rollNC()):
			if logging:
				print("> > Rolled Noncombat")
			return self.runNCAdv()
		else:
			if logging:
				print("> > Rolled Combat")
			return self.runCombatAdv()
			
	def fightNotCultist(self, notcultist):
		if self.remainingBanishes > 0:
			self.remainingBanishes -= 1
			self.zoneMonsters.remove(notcultist)
			if logging:
				print("> > > > Banished " + notcultist + ", " + str(self.remainingBanishes) + " banishes left")
			return False
		elif self.lighter:
			self.lighter = False
			litUp = random.randint(6, 8)
			if logging:
				print("> > > > Set " + str(litUp) + " protesters on fire with lighter")
			self.protesters -= litUp
			return True
		else:
			self.protesters -= 1
			if logging:
				print("> > > > Beat up " + notcultist)
			return True
			
	def fightCultist(self):
		if not self.olfactionUsed:
			self.olfactionUsed = True
			for i in range((2 if self.olfaction else 0) + self.nonolfactcopies):
				self.zoneMonsters.append("Cultist")
			if logging:
				print("> > > > Used all available olfacts on Cultist")
		if self.lighter:
			self.lighter = False
			litUp = random.randint(6, 8)
			if logging:
				print("> > > > Set " + str(litUp) + " protesters (including cultist) on fire with lighter")
			self.protesters -= litUp
			return True
		else:
			self.protesters -= 1
			if logging:
				print("> > > > Beat up a cultist")
		if 15 * (100 + self.itemdrop) > random.randint(1, 10000):
			self.lighter = True
			if logging:
				print("> > > > > Found a lighter!")
			
		return True
			
			
	def runCombatAdv(self):
		reroll = True
		adv = ""
		while reroll:
			reroll = False
			adv = random.choice(self.zoneMonsters)
			if logging:
				print("> > > Rolled " + adv + " as monster")
			if (adv in self.comQueue) and (random.randint(1, 4) > 1) and not (self.olfactionUsed and self.olfaction and adv == "Cultist"):
				reroll = True
				if logging:
					print("> > > > Rejected, rerolling!")
		self.comQueue.append(adv)
		self.comQueue = self.comQueue[-5:]
		if logging:
			print("> > > Locked in. Combat queue is now " + str(self.comQueue))
		if adv == "Cultist":
			return self.fightCultist()
		else:
			return self.fightNotCultist(adv)
	
	def runNCAdv(self):
		reroll = True
		adv = ""
		while reroll:
			reroll = False
			adv = random.choice(self.zoneNCs)
			if logging:
				print("> > > Rolled " + adv + " as NC")
			if (adv in self.ncomQueue) and (random.randint(1, 4) > 1):
				reroll = True
				if logging:
					print("> > > > Rejected, rerolling!")
		self.ncomQueue.append(adv)
		self.ncomQueue = self.ncomQueue[-5:]
		if logging:
			print("> > > Locked in. Noncombat queue is now " + str(self.ncomQueue))
		if adv == "benchWarrant":
			return self.runBenchWarrant()
		if adv == "amBush":
			return self.runAmBush()
		if adv == "fireAbove":
			return self.runFireAbove()
		return False #something has gone very wrong
		
	
	def runBenchWarrant(self):
		rolled = self.benchWarrantProtesters()
		if logging:
			print("> > > > Used " + str(self.sleaze) + " sleaze to creep out " + str(rolled) + " protesters")
		self.protesters -= rolled
		return True
	
	def runAmBush(self):
		if logging:
			print("> > > > Scared off " + str(self.amBushProtesters()) + " protesters")
		self.protesters -= self.amBushProtesters()
		return True
	
	def runFireAbove(self):
		self.protesters -= self.fireAboveProtesters()
		self.remainingCocktails -= 1
		if logging:
			if self.remainingCocktails >= 0:
				print("> > > > Used a Flamin' Whasthisname to light up 10 protesters. " + str(self.remainingCocktails) + " Whatshisnames remaining.")
			else:
				print("> > > > Lit up 3 protesters. ")
		return True
		
	def runCloverNC(self):
		self.remainingClovers -= 1
		if logging:
			print("> > > Choosing clover noncombat")
			print("> > > > Bench Warrant will creep out minimum of " + str(self.pessimisticBenchWarrantProtesters()))
			print("> > > > AmBush will scare " + str(self.amBushProtesters()))
			print("> > > > Fire Above will burn " + str(self.fireAboveProtesters()))
		if self.amBushProtesters() > self.pessimisticBenchWarrantProtesters():
			if self.amBushProtesters() > self.fireAboveProtesters():
				if logging:
					print("> > > Choosing Bush")
				return self.runAmBush()
			else:
				if logging:
					print("> > > Choosing Fire")
				return self.runFireAbove()
		else: 
			if self.pessimisticBenchWarrantProtesters() >= self.fireAboveProtesters():
				if logging:
					print("> > > Choosing Bench")
				return self.runBenchWarrant()
			else:
				if logging:
					print("> > > Choosing Fire")
				return self.runFireAbove()
	
	def benchWarrantProtesters(self):
		return max(3, randomRound(math.sqrt(self.sleaze)))
	
	def pessimisticBenchWarrantProtesters(self):
		return max(3, math.floor(math.sqrt(self.sleaze)))
		
	def amBushProtesters(self):
		return 3 + self.lynyrdness
		
	def fireAboveProtesters(self):
		return 10 if self.remainingCocktails > 0 else 3
	
	def runZeppelinMob(self):
		self.prepareRun()
		if logging:
			print("> Starting turn 1 with 80 protesters left")
			print("> > Forced Noncombat adventure: Too Much Humanity")
		while self.protesters > 0:
			if self.runAdv():
				self.turnsspent += 1
		if logging:
			print("> Starting turn " + str(self.turnsspent) + " with no protesters left")
			print("> > Forced Noncombat adventure: Not So Much With The Humanity")
			print("> Zeppelin Mob Cleared in " + str(self.turnsspent) + " turns")
		return self.turnsspent
	
	def runSimulations(self, runcount = 20000):
		runs = []
		for i in range(runcount):
			if logging:
				print("-----------------------------------")
				print("Simulating run " + str(i))
			runs.append(self.runZeppelinMob())
		return [statistics.mean(runs), statistics.harmonic_mean(runs), statistics.median(runs), statistics.pstdev(runs)]
		


logging = False

print(
	protestSim(
		itemdrop = 100, 	# Your + Item Drop percent, expressed as an integer (+100% = 100, etc)
		clovers = 3, 		# The number of clovers (and semirares, if available) you are devoting to the mob
		noncom = 10, 		# Your +NC%, expressed as an integer. If you have +Combat, set this negative
		sleaze = 69, 		# Your combined sleaze damage plus sleaze spell damage
		olfaction = True, 	# True if transcendent olfaction is available (2 copies and no queue rejection)
		banishes = 2, 		# Number of available banishes (assumed to be free runaways lasting for the whole zone)	
		nonolfactcopies = 2,# Number of non-Transcendent Olfaction copies of a monster you can add to the zone (Gallapagosian Call, Offer Latte, etc)
		whatshisnames = 1,  # Number of available flaming whatshisnames
		lynyrdness = 3		# 3 for lynyrd musk, +5 for each distinct lynyrdskin gear worn
	).runSimulations())
