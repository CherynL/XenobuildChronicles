# Chat broke but I can do the rest
from app.data_loader import WU_df, GR_df, GB_df, load_sheet
# ---------------
# Bound Functions
# ---------------

# Updating for equippable armour
def update_items(character,weapon,equips):
    selected_character = character.name.get() # update valid armour
    CS_df = load_sheet(selected_character)
    CS_df.set_index('Level', inplace=True)
    character.level["values"] = CS_df.index.tolist()
    character.level.set("99") #reset
    for g in [weapon.gem0,weapon.gem1,weapon.gem2]:
        g.combobox.set("Unslotted")
        g.rank.set("–")
        g.value.set(0)
    default_weapon = WU_df[WU_df[selected_character]].index.tolist()
    weapon.combobox["values"] = default_weapon
    weapon.combobox.set(default_weapon[0])
    # Making 'Name' the index
    for i in equips:
        df = load_sheet(i.sheet_name)
        df.set_index('Name', inplace=True)
        i.combobox["values"] = df[df[selected_character]].index.tolist()
        i.combobox.set("Not Equipped") #reset
        i.gem.combobox.set("Unslotted") #reset
        i.gem.rank.set("–")
        i.gem.value.set(0)

def update_weapon(weapon, character, p_defs, e_defs, weights): # TODO WORK ON THIS SECTION
    
    for i, g in enumerate([weapon.gem0, weapon.gem1, weapon.gem2]):
        # Gem Slot selection when equipment is 
        gem = WU_df.at[weapon.combobox.get(), f"Gem.{i}"]
        rank = WU_df.at[weapon.combobox.get(), f"Rank.{i}"]
        value = int(WU_df.at[weapon.combobox.get(), f"Value.{i}"]) # For some reason, this one wants to be a float
        match gem:
            case 'Open':
                g.combobox["values"] = GB_df[GB_df['Equipment'].isin(['Weapon', 'All'])].index.tolist()[1:]
                if g.combobox.get() == gem or g.combobox.get() == 'Unslotted': g.combobox.set('Open')
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
    misc_flag = WU_df.at[weapon.combobox.get(), "Misc_Flag"]
    if(misc_flag >= 3): weapon.anti_mechon.config(text="YES")
    else: weapon.anti_mechon.config(text="NO")
    if(misc_flag >= 5): min_mod = int(character.level.get())*1.4; max_mod = int(character.level.get())*1.5
    else: min_mod = max_mod = 1
    if(misc_flag >= 7): weapon.unshackled.config(text='YES')
    else: weapon.unshackled.config(text='NO')

    weapon.dmg_min.config(text=min(int(WU_df.at[weapon.combobox.get(), 'Dmg_Min']*min_mod),999))
    weapon.dmg_max.config(text=min(int(WU_df.at[weapon.combobox.get(), 'Dmg_Max']*max_mod),999))
    weapon.crit.config(text=WU_df.at[weapon.combobox.get(), 'Crit'])
    weapon.p_def.config(text=WU_df.at[weapon.combobox.get(), 'Phy_Def'])
    weapon.e_def.config(text=WU_df.at[weapon.combobox.get(), 'Eth_Def'])
    weapon.block.config(text=WU_df.at[weapon.combobox.get(), 'Block'])

    update_totals(character, weapon, p_defs, e_defs, weights)

# Updating Stats and slots
def update_equips(equips, character, weapon, p_defs, e_defs, weights):
    # I wonder if there's an easier way to bulk-assign values in python
    for i in equips:
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

    update_totals(character, weapon, p_defs, e_defs, weights)

def update_totals(character, weapon, p_defs, e_defs, weights):

    # TODO Gem Stats

    # weapon Stats

    # Armour Stats
    p_def = sum([int(c["text"]) for c in p_defs])+int(weapon.p_def["text"])
    e_def = sum([int(c["text"]) for c in e_defs])+int(weapon.e_def["text"])
    weight = sum([int(c["text"]) for c in weights])
    character.p_def.config(text=p_def)
    character.e_def.config(text=e_def)
    character.weight.config(text=weight)

    # character Stats
    CS_df = load_sheet(character.name.get())
    CS_df.set_index('Level', inplace=True)
    level = int(character.level.get())
    hp = CS_df.at[level,'HP']
    strength = CS_df.at[level,'Strength']
    ether = CS_df.at[level,'Ether']
    agility = CS_df.at[level,'Agility']
    character.hp.config(text=hp)
    character.strength.config(text=strength)
    character.ether.config(text=ether)
    character.agility.config(text=agility)