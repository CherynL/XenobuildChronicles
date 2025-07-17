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

# features to add:
#   Add frames
#   Weapons and attack
#   Level and base stats
#   Extra gem slot options
#   skill trees and skill linking
#   Affinity coins for skill linking

# Excel File
XenobuildData = 'Xenobuild.v2.xlsx'
# Sheet Names
CS = "Characters" # as in Character Select
HE = "Head_Equip"
TE = "Torso_Equip"
AE = "Arm_Equip"
LE = "Leg_Equip"
FE = "Foot_Equip"
GU = "Gems_Unlinked" # Unlinked, Manually edited
GR = "Gems_ByRank" # Includes used for minimum and maximum
GV = "Gems_Values" # List of all possible gem values
GB = "Gems_Bestest" # Only rank 6 Gems


# Parameters
GS = 2 # Gem Slot Column
PD = GS+3 # Because the Gems can take up a lot of space

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
# Gem Dataframe by Rank
GR_df = pd.read_excel(XenobuildData, sheet_name=GR)
# All Possible Gem Values Dataframe
GV_df = pd.read_excel(XenobuildData, sheet_name=GV)
# Bestest Gems Dataframe
GB_df = pd.read_excel(XenobuildData, sheet_name=GB)
GB_df.set_index('Gem', inplace=True)

# For storing Character builds
class Character:
    
    def __init__ (self, name = None, head = None, torso = None, arm = None, leg = None, foot = None, p_def = 0, e_def = 0):
        self.name = name
        self.head = head
        self.torso = torso
        self.arm = arm
        self.leg = leg
        self.foot = foot
        self.p_def = p_def
        self.e_def = e_def

# This class will make the equipment updating way easier.
class Equipment:

    def __init__ (self, name = None, sheet_name = None, combobox = None, gem = None, rank = '–', value = 0, p_def = 0, e_def = 0, weight = 0):
        self.name = name
        self.sheet_name = sheet_name
        self.combobox = combobox
        self.gem = gem
        self.rank = rank
        self.value = value
        self.p_def = p_def
        self.e_def = e_def
        self.weight = weight

head = Equipment('Head', HE)
torso = Equipment('Torso',TE)
arm = Equipment('Arm', AE)
leg = Equipment('Leg', LE)
foot = Equipment('Foot', FE)
equips = [head, torso, arm, leg, foot]
# Updating for equippable armour
def update_items(*args):
    selected_character = character_combobox.get() # update valid armour
    equips = [
        head, torso, arm, leg, foot
    ]
    # Making 'Name' the index
    for i in equips:
        df = pd.read_excel(XenobuildData, sheet_name=i.sheet_name)
        df.set_index('Name', inplace=True)
        i.combobox["values"] = df[df[selected_character]].index.tolist()
        i.combobox.set("Not Equipped") #reset
        i.gem.set("Unslotted") #reset

# Updating Stats and slots
def update_stats(*args):
    equips = [head, torso, arm, leg, foot] # I wonder if there's an easier way to bulk-assign values in python
    for i in equips:
        df = pd.read_excel(XenobuildData, sheet_name=i.sheet_name)
        df.set_index('Name', inplace=True)
        # Gem Slot selection when equipment is chosen
        gem_type = df.at[i.combobox.get(),  'Gem']
        match gem_type:
            case 'Open':
                i.gem["values"] = GB_df[GB_df['Equipment'].isin(['Armour', 'All'])].index.tolist()[1:]
                if i.gem.get() == gem_type or i.gem.get() == 'Unslotted': i.gem.set("Open")
                i.rank.config(text = GB_df.at[i.gem.get(), 'Rank'])
                i.value.config(text = GB_df.at[i.gem.get(), 'Value'])
                #reset 
                # TODO add functionality to either save the gems to the armour or bind gems separately.
                #rank["values"] = [GR_df['Rank'][i] while ]
                #rank.set(df.at[combobox.get(), 'Rank'])
            case _: # works for uniques and no-slots
                i.gem["values"] = []
                i.gem.set(gem_type)
                i.rank.config(text = df.at[i.combobox.get(), 'Rank'])
                #rank["values"] = [df.at[combobox.get(), 'Rank']]
                #rank.set(df.at[combobox.get(), 'Rank'])
                i.value.config(text = df.at[i.combobox.get(), 'Value'])
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

# Updating gems
def update_gems(*args):
    equips = [head, torso, arm, leg, foot] # I wonder if there's an easier way to bulk-assign values in python
    for i in equips:
        df = pd.read_excel(XenobuildData, sheet_name=i.sheet_name)
        df.set_index('Name', inplace=True)
        # Gem slot selection for Open Gem Slots
        gem_type = df.at[i.combobox.get(),  'Gem']
        match gem_type:
            case 'Open':
                i.gem["values"] = GU_df.index.tolist()
                i.rank.config(text = GB_df.at[i.gem.get(), 'Rank'])
                print(GB_df.at[i.gem.get(), 'Rank'])
                i.value.config(text = GB_df.at[i.gem.get(), 'Value'])
                print(GB_df.at[i.gem.get(), 'Value'])
            case _: # works for uniques and no-slots
                print(gem_type)
                i.gem["values"] = [gem_type]
                i.gem.set(gem_type)
                i.rank.config(text = df.at[i.combobox.get(), 'Rank'])
                i.value.config(text = df.at[i.combobox.get(), 'Value'])
        

