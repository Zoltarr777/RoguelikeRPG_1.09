import tcod as libtcod

from game_messages import Message

from random import randint


class Fighter:
	def __init__(self, hp, defense, power, magic, talismanhp, gold, xp=0):
		self.base_max_hp = hp
		self.hp = hp
		self.base_defense = defense
		self.base_power = power
		self.base_magic = magic
		self.xp = xp
		self.talismanhp = talismanhp
		self.gold = gold

	@property
	def max_hp(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.max_hp_bonus
		else:
			bonus = 0

		return self.base_max_hp + bonus

	@property
	def power(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.power_bonus
		else:
			bonus = 0

		return self.base_power + bonus

	@property
	def defense(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.defense_bonus
		else:
			bonus = 0

		return self.base_defense + bonus

	@property
	def magic(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.magic_bonus
		else:
			bonus = 0

		return self.base_magic + bonus

	def take_damage(self, amount):
		results = []

		if self.talismanhp >= amount:
			self.talismanhp -= amount
		else:
			hpdamage = amount - self.talismanhp
			self.talismanhp -= self.talismanhp
			self.hp -= hpdamage

		if self.hp <= 0:
			results.append({'dead': self.owner, 'xp': self.xp})

		return results

	def heal(self, amount):
		self.hp += amount

		if self.hp > self.max_hp:
			self.hp = self.max_hp

	def sacrifice(self, amount):
		results = []

		self.hp -= amount
		self.talismanhp += amount

		if self.hp <= 0:
			results.append({'dead': self.owner, 'xp': self.xp})

		return results

	def equipment_heal(self, amount):
		self.hp += amount

		if self.hp > self.max_hp:
			self.hp = self.max_hp

	def attack(self, target):
		results = []

		attack_chance = randint(1, 20)

		damage = round(self.power * (10 / (10 + target.fighter.defense)))

		if 2 <= attack_chance <= 19:
			if damage > 0:
				results.append({'message': Message("{0} attacks {1} for {2} hit points.".format(self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
				results.extend(target.fighter.take_damage(damage))
			else:
				results.append({'message': Message("{0} attacks {1} but does no damage.".format(self.owner.name.capitalize(), target.name), libtcod.white)})
				results.extend(target.fighter.take_damage(damage))

		elif attack_chance == 1:
			dodgemiss = randint(1, 2)

			if dodgemiss == 1:
				results.append({'message': Message("{0} attacks {1} but {1} dodges!".format(self.owner.name.capitalize(), target.name), libtcod.white)})
			else:
				results.append({'message': Message("{0} attacks {1} but misses!".format(self.owner.name.capitalize(), target.name), libtcod.white)})

		elif attack_chance == 20:

			damage = damage * 2

			results.append({'message': Message("{0} attacks {1} and critical hits for {2} hit points!".format(self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
			results.extend(target.fighter.take_damage(damage))

		return results