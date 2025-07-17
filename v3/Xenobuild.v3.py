import pandas as pd
import tkinter as tk
from tkinter import ttk

# v1 features: 
#   Selecting armour pieces by character
#       (assumes Heavy Equipment and Medium Equipment skills are either learned or linked)
#       (assumes all armour names are unique)
#   Will display physical defense, ether defense, and weight for each piece of equipment
#   Will display totals

# v2 features:
#   Added gem slot functionality for armour
#   Selecting gems for Slotted equipment
#   Displays gem effects for Unique equipment
#   Only selecting the "Bestest" gems
#       Automatically selects highest rank and value for gems

# v3 features:
#   Add level slider

# features to add:
#   Add frames
#   Weapons and attack
#   Level and base stats
#   Extra gem slot options
#   skill trees and skill linking
#   Affinity coins for skill linking

# Excel File
XenobuildData = 'Xenobuild.v3.xlsx'
# Sheet Names
CS = "Characters" # as in Character Select
HE = "Head_Equip"
TE = "Torso_Equip"
AE = "Arm_Equip"
LE = "Leg_Equip"
FE = "Foot_Equip"
#GL = "Gems_Linked"
GU = "Gems_Unlinked" # Unlinked, Manually edited
#GR = "Gems_ByRank" # Includes used for minimum and maximum
#GV = "Gems_Values" # List of all possible gem values
GB = "Gems_Bestest" # Only Rank VI Gems
#WS = "Weapons_Source"
WU = "Weapons_Unlinked"



# Parameters
GS = 2 # Gem Slot Column
PD = GS+3 # Because the Gems can take up a lot of space
WP = 4 # Weapon Row offset

# Gem Settings:
gem_options = ['Bestest', 'Best', 'Full', 'Worst', 'Worstest'] # TODO Add functionality for this.
gem_mode = 'Bestest'

# Methods
# Character Dataframe
CS_df = pd.read_excel(XenobuildData, sheet_name=CS)
CS_df.set_index('Name', inplace=True)
# Gem Dataframe
GU_df = pd.read_excel(XenobuildData, sheet_name=GU)
GU_df.set_index('Gem', inplace=True)
# Bestest Gems Dataframe
GB_df = pd.read_excel(XenobuildData, sheet_name=GB)
GB_df.set_index('Gem', inplace=True)
# Weapon Dataframe
WU_df = pd.read_excel(XenobuildData, sheet_name=WU)
WU_df.set_index('Name', inplace=True)

'''
class Character:
    
    def __init__ (self, name = None, min_level = None, hp = None, strength = None, ether = None, agility = None):
        self.name = name
        self.min_level = min_level
        self.hp = hp
        self.strength = strength
        self.ether = ether
        self.agility = agility

'''


# Gem Class
class Gem:

    def __init__ (self, combobox = None, rank = None, value = None):
        self.combobox = combobox
        self.rank = rank
        self.value = value

# This is for Weapons
class Weapon:

    def __init__ (self, combobox = None, dmg_min = None, dmg_max = None, crit = None, p_def = None, e_def = None, block = None, gem0 = None, gem1 = None, gem2 = None):

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

# This class will make the equipment updating way easier.
class Equipment:

    def __init__ (self, name = None, sheet_name = None, combobox = None, gem = None, p_def = None, e_def = None, weight = None):
        self.name = name
        self.sheet_name = sheet_name
        self.combobox = combobox
        self.gem = Gem(gem)
        self.p_def = p_def
        self.e_def = e_def
        self.weight = weight

"""
# For storing Character builds
class Character_Build:
    
    def __init__ (self, name = None, level_combobox = 99, weapon = 0, p_def = 0, e_def = 0, head = Equipment(), torso = Equipment(), arm = Equipment(), leg = Equipment(), foot = Equipment()):
        self.name = name
        self.level_combobox = level_combobox
        self.weapon = weapon
        self.head = head
        self.torso = torso
        self.arm = arm
        self.leg = leg
        self.foot = foot
"""
weapon = Weapon()
head = Equipment('Head', HE)
torso = Equipment('Torso',TE)
arm = Equipment('Arm', AE)
leg = Equipment('Leg', LE)
foot = Equipment('Foot', FE)
equips = [head, torso, arm, leg, foot]
# Updating for equippable armour
def update_items(*args):
    selected_character = character_combobox.get() # update valid armour
    weapon.combobox.set("Select...") #reset
    weapon.combobox["values"] = WU_df[WU_df[selected_character]].index.tolist()
    weapon.gem0.combobox.set("Unslotted") #reset
    weapon.gem1.combobox.set("Unslotted") #reset
    weapon.gem2.combobox.set("Unslotted") #reset

    equips = [head, torso, arm, leg, foot]
    # Making 'Name' the index
    for i in equips:
        df = pd.read_excel(XenobuildData, sheet_name=i.sheet_name)
        df.set_index('Name', inplace=True)
        i.combobox["values"] = df[df[selected_character]].index.tolist()
        i.combobox.set("Not Equipped") #reset
        i.gem.combobox.set("Unslotted") #reset

