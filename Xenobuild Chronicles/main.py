from app.constants import ARM_EQUIP, FOOT_EQUIP, HEAD_EQUIP, LEG_EQUIP, TORSO_EQUIP
from app.models import Character, Weapon, Loadout
from app.ui import build_ui
from app.binding import bind_all

# v4 features:
#   Reworked file structure
#   Added FULL gem customization
#   Added HP, Strength, Ether, and Agility

# v5
#   gem stats will display and influence stats
#   equipment that can be unslotted or slotted will now always display as slotted
#       This information was cross-referenced between Xenoblade Fandom Wiki and the Xeno Series Wiki

# features to add:s
#   skill tree
#   skill links
#   tooltips to reveal calculations

character = Character()
weapon = Weapon()
loadout = Loadout(character, weapon)

names = ['Head', 'Torso', 'Arm', 'Leg', 'Foot']
sheets = HEAD_EQUIP, TORSO_EQUIP, ARM_EQUIP, LEG_EQUIP, FOOT_EQUIP
for eq, n, s in zip(loadout.equips, names, sheets):
    eq.name = n
    eq.sheet_name = s

# building and binding
root = build_ui(loadout)
bind_all(loadout)

root.mainloop()