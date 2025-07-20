from app.constants import ARM_EQUIP, FOOT_EQUIP, HEAD_EQUIP, LEG_EQUIP, TORSO_EQUIP
from app.models import Character, Equipment, Weapon
from app.ui import build_ui
from app.binding import bind_all

# v4 features:
#   Reworked file structure
#   Added FULL gem customization
#   Added HP, Strength, Ether, and Agility

# features to add:s
#   skill tree
#   skill links
#   gem stats
#   tooltips to reveal calculations

character = Character()
weapon = Weapon()
equips = [
    Equipment('Head', HEAD_EQUIP),
    Equipment('Torso', TORSO_EQUIP),
    Equipment('Arm', ARM_EQUIP),
    Equipment('Leg', LEG_EQUIP),
    Equipment('Foot', FOOT_EQUIP)
    ]

# all stat sources
p_defs = []
e_defs = []
weights = []

# building and binding
root = build_ui(character, weapon, equips, p_defs, e_defs, weights)
bind_all(character, weapon, equips, p_defs, e_defs, weights)

root.mainloop()