# Starting the Window
root = tk.Tk()
root.title("Xenobuild Chronicles")

# Character Dropdown
character_label = ttk.Label(root, text="Character")
character_label.grid(row=0, column=0, padx=5, pady=5)

character_combobox = ttk.Combobox(root, values=list(CS_df.index),state='readonly',width=18)
character_combobox.set("Select...")
character_combobox.grid(row=0, column=1, padx=5, pady=5)

# Equips Dropdown
equip_comboboxes = []
equip_gems = []; equip_ranks = []; equip_values = []
equip_p_defs = []; equip_e_defs = []; equip_weights = []
stat_totals = []
parts = ['Head', 'Torso', 'Arm', 'Leg', 'Foot']


for i, part in enumerate(parts):
    # Label for each section (e.g., "Head", "Torso")
    equip_label = ttk.Label(root, text=part)
    equip_label.grid(row=i+1, column=0, padx=5, pady=5)
    # Combobox for each Part
    equip_combobox = ttk.Combobox(root, state='readonly',width=18)
    equip_combobox.grid(row=i+1, column=1, padx=5, pady=5)
    equip_comboboxes.append((equip_combobox))
    # Gem slot label/combobox for each part
    gem = ttk.Combobox(root, state='readonly',width=15)
    gem.grid(row=i+1, column=GS, padx=5, pady=5)
    equip_gems.append((gem))
    # Rank
    rank = ttk.Label(root, text="–")
    # rank = ttk.Combobox(root, state='readonly')
    rank.grid(row=i+1, column=GS+1, padx=5, pady=5)
    equip_ranks.append((rank))
    # Value
    value = ttk.Label(root, text=0)
    #value = ttk.Combobox(root, state='readonly')
    value.grid(row=i+1, column=GS+2, padx=5, pady=5)
    equip_values.append((value))
    
    # P Def label for each part
    p_def = ttk.Label(root, text=0)
    p_def.grid(row=i+1, column=PD, padx=5, pady=5)
    equip_p_defs.append((p_def))
    #E Def label for each part
    e_def = ttk.Label(root, text=0)
    e_def.grid(row=i+1, column=PD+1, padx=5, pady=5)
    equip_e_defs.append((e_def))
    # Weight label for each part
    weight = ttk.Label(root, text=0)
    weight.grid(row=i+1, column=PD+2, padx=5, pady=5)
    equip_weights.append((weight))



head.combobox,  torso.combobox, arm.combobox,   leg.combobox,   foot.combobox   = [w for w in equip_comboboxes]
head.gem,       torso.gem,      arm.gem,        leg.gem,        foot.gem        = [w for w in equip_gems]
head.rank,      torso.rank,     arm.rank,       leg.rank,       foot.rank       = [w for w in equip_ranks]
head.value,     torso.value,    arm.value,      leg.value,      foot.value      = [w for w in equip_values]
head.p_def,     torso.p_def,    arm.p_def,      leg.p_def,      foot.p_def      = [w for w in equip_p_defs]
head.e_def,     torso.e_def,    arm.e_def,      leg.e_def,      foot.e_def      = [w for w in equip_e_defs]
head.weight,    torso.weight,   arm.weight,     leg.weight,     foot.weight     = [w for w in equip_weights]


# Gem Labels:
ttk.Label(root, text='Gem Slot').grid(row=0, column=GS, padx=5, pady=5) # Slot
ttk.Label(root, text='Rank').grid(row=0, column=GS+1, padx=5, pady=5) # Rank
ttk.Label(root, text='Value').grid(row=0, column=GS+2, padx=5, pady=5) # Value
# Defensive Stat Totals
ttk.Label(root, text="Total").grid(row=6, column=PD-1, padx=5, pady=5)
stat_names = ['P Def','E Def','Weight']
for i, label_name in enumerate(stat_names):
    label_total = ttk.Label(root,text=label_name).grid(row=0, column=PD+i, padx=5, pady=5)
    total = ttk.Label(root, text=0)
    total.grid(row=6, column=PD+i, padx=5, pady=5)
    stat_totals.append((total))

total_p_def, total_e_def, total_weight = [w for w in stat_totals]

# Binding the equip options for Characters
character_combobox.bind("<<ComboboxSelected>>", update_items)
# Binding stats for Equips
for w in equip_comboboxes:  w.bind("<<ComboboxSelected>>", update_stats)
# Binding for gems
for w in equip_gems: w.bind("<<ComboboxSelected>>", update_stats)

# Happens at the end
root.mainloop()
