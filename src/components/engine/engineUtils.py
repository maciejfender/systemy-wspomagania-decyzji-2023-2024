import pandas as pd
import tkinter as tk


def deactivate(obj):
    obj.configure(state="disabled")


def activate(obj):
    obj.configure(state="active")


def normal(obj):
    obj.configure(state="normal")


def suggest_type(column, df) -> tuple:
    column_data = df[column].head(10).values
    # data_type = pd.api.types.infer_dtype(column_data, skipna=True)
    data_type = 'string'
    float_occured = False

    for element in column_data:
        is_f = is_float(element)
        is_i = is_int(element)

        if not is_f and not is_i:
            data_type = 'string'
            break

        if is_i and ',' not in str(element) and '.' not in str(element) and not float_occured:
            data_type = 'int'

        if is_f and not is_i:
            float_occured = True
            data_type = 'float'

    if data_type == 'int':
        return 'int64', tk.IntVar()
    elif data_type == 'float':
        return 'float64', tk.DoubleVar()
    else:
        return 'string', tk.StringVar()


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
        return pd.read_excel(path, header=header)

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


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
