"""Compatibility wrapper for the SDESM CSV storage module.

The primary implementation lives in data_storage.py, but this file keeps the existing name usable.
"""

from data_storage import clear_history, load_history, save_record


if __name__ == "__main__":
    print("SDESM Datastorage Compatibility Test")
    clear_history()
    save_record(25, 2.5, 40, "Clear", 10.0, 500.0, 10.0, "SAFE", ["Compatibility check"])
    print(load_history())