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
#   Added levels
#   Added Weapon selection
#       Weapons clarify if they can damage Mechon and Faces
#       Monado damage scales with level

# features to add:
#   Auto-attack
#   Base stats
#   Gem Calculations
#   Extra gem slot options
#   skill trees and skill linking
#   Affinity coins for skill linking

# ----------
# Excel File
# ----------

XenobuildData = 'Xenobuild.v3.xlsx'
# Sheet Names
# Character Stat Tables not Included as Variables
HE = "Head_Equip"
TE = "Torso_Equip"
AE = "Arm_Equip"
LE = "Leg_Equip"
FE = "Foot_Equip"
GU = "Gems_Unlinked" # Unlinked, Manually edited
GB = "Gems_Bestest" # Only Rank VI Gems
WU = "Weapons_Unlinked"

# Gem Settings:
gem_options = ['Bestest', 'Best', 'Full', 'Worst', 'Worstest'] # TODO Add functionality for this. (After the skill trees I think)
gem_mode = 'Bestest'

# Methods
# Gem Dataframe
GU_df = pd.read_excel(XenobuildData, sheet_name=GU)
GU_df.set_index('Gem', inplace=True)
# Bestest Gems Dataframe
GB_df = pd.read_excel(XenobuildData, sheet_name=GB)
GB_df.set_index('Gem', inplace=True)
# Weapon Dataframe
WU_df = pd.read_excel(XenobuildData, sheet_name=WU)
WU_df.set_index('Name', inplace=True)

# Grid Parameters
GS = 2 # Gem Slot Column
PD = GS+3 # Because the Gems can take up a lot of space
WP = 5 # Weapon Row offset

# -------
# Classes
# -------

class Character: # These values are NOT tkinter widgets
    
    def __init__ (
            self, name = None, hp = 100, strength = 1, ether = 1, agility = 1,
            dmg_min = 1, dmg_max = 1, crit = 0, p_def = 0, e_def = 0, block = 0
            ):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.ether = ether
        self.agility = agility
        self.dmg_min = dmg_min
        self.dmg_max = dmg_max
        self.crit = crit
        self.p_def = p_def
        self.e_def = e_def
        self.block = block




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
character = Character()
weapon = Weapon()
head = Equipment('Head', HE)
torso = Equipment('Torso',TE)
arm = Equipment('Arm', AE)
leg = Equipment('Leg', LE)
foot = Equipment('Foot', FE)
equips = [head, torso, arm, leg, foot]
characters = ['Shulk','Reyn','Fiora','Dunban','Sharla','Riki','Melia','Seven']

# ---------------
# Bound Functions
# ---------------

# Updating for equippable armour
def update_items(*args):
    selected_character = character_combobox.get() # update valid armour
    CS_df = pd.read_excel(XenobuildData, sheet_name=selected_character)
    CS_df.set_index('Level', inplace=True)
    level_combobox["values"] = CS_df.index.tolist()
    level_combobox.set("99") #reset
    for g in [weapon.gem0,weapon.gem1,weapon.gem2]:
        g.combobox.set("Unslotted")
    default_weapon = WU_df[WU_df[selected_character]].index.tolist()
    weapon.combobox["values"] = default_weapon
    weapon.combobox.set(default_weapon[0])
    equips = [head, torso, arm, leg, foot]
    # Making 'Name' the index
    for i in equips:
        df = pd.read_excel(XenobuildData, sheet_name=i.sheet_name)
        df.set_index('Name', inplace=True)
        i.combobox["values"] = df[df[selected_character]].index.tolist()
        i.combobox.set("Not Equipped") #reset
        i.gem.combobox.set("Unslotted") #reset


# Updating Stats and slots
def update_equips(*args):
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

    update_totals()

    

