# Chat broke but I can do the rest
from itertools import combinations
from app.data_loader import load_sheet, WU_df, GR_df, GB_df
# ---------------
# Bound Functions
# ---------------

# Updating for equippable armour
def update_items(loadout):
    selected_character = loadout.character.name.get() # update valid armour
    CS_df = load_sheet(selected_character)
    CS_df.set_index('Level', inplace=True)
    loadout.character.level["values"] = CS_df.index.tolist()
    loadout.character.level.set("99") #reset
    for g in [loadout.weapon.gem0,loadout.weapon.gem1,loadout.weapon.gem2]:
        g.combobox.set("Unslotted")
        g.rank.set("–")
        g.value.set(0)
    default_weapon = WU_df[WU_df[selected_character]].index.tolist()
    loadout.weapon.combobox["values"] = default_weapon
    loadout.weapon.combobox.set(default_weapon[0])
    # Making 'Name' the index
    for i in loadout.equips:
        df = load_sheet(i.sheet_name)
        df.set_index('Name', inplace=True)
        i.combobox["values"] = df[df[selected_character]].index.tolist()
        i.combobox.set("Not Equipped") #reset
        i.gem.combobox.set("Unslotted") #reset
        i.gem.rank.set("–")
        i.gem.value.set(0)

def update_weapon(loadout): # TODO WORK ON THIS SECTION
    
    for i, g in enumerate([loadout.weapon.gem0, loadout.weapon.gem1, loadout.weapon.gem2]):
        # Gem Slot selection when equipment is 
        gem = WU_df.at[loadout.weapon.combobox.get(), f"Gem.{i}"]
        rank = WU_df.at[loadout.weapon.combobox.get(), f"Rank.{i}"]
        value = int(WU_df.at[loadout.weapon.combobox.get(), f"Value.{i}"]) # For some reason, this one wants to be a float
        match gem:
            case 'Open':
                g.combobox["values"] = GB_df[GB_df['Equipment'].isin(['Weapon', 'All'])].index.tolist()[1:]
                if g.combobox.get() == gem or g.combobox.get() == 'Unslotted':
                    g.combobox.set('Open')
                    g.rank.set('–')
                g.rank["values"] = GR_df[GR_df["Gem"] == g.combobox.get()]['Rank'].tolist()
                if g.rank.get() == GB_df.at[g.combobox.get(), 'Rank'] or g.rank.get() == '–':
                    g.rank.set(GB_df.at[g.combobox.get(), 'Rank']) # Autosets to max rank
                min_value = int(GR_df.at[(g.combobox.get(),g.rank.get()), 'Min'])
                max_value = int(GR_df.at[(g.combobox.get(),g.rank.get()), 'Max'])
                g.value["values"] = [r for r in range(min_value,max_value+1)]
                if int(g.value.get()) < min_value or int(g.value.get()) >= max_value:
                    g.value.set(GR_df.at[(g.combobox.get(),g.rank.get()), 'Max']) # Autosets to max value
            case _: # works for uniques and no-slots
                g.combobox["values"] = []
                g.combobox.set(gem)
                g.rank["values"] = []
                g.rank.set(rank)
                g.value["values"] = []
                g.value.set(value)
    # weapon Stats
    misc_flag = WU_df.at[loadout.weapon.combobox.get(), "Misc_Flag"]
    if(misc_flag >= 3): loadout.weapon.anti_mechon.config(text="YES")
    else: loadout.weapon.anti_mechon.config(text="NO")
    if(misc_flag >= 5): min_mod = int(loadout.character.level.get())*1.4; max_mod = int(loadout.character.level.get())*1.5
    else: min_mod = max_mod = 1
    if(misc_flag >= 7): loadout.weapon.unshackled.config(text='YES')
    else: loadout.weapon.unshackled.config(text='NO')

    loadout.weapon.dmg_min.config(text=min(int(WU_df.at[loadout.weapon.combobox.get(), 'Dmg_Min']*min_mod),999))
    loadout.weapon.dmg_max.config(text=min(int(WU_df.at[loadout.weapon.combobox.get(), 'Dmg_Max']*max_mod),999))
    loadout.weapon.crit.config(text=WU_df.at[loadout.weapon.combobox.get(), 'Crit'])
    loadout.weapon.p_def.config(text=WU_df.at[loadout.weapon.combobox.get(), 'Phy_Def'])
    loadout.weapon.e_def.config(text=WU_df.at[loadout.weapon.combobox.get(), 'Eth_Def'])
    loadout.weapon.block.config(text=WU_df.at[loadout.weapon.combobox.get(), 'Block'])

    update_totals(loadout)

