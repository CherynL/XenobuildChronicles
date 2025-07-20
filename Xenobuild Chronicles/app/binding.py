from app.logic import(
    update_items, update_weapon, update_equips
)

def bind_all(character, weapon, equips, p_defs, e_defs, weights):
    # -------
    # BINDING
    # -------

    # Character dropdown triggers update of items and weapon
    character.name.bind(
        "<<ComboboxSelected>>",
        lambda e: (
            update_items(character, weapon, equips),
            update_weapon(weapon, character, p_defs, e_defs, weights)
        )
    )

    # Level dropdown updates weapon and equips
    character.level.bind(
        "<<ComboboxSelected>>",
        lambda e: (
            update_weapon(weapon, character, p_defs, e_defs, weights),
            update_equips(equips, character, weapon, p_defs, e_defs, weights)
        )
    )

    # Equipment slots (main armour pieces)
    for eq in equips:
        eq.combobox.bind(
            "<<ComboboxSelected>>",
            lambda e, eq=eq: update_equips(equips, character, weapon, p_defs, e_defs, weights)
        )
        eq.gem.combobox.bind(
            "<<ComboboxSelected>>",
            lambda e, eq=eq: update_equips(equips, character, weapon, p_defs, e_defs, weights)
        )
        eq.gem.rank.bind(
            "<<ComboboxSelected>>",
            lambda e, eq=eq: update_equips(equips, character, weapon, p_defs, e_defs, weights)
        )
        eq.gem.value.bind(
            "<<ComboboxSelected>>",
            lambda e, eq=eq: update_equips(equips, character, weapon, p_defs, e_defs, weights)
        )

    # Weapon combobox
    weapon.combobox.bind(
        "<<ComboboxSelected>>",
        lambda e: update_weapon(weapon, character, p_defs, e_defs, weights)
    )

    # Weapon gem slots
    for g in [weapon.gem0, weapon.gem1, weapon.gem2]:
        g.combobox.bind(
            "<<ComboboxSelected>>",
            lambda e: update_weapon(weapon, character, p_defs, e_defs, weights)
        )
        g.rank.bind(
            "<<ComboboxSelected>>",
            lambda e: update_weapon(weapon, character, p_defs, e_defs, weights)
        )
        g.value.bind(
            "<<ComboboxSelected>>",
            lambda e: update_weapon(weapon, character, p_defs, e_defs, weights)
        )