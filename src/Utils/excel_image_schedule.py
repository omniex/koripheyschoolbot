import os

import pandas as pd


async def get_schedule_from_excel():
    df = pd.read_excel('data/schedule.xlsx', index_col=1, skiprows=7)
    print(df)
