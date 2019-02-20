import random
import math
import statistics

logging = False

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
	output = integer if random.random() > rounding else integer + 1
	if logging: 
		print("Rounded " + str(number) + " randomly to " + str(output))
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
		self.turnsspent = 1 #Too Much Humanity
		self.remainingBanishes = self.banishes
		self.olfactionUsed = False
		self.remainingClovers = self.clovers
		self.remainingCocktails = self.whatshisnames
		self.lighters = 0
		random.seed()
	
	def rollNC(self):
		return (random.randint(1, 100) > (90 - self.noncom))
	
	def runAdv(self):
	#returns true if adventure spent
		if (self.turnsspent % 7 == 0):
			return self.runNCAdv()
		elif (self.remainingClovers > 0):
			return self.runCloverNC()
		elif (self.rollNC()):
			return self.runNCAdv()
		else:
			return self.runCombatAdv()
			
	def runCombatAdv(self):
		self.protesters -= 1
		return True
	
	def runNCAdv(self):
		reroll = True
		adv = ""
		while reroll:
			reroll = False
			adv = random.choice(self.zoneNCs)
			if logging:
				print("Rolled " + adv + " as NC")
			for NC in self.ncomQueue:
				if (NC == adv) and (random.randint(1, 4) > 1):
					reroll = True
					if logging:
						print("Rerolling!")
					break
		self.ncomQueue.append(adv)
		if logging:
			print("Locked in. Noncombat queue is now " + self.ncomQueue)
		if adv == "benchWarrant":
			return self.runBenchWarrant()
		if adv == "amBush":
			return self.runAmBush()
		if adv == "fireAbove":
			return self.runFireAbove()
		return False #something has gone very wrong
		
	
	def runBenchWarrant(self):
		rolled = self.benchWarrantProtesters()
		self.protesters -= rolled
		return True
	
	def runAmBush(self):
		self.protesters -= self.amBushProtesters()
		return True
	
	def runFireAbove(self):
		self.protesters -= self.fireAboveProtesters()
		self.remainingCocktails -= 1
		return True
		
	def runCloverNC(self):
		self.remainingClovers -= 1
		if self.amBushProtesters() > self.pessimisticBenchWarrantProtesters():
			if self.amBushProtesters() > self.fireAboveProtesters():
				return self.runAmBush()
			else:
				return self.runFireAbove()
		else: 
			if self.pessimisticBenchWarrantProtesters() >= self.fireAboveProtesters():
				return self.runBenchWarrant()
			else:
				return self.runFireAbove()
	
	def benchWarrantProtesters(self):
		return max(3, randomRound(math.sqrt(self.sleaze)))
	
	def pessimisticBenchWarrantProtesters(self):
		return max(3, math.floor(math.sqrt(self.sleaze)))
		
	def amBushProtesters(self):
		return max(3, self.lynyrdness)
		
	def fireAboveProtesters(self):
		return 10 if self.remainingCocktails > 0 else 3
	
	def runZeppelinMob(self):
		self.prepareRun()
		if logging:
			print("Noncombat adventure: Too Much Humanity")
		while self.protesters > 0:
			if self.runAdv():
				self.turnsspent += 1
		self.turnsspent += 1 #not so much with the humanity
		if logging:
			print("Noncombat adventure: Not So Much With The Humanity")
			print("Zeppelin Mob Cleared in " + str(self.turnsspent) + " turns")
		return self.turnsspent
	
	def runSimulations(self, runcount = 5000):
		runs = []
		for i in range(runcount):
			runs.append(self.runZeppelinMob())
		return [statistics.mean(runs), statistics.harmonic_mean(runs), statistics.median(runs), statistics.pstdev(runs)]
		
print(protestSim().runSimulations())
