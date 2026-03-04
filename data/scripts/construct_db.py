import sys, os

script_dir = os.path.dirname(os.path.abspath(__file__))

if script_dir not in sys.path:
    sys.path.append(script_dir)

from excel_to_db import excel_to_db 

program = excel_to_db()
program.set_database("tax_data.db")

years = ["2020", "2021", "2022", "2023", "2024", "2025"]
file_handle = "_tax_data.xlsx"
path = "./raw/"

for year in years:
    program.set_table(year)
    program.set_input(path + year + file_handle)
    program.convert_to_db()
    print("Loaded table for " + year)
