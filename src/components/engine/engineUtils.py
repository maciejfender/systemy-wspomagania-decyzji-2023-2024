import pandas as pd


def deactivate(obj):
    obj.configure(state="disabled")


def activate(obj):
    obj.configure(state="active")


def normal(obj):
    obj.configure(state="normal")


def read_to_df(path: str, header_checked=False, separator_checked=False, separator=',') -> pd.DataFrame:
    header = 0
    sep = ','

    if not header_checked:
        header = None

    if separator_checked:
        sep = separator

    if path.endswith(".xls") or path.endswith(".xlsx"):
        return pd.read_excel(path)

    if path.endswith(".csv") or path.endswith(".tsv"):
        return pd.read_csv(path, sep=sep, header=header)

    if path.endswith(".json"):
        return pd.read_json(path)