def update_weapon(*args): # TODO WORK ON THIS SECTION
    
    for i, gem in enumerate([weapon.gem0, weapon.gem1, weapon.gem2]):
        # Gem Slot selection when equipment is 
        gem_type = WU_df.at[weapon.combobox.get(),  f"Gem.{i}"]
        match gem_type:
            case 'Open':
                gem.combobox["values"] = GB_df[GB_df['Equipment'].isin(['Weapon', 'All'])].index.tolist()[1:]
                if gem.combobox.get() == gem_type or gem.combobox.get() == 'Unslotted': gem.combobox.set('Open')
                gem.rank.config(text = GB_df.at[gem.combobox.get(), 'Rank'])
                gem.value.config(text = GB_df.at[gem.combobox.get(), 'Value'])
            case _: # works for uniques and no-slots
                gem.combobox["values"] = []
                gem.combobox.set(gem_type)
                gem.rank.config(text = WU_df.at[weapon.combobox.get(), f'Rank.{i}'])
                gem.value.config(text = WU_df.at[weapon.combobox.get(), f'Value.{i}'])
    # Weapon Stats
    misc_flag = WU_df.at[weapon.combobox.get(), "Misc_Flag"]
    if(misc_flag >= 3): anti_mechon_flag.config(text="YES")
    else: anti_mechon_flag.config(text="NO")
    if(misc_flag >= 5): min_mod = int(level_combobox.get())*1.4; max_mod = int(level_combobox.get())*1.5
    else: min_mod = max_mod = 1
    if(misc_flag >= 7): unshackled_flag.config(text='YES')
    else: unshackled_flag.config(text='NO')

    weapon.dmg_min.config(text=min(int(WU_df.at[weapon.combobox.get(), 'Dmg_Min']*min_mod),999))
    weapon.dmg_max.config(text=min(int(WU_df.at[weapon.combobox.get(), 'Dmg_Max']*max_mod),999))
    weapon.crit.config(text=WU_df.at[weapon.combobox.get(), 'Crit'])
    weapon.p_def.config(text=WU_df.at[weapon.combobox.get(), 'Phy_Def'])
    weapon.e_def.config(text=WU_df.at[weapon.combobox.get(), 'Eth_Def'])
    weapon.block.config(text=WU_df.at[weapon.combobox.get(), 'Block'])

    update_totals()


def update_totals():
    # Defenses (NO GEMS)
    p_def_sum = sum([int(c["text"]) for c in equip_p_defs])+int(weapon.p_def["text"])+character.p_def
    total_p_def.config(text=p_def_sum)
    e_def_sum = sum([int(c["text"]) for c in equip_e_defs])+int(weapon.e_def["text"])+character.e_def
    total_e_def.config(text=e_def_sum)
    
    # Weight
    weight_sum = sum([int(c["text"]) for c in equip_weights])
    total_weight.config(text=weight_sum)

def update_stats():
    CS_df = pd.read_excel(XenobuildData, sheet_name=character_combobox.get())
    CS_df.set_index('Level', inplace=True)
    level = level_combobox.get()
    hp = CS_df.at[level,'HP']
    strength = CS_df.at[level,'Strength']
    ether = CS_df.at[level,'Ether']
    agility = CS_df.at[level,'Agility']

# ------
# WINDOW
# ------

# Starting the Window
root = tk.Tk()
root.title("Xenobuild Chronicles")
# Character Dropdown
character_frame = tk.Frame(root, borderwidth=5,relief='groove')
character_frame.grid(row=0, column=0, sticky="W")
#character_label = ttk.Label(character_frame, text="Character")
#character_label.grid(row=0, column=0, padx=5, pady=5)
ttk.Label(character_frame, text="Character").grid(row=0, column=0, padx=5, pady=5)
character_combobox = ttk.Combobox(character_frame, values=characters,state='readonly',width=8)
character_combobox.set("Select...")
character_combobox.grid(row=0, column=1, padx=5, pady=5)
# Level Dropdown
ttk.Label(character_frame, text="Lv").grid(row=0, column=2, padx=5, pady=5)
level_combobox = ttk.Combobox(character_frame, values=[],state='readonly',width=3)
level_combobox.grid(row=0, column=3, padx=5, pady=5)

