import pandas as pd
import tkinter as tk
from tkinter import ttk

# v1 features: 
#   Selecting armour pieces by character
#       (assumes Heavy Equipment and Medium Equipment skills are either learned or linked)
#   Will display physical defense, ether defense, and weight for each piece of equipment
#   Will display totals

# features to add:
#   Level and base stats
#   gem slot funcitonality
#   skill trees and skill linking
#   Weapons
#   Affinity coins for skill linking

#Sheet Names
CS = "Characters" # as in Character Select
HE = "Head_Equip"
TE = "Torso_Equip"
AE = "Arm_Equip"
LE = "Leg_Equip"
FE = "Foot_Equip"

# Updating for valid armour
def update_items(*args):
    selected_character = character_combobox.get() # update valid armour

    equips = [
        (HE, head_combobox),
        (TE, torso_combobox),
        (AE, arm_combobox),
        (LE, leg_combobox),
        (FE, foot_combobox)
    ]
    
    for equip, combobox in equips:
        df = pd.read_excel('Xenobuild.v1.xlsx', sheet_name=equip)
        df.set_index('Name', inplace=True)
        combobox["values"] = df[df[selected_character]].index.tolist()
        combobox.set("Not Equipped") #reset

def update_stats(*args):
    equips = [
        (1, HE, head_combobox, head_p_def, head_e_def, head_weight),
        (2, TE, torso_combobox, torso_p_def, torso_e_def, torso_weight),
        (3, AE, arm_combobox, arm_p_def, arm_e_def, arm_weight),
        (4, LE, leg_combobox, leg_p_def, leg_e_def, leg_weight),
        (5, FE, foot_combobox, foot_p_def, foot_e_def, foot_weight)
    ]

    for i, equip, combobox, p_def, e_def, weight in equips:
        df = pd.read_excel('Xenobuild.v1.xlsx', sheet_name=equip)
        df.set_index('Name', inplace=True)
        p_def.config(text=df.at[combobox.get(),'Phy_Def'])
        e_def.config(text=df.at[combobox.get(),'Eth_Def'])
        weight.config(text=df.at[combobox.get(),'Weight'])

    stats_totals = [
        (total_p_def, equip_p_def),
        (total_e_def, equip_e_def),
        (total_weight, equip_weight)
        ]
    for total, equip in stats_totals:
        stat_sum=sum([int(w["text"]) for w in equip])
        total.config(text=stat_sum)

root = tk.Tk()
root.title("Xenobuild Chronicles")

# Character Dropdown
character_label = ttk.Label(root, text="Character")
character_label.grid(row=0, column=0, padx=5, pady=5)

CS_df = pd.read_excel('Xenobuild.v1.xlsx', sheet_name=CS)
CS_df.set_index('Name', inplace=True)
character_combobox = ttk.Combobox(root, values=list(CS_df.index),state='readonly')
character_combobox.set("Select...")
character_combobox.grid(row=0, column=1, padx=5, pady=5)

# Equips Dropdown
equips_widgets = []
equip_p_def = []
equip_e_def = []
equip_weight = []
stat_totals = []
parts = ['Head', 'Torso', 'Arm', 'Leg', 'Foot']

for i, part in enumerate(parts):
    # Label for each section (e.g., "Head", "Torso")
    equip_label = ttk.Label(root, text=part)
    equip_label.grid(row=i+1, column=0, padx=5, pady=5)
    # Combobox for each Part
    equip_combobox = ttk.Combobox(root, state='readonly')
    equip_combobox.grid(row=i+1, column=1, padx=5, pady=5)
    equips_widgets.append((equip_combobox))
    # P Def label for each part
    p_def = ttk.Label(root, text=0)
    p_def.grid(row=i+1, column=2, padx=5, pady=5)
    equip_p_def.append((p_def))
    #E Def label for each part
    e_def = ttk.Label(root, text=0)
    e_def.grid(row=i+1, column=3, padx=5, pady=5)
    equip_e_def.append((e_def))
    # Weight label for each part
    weight = ttk.Label(root, text=0)
    weight.grid(row=i+1, column=4, padx=5, pady=5)
    equip_weight.append((weight))

head_combobox, torso_combobox, arm_combobox, leg_combobox, foot_combobox = [w for w in equips_widgets]
head_p_def, torso_p_def, arm_p_def, leg_p_def, foot_p_def = [w for w in equip_p_def]
head_e_def, torso_e_def, arm_e_def, leg_e_def, foot_e_def = [w for w in equip_e_def]
head_weight, torso_weight, arm_weight, leg_weight, foot_weight = [w for w in equip_weight]

    

# Full Stats:
ttk.Label(root, text="Total").grid(row=6, column=1, padx=5, pady=5)

stat_names = ['P Def','E Def','Weight']
for i, label_name in enumerate(stat_names):
    label_total = ttk.Label(root,text=label_name).grid(row=0, column=2+i, padx=5, pady=5)
    total = ttk.Label(root, text=0)
    total.grid(row=6, column=2+i, padx=5, pady=5)
    stat_totals.append((total))

total_p_def, total_e_def, total_weight = [w for w in stat_totals]

# Binding Character to the Equips
character_combobox.bind("<<ComboboxSelected>>", update_items)
head_combobox.bind("<<ComboboxSelected>>", update_stats)
torso_combobox.bind("<<ComboboxSelected>>", update_stats)
arm_combobox.bind("<<ComboboxSelected>>", update_stats)
leg_combobox.bind("<<ComboboxSelected>>", update_stats)
foot_combobox.bind("<<ComboboxSelected>>", update_stats)

# Happens at the end
root.mainloop()