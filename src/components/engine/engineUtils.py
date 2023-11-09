import pandas as pd


def deactivate(obj):
    obj.configure(state="disabled")


def activate(obj):
    obj.configure(state="active")


def read_to_df(path):
    return pd.read_excel(path)