# Updating Stats and slots
def update_equip_stats(*args):
    equips = [head, torso, arm, leg, foot] # I wonder if there's an easier way to bulk-assign values in python
    for i in equips:
        df = pd.read_excel(XenobuildData, sheet_name=i.sheet_name)
        df.set_index('Name', inplace=True)
        # Gem Slot selection when equipment is chosen
        gem_type = df.at[i.combobox.get(),  'Gem']
        match gem_type:
            case 'Open':
                i.gem.combobox["values"] = GU_df[GU_df['Equipment'].isin(['Armour', 'All'])].index.tolist()[1:]
                if i.gem.combobox.get() == gem_type or i.gem.combobox.get() == 'Unslotted': i.gem.combobox.set("Open")
                i.gem.rank.config(text = GB_df.at[i.gem.combobox.get(), 'Rank'])
                i.gem.value.config(text = GB_df.at[i.gem.combobox.get(), 'Value'])
                #reset 
                # TODO add functionality to either save the gems to the armour or bind gems separately.
                #rank["values"] = [GR_df['Rank'][i] while ]
                #rank.set(df.at[combobox.get(), 'Rank'])
            case _: # works for uniques and no-slots
                i.gem.combobox["values"] = []
                i.gem.combobox.set(gem_type)
                i.gem.rank.config(text = df.at[i.combobox.get(), 'Rank'])
                #rank["values"] = [df.at[combobox.get(), 'Rank']]
                #rank.set(df.at[combobox.get(), 'Rank'])
                i.gem.value.config(text = df.at[i.combobox.get(), 'Value'])
                #value["values"] = [df.at[combobox.get(), 'Value']]
                #value.set(df.at[combobox.get(), 'Value'])
        

        # The rest of the stats
        i.p_def.config(   text=df.at[i.combobox.get(),  'Phy_Def'])
        i.e_def.config(   text=df.at[i.combobox.get(),  'Eth_Def'])
        i.weight.config(  text=df.at[i.combobox.get(),  'Weight'])
    stats_totals = [
        (total_p_def, equip_p_defs),
        (total_e_def, equip_e_defs),
        (total_weight, equip_weights)
    ]
    for total, equip in stats_totals:
        stat_sum=sum([int(w["text"]) for w in equip])
        total.config(text=stat_sum)

def update_weapon_stats(*args): # TODO WORK ON THIS SECTION
    
    for i, gem in enumerate(weapon.gems):
        # Gem Slot selection when equipment is chosen
        gem_type = WU_df.at[gem.combobox.get(),  'Gem.'+i]
        match gem_type:
            case 'Open':
                gem.combobox["values"] = GB_df[GB_df['Equipment'].isin(['Weapon', 'All'])].index.tolist()[1:]
                if gem.combobox.get() == gem_type or gem.combobox.get() == 'Unslotted': gem.combobox.set("Open")
                gem.rank.config(text = GB_df.at[gem.combobox.get(), 'Rank.'+i])
                gem.value.config(text = GB_df.at[gem.combobox.get(), 'Value.'+i])
            case _: # works for uniques and no-slots
                gem.combobox["values"] = []
                gem.combobox.set(gem_type)
                gem.rank.config(text = WU_df.at[gem.combobox.get(), 'Rank.'+i])
                gem.value.config(text = WU_df.at[gem.combobox.get(), 'Value.'+i])
        
    '''
        # The rest of the stats
        i.p_def.config(   text=df.at[i.combobox.get(),  'Phy_Def'])
        i.e_def.config(   text=df.at[i.combobox.get(),  'Eth_Def'])
        i.weight.config(  text=df.at[i.combobox.get(),  'Weight'])
    stats_totals = [
        (total_p_def, equip_p_defs),
        (total_e_def, equip_e_defs),
        (total_weight, equip_weights)
    ]
    for total, equip in stats_totals:
        stat_sum=sum([int(w["text"]) for w in equip])
        total.config(text=stat_sum)
    '''

