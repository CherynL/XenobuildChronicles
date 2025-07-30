import pandas as pd
from app.constants import (
    XENOBUILD_DATA,
    GEMS_UNLINKED, GEMS_BY_RANK, GEMS_BESTEST,
    WEAPONS_UNLINKED,
    SKILLS_FULL, LINKS_BY_CHARACTER
)



# A helper function to load other sheets (character stats, armor, etc.)
def load_sheet(sheet_name: str):
    df = pd.read_excel(XENOBUILD_DATA, sheet_name=sheet_name)
    return df

# Load base Excel sheets
GU_df = load_sheet(GEMS_UNLINKED)
GU_df.set_index('Gem', inplace=True)

GR_df = load_sheet(GEMS_BY_RANK)
GR_df.set_index(['Gem', 'Rank'], inplace=True, drop=False)

GB_df = load_sheet(GEMS_BESTEST)
GB_df.set_index('Gem', inplace=True)

WU_df = load_sheet(WEAPONS_UNLINKED)
WU_df.set_index('Name', inplace=True)

# Future features

SF_df = load_sheet(SKILLS_FULL)
SF_df.set_index(['Skill','Character'], inplace=True, drop=False)

LC_df = load_sheet(LINKS_BY_CHARACTER)
LC_df.set_index('Link_Slot', inplace = True)