# Updating Stats and slots
def update_equips(loadout):
    # I wonder if there's an easier way to bulk-assign values in python
    for i in loadout.equips:
        df = load_sheet(i.sheet_name)
        df.set_index('Name', inplace=True)
        # Gem Slot selection when equipment is chosen
        gem = df.at[i.combobox.get(), 'Gem']
        rank = df.at[i.combobox.get(), 'Rank']
        value = df.at[i.combobox.get(), 'Value']
        match gem:
            case 'Open':
                i.gem.combobox["values"] = GB_df[GB_df['Equipment'].isin(['Armour', 'All'])].index.tolist()[1:]
                if i.gem.combobox.get() == gem or i.gem.combobox.get() == 'Unslotted':
                    i.gem.combobox.set("Open")
                    i.gem.rank.set('–')
                i.gem.rank["values"] = GR_df[GR_df["Gem"] == i.gem.combobox.get()]['Rank'].tolist()
                if i.gem.rank.get() == GB_df.at[i.gem.combobox.get(), 'Rank'] or i.gem.rank.get() == '–':
                    i.gem.rank.set(GB_df.at[i.gem.combobox.get(), 'Rank']) # Autosets to max rank
                min_value = int(GR_df.at[(i.gem.combobox.get(),i.gem.rank.get()), 'Min'])
                max_value = int(GR_df.at[(i.gem.combobox.get(),i.gem.rank.get()), 'Max'])
                i.gem.value["values"] = [r for r in range(min_value,max_value+1)]
                if int(i.gem.value.get()) < min_value or int(i.gem.value.get()) >= max_value:
                    i.gem.value.set(GR_df.at[(i.gem.combobox.get(),i.gem.rank.get()), 'Max']) # Autosets to max value
            case _: # works for uniques and no-slots
                i.gem.combobox["values"] = []
                i.gem.combobox.set(gem)
                i.gem.rank["values"] = []
                i.gem.rank.set(rank)
                i.gem.value["values"] = []
                i.gem.value.set(value)
        # The rest of the stats
        i.p_def.config(   text=df.at[i.combobox.get(),  'Phy_Def'])
        i.e_def.config(   text=df.at[i.combobox.get(),  'Eth_Def'])
        i.weight.config(  text=df.at[i.combobox.get(),  'Weight'])

    update_totals(loadout)

def update_totals(loadout):
    for g in range(8): # Reset
        loadout.effects[g].config(text="–")
        loadout.gem_values[g].config(text="–")
    gems_set = {} # Uses a set to call indexes by name
    g = 0  # Current slot index
    for h in loadout.gems:
        gem = h.combobox.get()
        value = h.value.get()
        if gem in ['Unslotted', 'Open'] or not gem: continue  # Skip
        if gem in gems_set:
            idx = gems_set[gem]
            # Add to the existing value
            existing_value = loadout.gem_values[idx].cget("text")
            try:
                total = int(existing_value) + int(value)
                total = min(total,int(GB_df.at[gem, 'Total_Max']))
                loadout.gem_values[idx].config(text=total)
            except ValueError:
                # Handle non-integer values gracefully
                loadout.gem_values[idx].config(text=f"{value}")
        else:
            if g < 8:
                loadout.effects[g].config(text=gem)
                loadout.gem_values[g].config(text=value)
                gems_set[gem] = g
                g += 1
            else:
                print(f"Warning: More than 8 unique gem types. '{gem}' not displayed.")

    # Armour Stats
    p_def = sum([int(c.p_def["text"]) for c in loadout.equips])+int(loadout.weapon.p_def["text"])
    if 'Muscle Up' in gems_set: p_def = p_def + int(loadout.gem_values[gems_set['Muscle Up']]["text"])
    e_def = sum([int(c.e_def["text"]) for c in loadout.equips])+int(loadout.weapon.e_def["text"])
    if 'Ether Def Up' in gems_set: e_def = e_def + int(loadout.gem_values[gems_set['Ether Def Up']]["text"])
    weight = sum([int(c.weight["text"]) for c in loadout.equips])
    loadout.character.p_def.config(text=p_def)
    loadout.character.e_def.config(text=e_def)
    loadout.character.weight.config(text=weight)

    # character Stats
    CS_df = load_sheet(loadout.character.name.get())
    CS_df.set_index('Level', inplace=True)
    level = int(loadout.character.level.get())
    hp = int(CS_df.at[level,'HP'])
    if 'HP Up' in gems_set: hp = int(hp + (int(loadout.gem_values[gems_set['HP Up']]["text"]) * hp / 100))
    strength = int(CS_df.at[level,'Strength'])
    if 'Strength Up' in gems_set: strength = strength + int(loadout.gem_values[gems_set['Strength Up']]["text"])
    ether = int(CS_df.at[level,'Ether'])
    if 'Ether Up' in gems_set: ether = ether + int(loadout.gem_values[gems_set['Ether Up']]["text"])
    agility = int(CS_df.at[level,'Agility']) - weight
    if 'Agility Up' in gems_set: agility = agility + int(loadout.gem_values[gems_set['Agility Up']]["text"])
    loadout.character.hp.config(text=hp)
    loadout.character.strength.config(text=strength)
    loadout.character.ether.config(text=ether)
    loadout.character.agility.config(text=agility)

    # weapon Stats
    aa_max = int(loadout.weapon.dmg_max["text"])+strength
    if 'Attack Plus' in gems_set: aa_min = min(int(aa_max + int(loadout.gem_values[gems_set['Attack Plus']]["text"]) * aa_max / 100), 999)
    aa_min = int(loadout.weapon.dmg_min["text"])+strength
    if 'Attack Stability' in gems_set: aa_min = min(int(aa_min + int(loadout.gem_values[gems_set['Attack Stability']]["text"]) * aa_min / 100), aa_max)
    crit = int(loadout.weapon.crit["text"])
    if 'Critical Up' in gems_set: crit = crit + int(loadout.gem_values[gems_set['Critical Up']]["text"])
    block = int(loadout.weapon.block["text"])
    loadout.character.aa_min.config(text=aa_min)
    loadout.character.aa_max.config(text=aa_max)
    loadout.character.crit.config(text=crit)
    loadout.character.block.config(text=block)