# Equipment Frame
equips_frame = tk.Frame(root,borderwidth=5,relief='groove')
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

# Misc_Flag Frame
misc_flag_frame = tk.Frame(equips_frame)
misc_flag_frame.grid(row=2,column=0,rowspan=2,columnspan=2, sticky='W')
ttk.Label(misc_flag_frame, text='Anti-Mechon').grid(row=0,column=0, padx=5, pady=5)
ttk.Label(misc_flag_frame, text='Unshackled').grid(row=1,column=0, padx=5, pady=5)
anti_mechon = ttk.Label(misc_flag_frame, text='Anti-Mechon:')
anti_mechon.grid(row=0,column=0, padx=5, pady=5)
anti_mechon_flag = ttk.Label(misc_flag_frame, text='Y/N')
anti_mechon_flag.grid(row=0,column=1, padx=5, pady=5)
unshackled = ttk.Label(misc_flag_frame, text='Unshackled:')
unshackled.grid(row=1,column=0, padx=5, pady=5)
unshackled_flag = ttk.Label(misc_flag_frame, text='Y/N')
unshackled_flag.grid(row=1,column=1, padx=5, pady=5)

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

weapon.dmg_min, weapon.dmg_max, weapon.crit, weapon.p_def, weapon.e_def, weapon.block = [w for w in weapon_stats]

ttk.Separator(equips_frame,orient='horizontal').grid(row=WP-1,column=0,columnspan=8,sticky='ew',padx=5,pady=5)

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

# -----------
# STAT TOTALS
# -----------

# Defensive Stat Totals
ttk.Label(equips_frame, text="Total").grid(row=6+WP, column=PD-1, padx=5, pady=5)
for i, label_name in enumerate(['P Def','E Def','Weight']):
    ttk.Label(equips_frame,text=label_name).grid(row=WP, column=PD+i, padx=5, pady=5)
    total = ttk.Label(equips_frame, text=0)
    total.grid(row=6+WP, column=PD+i, padx=5, pady=5)
    stat_totals.append((total))

total_p_def, total_e_def, total_weight = [w for w in stat_totals]
'''
# ---------------
# Character Stats
# ---------------

stat_frame = tk.Frame(root, borderwidth=5, relief='groove')
stat_frame.grid(row=0, column=1,rowspan=2,padx=5,pady=5)
ttk.Label(stat_frame,text="HP").grid(row=0,column=0,padx=5,pady=5)
ttk.Label(stat_frame,text="Strength").grid(row=1,column=0,padx=5,pady=5)
ttk.Label(stat_frame,text="Ether").grid(row=2,column=0,padx=5,pady=5)
ttk.Label(stat_frame,text="Agility").grid(row=3,column=0,padx=5,pady=5)

hp = ttk.Label(stat_frame,text="–")
hp.grid(row=0,column=1,padx=5,pady=5)
strength = ttk.Label(stat_frame,text="–")
strength.grid(row=1,column=1,padx=5,pady=5)
ether = ttk.Label(stat_frame,text="–")
ether.grid(row=2,column=1,padx=5,pady=5)
agility = ttk.Label(stat_frame,text="–")
agility.grid(row=3,column=1,padx=5,pady=5)
'''
# -------
# BINDING
# -------

# Binding the equip options for Characters
character_combobox.bind("<<ComboboxSelected>>", update_items)
character_combobox.bind("<<ComboboxSelected>>", update_weapon, add='+')
# Binding stats for the Level
level_combobox.bind("<<ComboboxSelected>>", update_weapon)
level_combobox.bind("<<ComboboxSelected>>", update_equips)
# Binding stats for Equips
for w in equip_comboboxes: w.bind("<<ComboboxSelected>>", update_equips)
# Binding for gems
for w in equip_gems: w.bind("<<ComboboxSelected>>", update_equips)

weapon.combobox.bind("<<ComboboxSelected>>", update_weapon)
for w in weapon_gems: w.bind("<<ComboboxSelected>>", update_weapon)

# Happens at the end
root.mainloop()