# Starting the Window
root = tk.Tk()
root.title("Xenobuild Chronicles")
# Character Dropdown
character_frame = tk.Frame(root)
character_frame.grid(row=0, column=0, sticky="W")
#character_label = ttk.Label(character_frame, text="Character")
#character_label.grid(row=0, column=0, padx=5, pady=5)
ttk.Label(character_frame, text="Character").grid(row=0, column=0, padx=5, pady=5)
character_combobox = ttk.Combobox(character_frame, values=list(CS_df.index),state='readonly',width=8)
character_combobox.set("Select...")
character_combobox.grid(row=0, column=1, padx=5, pady=5)
# Level Dropdown
ttk.Label(character_frame, text="Lv").grid(row=0, column=2, padx=5, pady=5)
level_combobox = ttk.Combobox(character_frame, values=[i for i in range(1,100)],state='readonly',width=3)
level_combobox.set("99")
level_combobox.grid(row=0, column=3, padx=5, pady=5)

# Equips Frame
equips_frame = tk.Frame(root)
equips_frame.grid(row=1, column=0)

# Labels
ttk.Label(equips_frame, text='Equipment').grid(row=0, column=1, padx=5, pady=5)
ttk.Label(equips_frame, text='Equipment').grid(row=WP, column=1, padx=5, pady=5)
ttk.Label(equips_frame, text='Gem Slot').grid(row=0, column=GS, padx=5, pady=5) # Slot
ttk.Label(equips_frame, text='Gem Slot').grid(row=WP, column=GS, padx=5, pady=5) # Slot
ttk.Label(equips_frame, text='Rank').grid(row=0, column=GS+1, padx=5, pady=5) # Rank
ttk.Label(equips_frame, text='Rank').grid(row=WP, column=GS+1, padx=5, pady=5) # Rank
ttk.Label(equips_frame, text='Value').grid(row=0, column=GS+2, padx=5, pady=5) # Value
ttk.Label(equips_frame, text='Value').grid(row=WP, column=GS+2, padx=5, pady=5) # Value

# Weapons Dropdown
ttk.Label(equips_frame, text='Weapon').grid(row=1, column=0, padx=5, pady=5)
weapon.combobox = ttk.Combobox(equips_frame, state='readonly',width=18)
weapon.combobox.grid(row=1, column=1, padx=5, pady=5)

# Weapon Stats
weapon_stats = []
weapon_gems = []; weapon_ranks = []; weapon_values = []

# Weapon Gems
for i in range(3):
    # Gem slot label/combobox for each part
    combobox = ttk.Combobox(equips_frame, state='readonly',width=15)
    combobox.grid(row=i+1, column=GS, padx=5, pady=5)
    weapon_gems.append((combobox))
    # Rank
    rank = ttk.Label(equips_frame, text="–")
    rank.grid(row=i+1, column=GS+1, padx=5, pady=5)
    weapon_ranks.append((rank))
    # Value
    value = ttk.Label(equips_frame, text=0)
    value.grid(row=i+1, column=GS+2, padx=5, pady=5)
    weapon_values.append((value))

weapon.gem0.combobox, weapon.gem1.combobox, weapon.gem2.combobox = [w for w in weapon_gems]
weapon.gem0.rank, weapon.gem1.rank, weapon.gem2.rank = [w for w in weapon_ranks]
weapon.gem0.value, weapon.gem1.value, weapon.gem2.value = [w for w in weapon_values]

for i, label_name in enumerate(['Min', 'Max', 'Crit']):
    ttk.Label(equips_frame,text=label_name).grid(row=0, column=PD+i, padx=5, pady=5)
    stat = ttk.Label(equips_frame, text=0)
    stat.grid(row=1, column=PD+i, padx=5, pady=5)
    weapon_stats.append((stat))

for i, label_name in enumerate(['P Def', 'E Def', 'Block']):
    ttk.Label(equips_frame,text=label_name).grid(row=2, column=PD+i, padx=5, pady=5)
    stat = ttk.Label(equips_frame, text=0)
    stat.grid(row=3, column=PD+i, padx=5, pady=5)
    weapon_stats.append((stat))

weapon.p_def, weapon.e_def, weapon.crit, weapon.p_def, weapon.e_def, weapon.block = [w for w in weapon_stats]

