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
        sep = sep.replace("\\t", "\t")

    if path.lower().endswith(".txt"):
        return read_txt(path, sep, header)

    if path.lower().endswith(".xls") or path.lower().endswith(".xlsx"):
        return pd.read_excel(path)

    if path.lower().endswith(".csv") or path.lower().endswith(".tsv"):
        return pd.read_csv(path, sep=sep, header=header)

    if path.lower().endswith(".json"):
        return pd.read_json(path)


def read_txt(path: str, sep: str = ',', header: str = None):
    data = []
    header_columns = None

    file = open(path, "r")
    lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]

    if header is not None:
        header_columns = lines.pop(0).split(sep)

    for line in lines:
        record = line.split(sep)

        for i in range(len(record)):
            if record[i].replace(',', '').isdigit():
                record[i] = record[i].replace(",", ".")

            if record[i].startswith('.') and record[i].replace('.', '').isdigit():
                record[i] = '0' + record[i]

        data.append(record)

    if header is not None:
        return pd.DataFrame(data, columns=header_columns)

    return pd.DataFrame(data)
