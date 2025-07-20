import pandas as pd
from app.constants import (
    XENOBUILD_DATA,
    GEMS_UNLINKED, GEMS_BY_RANK, GEMS_BESTEST,
    WEAPONS_UNLINKED
)

# Load base Excel sheets
GU_df = pd.read_excel(XENOBUILD_DATA, sheet_name=GEMS_UNLINKED)
GU_df.set_index('Gem', inplace=True)

GR_df = pd.read_excel(XENOBUILD_DATA, sheet_name=GEMS_BY_RANK)
GR_df.set_index(['Gem', 'Rank'], inplace=True, drop=False)

GB_df = pd.read_excel(XENOBUILD_DATA, sheet_name=GEMS_BESTEST)
GB_df.set_index('Gem', inplace=True)

WU_df = pd.read_excel(XENOBUILD_DATA, sheet_name=WEAPONS_UNLINKED)
WU_df.set_index('Name', inplace=True)

# A helper function to load other sheets (character stats, armor, etc.)
def load_sheet(sheet_name: str):
    df = pd.read_excel(XENOBUILD_DATA, sheet_name=sheet_name)
    return df