import cantools
import can
import pandas as pd
import os
from typing import Union, List, Optional
from collections import defaultdict

StringPathLike = Union[str, os.PathLike]

def load_dbc_files(dbc_input: Union[StringPathLike, List[StringPathLike]]) -> List[cantools.database.Database]:
    dbcs = []
    if isinstance(dbc_input, str):
        if os.path.isdir(dbc_input):
            for file in os.listdir(dbc_input):
                if file.endswith('.dbc'):
                    dbc_path = os.path.join(dbc_input, file)
                    dbcs.append((dbc_path, cantools.db.load_file(dbc_path)))
        else:
            dbcs.append((dbc_input, cantools.db.load_file(dbc_input)))
    elif isinstance(dbc_input, list):
        for dbc_path in dbc_input:
            dbcs.append((dbc_path, cantools.db.load_file(dbc_path)))
    return dbcs

def load_can_files(can_input: Union[StringPathLike, List[StringPathLike]]) -> List[str]:
    can_files = []
    if isinstance(can_input, str):
        if os.path.isdir(can_input):
            for file in os.listdir(can_input):
                if file.lower().endswith(('.blf', '.asc')):
                    can_path = os.path.join(can_input, file)
                    can_files.append(can_path)
        else:
            can_files.append(can_input)
    elif isinstance(can_input, list):
        for can_path in can_input:
            can_files.append(can_path)
    return can_files

def _read_can_files(dbc_input: Union[StringPathLike, List[StringPathLike]],
                    can_input: Union[StringPathLike, List[StringPathLike]],
                    signal_names: Optional[List[str]] = None):
    dbcs = load_dbc_files(dbc_input)
    can_files = load_can_files(can_input)

    for can_file in can_files:
        if can_file.lower().endswith('.blf'):
            log_data = can.BLFReader(can_file)
        elif can_file.lower().endswith('.asc'):
            log_data = can.ASCReader(can_file)
        else:
            continue

        # Dictionary to store decoded data for each DBC file
        all_decoded = {dbc_path: defaultdict(list) for dbc_path, _ in dbcs}

        for msg in log_data:
            for dbc_path, dbc in dbcs:
                try:
                    dec = dbc.decode_message(msg.arbitration_id, msg.data)
                    if dec:
                        for key, data in dec.items():
                            if signal_names is None or key in signal_names:
                                all_decoded[dbc_path][key].append([msg.timestamp, data])
                except:
                    pass

        for dbc_path, decoded in all_decoded.items():
            sigs = []
            for k, v in decoded.items():
                timestamps = [i[0] for i in v]
                data = [i[1] for i in v]
                s = pd.Series(data, index=pd.to_datetime(timestamps, unit='s'), name=k)
                sigs.append(s)

            df = pd.DataFrame(sigs).T

            # Interpolate missing values
            df.interpolate(method='time', inplace=True)

            # Create a unique filename for each combination of DBC and CAN files
            base_name = f"{os.path.splitext(os.path.basename(dbc_path))[0]}_{os.path.splitext(os.path.basename(can_file))[0]}"
            csv_filename = f"{base_name}.csv"
            parquet_filename = f"{base_name}.parquet"
            df.to_csv(csv_filename, encoding='utf-8-sig')
            df.to_parquet(parquet_filename)


if __name__ == '__main__':
        # Example usage:
        dbc_input = ["path/to/dbc1.dbc", "path/to/dbc2.dbc"]
        blf_input = ["path/to/blf1.blf", "path/to/blf2.blf"]
        _read_can_files(dbc_input, blf_input)
