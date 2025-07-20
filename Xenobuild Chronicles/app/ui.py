import tkinter as tk
from tkinter import ttk
from app.constants import (
    GEM_SLOT_COLUMN as GS, PHYSICAL_DEFENSE_OFFSET as PD, WEAPON_ROW_OFFSET as WP,
    CHARACTER_NAMES as characters
)

parts = ['Head', 'Torso', 'Arm', 'Leg', 'Foot']
def build_ui(character, weapon, equips, p_defs, e_defs, weights):

    weapon_stats = []
    weapon_gems = []; weapon_ranks = []; weapon_values = []
    comboboxes = []
    gems = []; ranks = []; values = []
    # Starting the Window
    root = tk.Tk()
    root.title("Xenobuild Chronicles")
    # Character Dropdown
    character_frame = tk.Frame(root, borderwidth=5,relief='groove')
    character_frame.grid(row=0, column=0, sticky="W")
    ttk.Label(character_frame, text="Character").grid(row=0, column=0, padx=5, pady=5)
    character.name = ttk.Combobox(character_frame, values=characters,state='readonly',width=8)
    character.name.set("Select...")
    character.name.grid(row=0, column=1, padx=5, pady=5)
    # Level Dropdown
    ttk.Label(character_frame, text="Lv").grid(row=0, column=2, padx=5, pady=5)
    character.level = ttk.Combobox(character_frame, values=[],state='readonly',width=3)
    character.level.grid(row=0, column=3, padx=5, pady=5)

    # Equipment Frame
    equips_frame = tk.Frame(root,borderwidth=5,relief='groove')
    equips_frame.grid(row=1, column=0)


    # weapon Labels
    ttk.Label(equips_frame, text='Equipment').grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(equips_frame, text='Gem Slot').grid(row=0, column=GS, padx=5, pady=5) # Slot
    ttk.Label(equips_frame, text='Rank').grid(row=0, column=GS+1, padx=5, pady=5) # Rank
    ttk.Label(equips_frame, text='Value').grid(row=0, column=GS+2, padx=5, pady=5) # Value

    # weapons Dropdown
    ttk.Label(equips_frame, text='Weapon').grid(row=1, column=0, padx=5, pady=5)
    weapon.combobox = ttk.Combobox(equips_frame, state='readonly',width=18)
    weapon.combobox.grid(row=1, column=1, padx=5, pady=5)

    # Misc_Flag Frame
    misc_flag_frame = tk.Frame(equips_frame)
    misc_flag_frame.grid(row=2,column=0,rowspan=2,columnspan=2, sticky='W')
    ttk.Label(misc_flag_frame, text='Anti-Mechon').grid(row=0,column=0, padx=5, pady=5)
    ttk.Label(misc_flag_frame, text='Unshackled').grid(row=1,column=0, padx=5, pady=5)
    weapon.anti_mechon = ttk.Label(misc_flag_frame, text='Y/N')
    weapon.anti_mechon.grid(row=0,column=1, padx=5, pady=5)
    weapon.unshackled = ttk.Label(misc_flag_frame, text='Y/N')
    weapon.unshackled.grid(row=1,column=1, padx=5, pady=5)

    # weapon Stats


    # weapon Gems
    for i in range(3):
        # Gem slot label/combobox for each part
        combobox = ttk.Combobox(equips_frame, state='readonly',width=15)
        combobox.grid(row=i+1, column=GS, padx=5, pady=5)
        weapon_gems.append((combobox))
        # Rank
        rank = ttk.Combobox(equips_frame, state='readonly',width=5)
        rank.grid(row=i+1, column=GS+1, padx=5, pady=5)
        weapon_ranks.append((rank))
        # Value
        value = ttk.Combobox(equips_frame, state='readonly',width=5)
        value.grid(row=i+1, column=GS+2, padx=5, pady=5)
        weapon_values.append((value))

    weapon.gem0.combobox, weapon.gem1.combobox, weapon.gem2.combobox = [w for w in weapon_gems]
    weapon.gem0.rank, weapon.gem1.rank, weapon.gem2.rank = [w for w in weapon_ranks]
    weapon.gem0.value, weapon.gem1.value, weapon.gem2.value = [w for w in weapon_values]


    weapon_display = enumerate(['Min', 'Max', 'Crit','P Def', 'E Def', 'Block'])
    # 0 1 2 (Modulus to iterate through columns)
    # 3 4 5 (Floor division to split it into rows of 3)
    for i,label_name in weapon_display:
        ttk.Label(equips_frame,text=label_name).grid(row=i//3*2, column=PD+(i%3), padx=5, pady=5)
        stat = ttk.Label(equips_frame, text=0)
        stat.grid(row=i//3*2+1, column=PD+(i%3), padx=5, pady=5)
        weapon_stats.append((stat))

    weapon.dmg_min, weapon.dmg_max, weapon.crit, weapon.p_def, weapon.e_def, weapon.block = [w for w in weapon_stats]

    ttk.Separator(equips_frame,orient='horizontal').grid(row=WP-1,column=0,columnspan=8,sticky='ew',padx=5,pady=5)

    ttk.Label(equips_frame, text='Equipment').grid(row=WP, column=1, padx=5, pady=5)
    ttk.Label(equips_frame, text='Gem Slot').grid(row=WP, column=GS, padx=5, pady=5) # Slot
    ttk.Label(equips_frame, text='Rank').grid(row=WP, column=GS+1, padx=5, pady=5) # Rank
    ttk.Label(equips_frame, text='Value').grid(row=WP, column=GS+2, padx=5, pady=5) # Value
    ttk.Label(equips_frame, text='P Def').grid(row=WP, column=PD, padx=5, pady=5)
    ttk.Label(equips_frame, text='E Def').grid(row=WP, column=PD+1, padx=5, pady=5)
    ttk.Label(equips_frame, text='Weight').grid(row=WP, column=PD+2, padx=5, pady=5)

    # Each Equipment Piece
    for i, part in enumerate(parts):
        # Label for each section (e.g., "Head", "Torso")
        equip = ttk.Label(equips_frame, text=part)
        equip.grid(row=i+WP+1, column=0, padx=5, pady=5)
        # Combobox for each Part
        combobox = ttk.Combobox(equips_frame, state='readonly',width=18)
        combobox.grid(row=i+WP+1, column=1, padx=5, pady=5)
        comboboxes.append((combobox))
        # Gem slot label/combobox for each part
        gem = ttk.Combobox(equips_frame, state='readonly',width=15)
        gem.grid(row=i+WP+1, column=GS, padx=5, pady=5)
        gems.append((gem))
        # Rank
        rank = ttk.Combobox(equips_frame, state='readonly',width=5)
        rank.grid(row=i+WP+1, column=GS+1, padx=5, pady=5)
        ranks.append((rank))
        # Value
        value = ttk.Combobox(equips_frame, state='readonly',width=5)
        value.grid(row=i+WP+1, column=GS+2, padx=5, pady=5)
        values.append((value))
        
        # P Def label for each part
        p_def = ttk.Label(equips_frame, text=0)
        p_def.grid(row=i+WP+1, column=PD, padx=5, pady=5)
        p_defs.append((p_def))
        #E Def label for each part
        e_def = ttk.Label(equips_frame, text=0)
        e_def.grid(row=i+WP+1, column=PD+1, padx=5, pady=5)
        e_defs.append((e_def))
        # Weight label for each part
        weight = ttk.Label(equips_frame, text=0)
        weight.grid(row=i+WP+1, column=PD+2, padx=5, pady=5)
        weights.append((weight))

    for eq, c, g, r, v, pd, ed, wt in zip(equips, comboboxes, gems, ranks, values, p_defs, e_defs, weights):
        eq.combobox = c
        eq.gem.combobox = g
        eq.gem.rank = r
        eq.gem.value = v
        eq.p_def = pd
        eq.e_def = ed
        eq.weight = wt

    # ---------------
    # Character Stats
    # ---------------

    stat_frame = tk.Frame(root, borderwidth=5, relief='groove')
    stat_frame.grid(row=0, column=1,rowspan=2,padx=5,pady=5)

    ttk.Label(stat_frame,text="HP").grid(row=0,column=0,padx=5,pady=5)
    ttk.Label(stat_frame,text="Strength").grid(row=1,column=0,padx=5,pady=5)
    ttk.Label(stat_frame,text="Ether").grid(row=2,column=0,padx=5,pady=5)
    ttk.Label(stat_frame,text="Agility").grid(row=3,column=0,padx=5,pady=5)

    character.hp = ttk.Label(stat_frame,text="–")
    character.hp.grid(row=0,column=1,padx=5,pady=5)
    character.strength = ttk.Label(stat_frame,text="–")
    character.strength.grid(row=1,column=1,padx=5,pady=5)
    character.ether = ttk.Label(stat_frame,text="–")
    character.ether.grid(row=2,column=1,padx=5,pady=5)
    character.agility = ttk.Label(stat_frame,text="–")
    character.agility.grid(row=3,column=1,padx=5,pady=5)

    ttk.Separator(stat_frame,orient='horizontal').grid(row=4,column=0,columnspan=8,sticky='ew',padx=5,pady=5)

    ttk.Label(stat_frame,text='P Def').grid(row=5, column=0, padx=5, pady=5)
    ttk.Label(stat_frame,text='E Def').grid(row=6, column=0, padx=5, pady=5)
    ttk.Label(stat_frame,text='Weight').grid(row=7, column=0, padx=5, pady=5)

    character.p_def = ttk.Label(stat_frame, text="–")
    character.p_def.grid(row=5, column=1, padx=5, pady=5)
    character.e_def = ttk.Label(stat_frame, text="–")
    character.e_def.grid(row=6, column=1, padx=5, pady=5)
    character.weight = ttk.Label(stat_frame, text="–")
    character.weight.grid(row=7, column=1, padx=5, pady=5)

    return root