#   Empty,  Equipment,  [Gems], Dmg_Min,    Dmg_Max,    Crit
#   Weapon, Combobox,
#   Anti-Mechon?,   Y/N,        Phy_Def,    Eth_Def,    Block
#   Unshackled?,    Y/N,        


# Equips Dropdown
equip_comboboxes = []
equip_gems = []; equip_ranks = []; equip_values = []
equip_p_defs = []; equip_e_defs = []; equip_weights = []
stat_totals = []
parts = ['Head', 'Torso', 'Arm', 'Leg', 'Foot']

# Each Equipment Piece
for i, part in enumerate(parts):
    # Label for each section (e.g., "Head", "Torso")
    equip_label = ttk.Label(equips_frame, text=part)
    equip_label.grid(row=i+WP+1, column=0, padx=5, pady=5)
    # Combobox for each Part
    equip_combobox = ttk.Combobox(equips_frame, state='readonly',width=18)
    equip_combobox.grid(row=i+WP+1, column=1, padx=5, pady=5)
    equip_comboboxes.append((equip_combobox))
    # Gem slot label/combobox for each part
    gem_combobox = ttk.Combobox(equips_frame, state='readonly',width=15)
    gem_combobox.grid(row=i+WP+1, column=GS, padx=5, pady=5)
    equip_gems.append((gem_combobox))
    # Rank
    rank_label = ttk.Label(equips_frame, text="–")
    # rank = ttk.Combobox(equips_frame, state='readonly')
    rank_label.grid(row=i+WP+1, column=GS+1, padx=5, pady=5)
    equip_ranks.append((rank_label))
    # Value
    value_label = ttk.Label(equips_frame, text=0)
    #value = ttk.Combobox(equips_frame, state='readonly')
    value_label.grid(row=i+WP+1, column=GS+2, padx=5, pady=5)
    equip_values.append((value_label))
    
    # P Def label for each part
    p_def = ttk.Label(equips_frame, text=0)
    p_def.grid(row=i+WP+1, column=PD, padx=5, pady=5)
    equip_p_defs.append((p_def))
    #E Def label for each part
    e_def = ttk.Label(equips_frame, text=0)
    e_def.grid(row=i+WP+1, column=PD+1, padx=5, pady=5)
    equip_e_defs.append((e_def))
    # Weight label for each part
    weight = ttk.Label(equips_frame, text=0)
    weight.grid(row=i+WP+1, column=PD+2, padx=5, pady=5)
    equip_weights.append((weight))



head.combobox,      torso.combobox,     arm.combobox,       leg.combobox,       foot.combobox       = [w for w in equip_comboboxes]
head.gem.combobox,  torso.gem.combobox, arm.gem.combobox,   leg.gem.combobox,   foot.gem.combobox   = [w for w in equip_gems]
head.gem.rank,      torso.gem.rank,     arm.gem.rank,       leg.gem.rank,       foot.gem.rank       = [w for w in equip_ranks]
head.gem.value,     torso.gem.value,    arm.gem.value,      leg.gem.value,      foot.gem.value      = [w for w in equip_values]
head.p_def,         torso.p_def,        arm.p_def,          leg.p_def,          foot.p_def          = [w for w in equip_p_defs]
head.e_def,         torso.e_def,        arm.e_def,          leg.e_def,          foot.e_def          = [w for w in equip_e_defs]
head.weight,        torso.weight,       arm.weight,         leg.weight,         foot.weight         = [w for w in equip_weights]



# Defensive Stat Totals
ttk.Label(equips_frame, text="Total").grid(row=6+WP, column=PD-1, padx=5, pady=5)
for i, label_name in enumerate(['P Def','E Def','Weight']):
    ttk.Label(equips_frame,text=label_name).grid(row=WP, column=PD+i, padx=5, pady=5)
    total = ttk.Label(equips_frame, text=0)
    total.grid(row=6+WP, column=PD+i, padx=5, pady=5)
    stat_totals.append((total))

total_p_def, total_e_def, total_weight = [w for w in stat_totals]

# Binding the equip options for Characters
character_combobox.bind("<<ComboboxSelected>>", update_items)
# Binding stats for the Level
level_combobox.bind("<<ComboboxSelected>>", update_equip_stats)
# Binding stats for Equips
for w in equip_comboboxes:  w.bind("<<ComboboxSelected>>", update_equip_stats)
# Binding for gems
for w in equip_gems: w.bind("<<ComboboxSelected>>", update_equip_stats)

# Happens at the end
root.mainloop()
