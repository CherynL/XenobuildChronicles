# -------
# Classes
# -------

class Character():

    def __init__(self,
                 name = None, level = None,
                 hp = None, strength = None, ether = None, agility = None,
                 p_def = None, e_def = None, weight = None,
                 aa_min = None, aa_max = None, crit = None, block = None):
        self.name = name
        self.level = level
        # -------------
        self.hp = hp
        self.strength = strength
        self.ether = ether
        self.agility = agility
        # -------------
        self.p_def = p_def
        self.e_def = e_def
        self.weight = weight
        # -------------
        self.aa_min = aa_min
        self.aa_max = aa_max
        self.crit = crit
        self.block = block
    

# Gem Class
class Gem:

    def __init__ (self, combobox = None, rank = None, value = None):
        self.combobox = combobox
        self.rank = rank
        self.value = value

# This is for Weapons
class Weapon():
        
    def __init__(self,
                 combobox = None,
                 dmg_min = None, dmg_max = None, crit = None,
                 p_def = None,   e_def = None,   block = None,
                 gem0 = None,   gem1 = None,   gem2 = None,
                 anti_mechon = None, unshackled = None):
        self.combobox = combobox
        self.dmg_min = dmg_min
        self.dmg_max = dmg_max
        self.crit = crit
        self.p_def = p_def
        self.e_def = e_def
        self.block = block
        self.gem0 = Gem(gem0)
        self.gem1 = Gem(gem1)
        self.gem2 = Gem(gem2)
        self.anti_mechon = anti_mechon
        self.unshackled = unshackled
        

# This class will make the equipment updating way easier.
class Equipment:

    def __init__ (self, name = None, sheet_name = None, combobox = None, p_def = None, e_def = None, weight = None, gem = None):
        self.name = name
        self.sheet_name = sheet_name
        self.combobox = combobox
        self.p_def = p_def
        self.e_def = e_def
        self.weight = weight
        self.gem = Gem(gem)


class Loadout:

    def __init__ (self,
                  character = None,
                  weapon = None,
                  head = Equipment(), torso = Equipment(), arm = Equipment(), leg = Equipment(), foot = Equipment()):
        self.character = Character(character)
        self.weapon = Weapon(weapon)
        self.equips = [head, torso, arm, leg, foot]
        self.gems = [self.weapon.gem0, self.weapon.gem1, self.weapon.gem2, head.gem, torso.gem, arm.gem, leg.gem, foot.gem]
        self.effects = []
        self.gem_values = []