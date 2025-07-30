from app.logic import(
    update_items, update_weapon, update_equips
)

def bind_all(loadout):
    # -------
    # BINDING
    # -------

    # Character dropdown triggers update of items and weapon
    loadout.character.name.bind(
        "<<ComboboxSelected>>",
        lambda e: (
            update_items(loadout),
            update_weapon(loadout)
        )
    )

    # Level dropdown updates weapon and equips
    loadout.character.level.bind(
        "<<ComboboxSelected>>",
        lambda e: (
            update_weapon(loadout),
            update_equips(loadout)
        )
    )

    # Equipment slots (main armour pieces)
    for eq in loadout.equips:
        eq.combobox.bind(
            "<<ComboboxSelected>>",
            lambda e, eq=eq: update_equips(loadout)
        )
        eq.gem.combobox.bind(
            "<<ComboboxSelected>>",
            lambda e, eq=eq: update_equips(loadout)
        )
        eq.gem.rank.bind(
            "<<ComboboxSelected>>",
            lambda e, eq=eq: update_equips(loadout)
        )
        eq.gem.value.bind(
            "<<ComboboxSelected>>",
            lambda e, eq=eq: update_equips(loadout)
        )

    # Weapon combobox
    loadout.weapon.combobox.bind(
        "<<ComboboxSelected>>",
        lambda e: update_weapon(loadout)
    )

    # Weapon gem slots
    for g in [loadout.weapon.gem0, loadout.weapon.gem1, loadout.weapon.gem2]:
        g.combobox.bind(
            "<<ComboboxSelected>>",
            lambda e: update_weapon(loadout)
        )
        g.rank.bind(
            "<<ComboboxSelected>>",
            lambda e: update_weapon(loadout)
        )
        g.value.bind(
            "<<ComboboxSelected>>",
            lambda e: update_weapon(loadout)
        )