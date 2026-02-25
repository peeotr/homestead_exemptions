from pprint import pprint
import sqlite3
import pandas as pd

con = sqlite3.connect("./data/tax_data.db")
cur = con.cursor()
output = ""

def run_query(query_path, year):
    with open(query_path, "r") as query:
        cur.execute(query.read().replace("year", year))
    return cur.fetchall()

def count_exemptions(query_path, year):
    output = run_query(query_path, year)
    owner_count = 0
    total_exemptions = 0

    for entry in output:
        owner_count += 1
        total_exemptions += entry[1]

    print(query_path.split("/")[-1])
    print("owner_count: " + str(owner_count), "exemption_count: " + str(total_exemptions))

def tally_all_deductions(query_path, year):
    taxes_dict = tally_deductions_by_distinct(query_path, year)
    return sum(taxes_dict.values())

def tally_deductions_by_distinct(query_path, year):
    property_rates_dict = exchange_query_tax_codes_for_rates(query_path, year)
    updated = {
            k: round(sum(v) / 100 * 6000, 2)
            for k,v in property_rates_dict.items()
            }
    return updated

def exchange_query_tax_codes_for_rates(query_path, year):
    property_dict = get_tax_codes_by_query(query_path, year)
    tax_code_dict = get_tax_code_rates()

    updated = {
            k: [tax_code_dict[entry] for entry in v]
            for k, v in property_dict.items()
            }
    return updated

def get_tax_code_rates():
    df = pd.read_csv("./data/tax_codes.csv", index_col=0)
    rates = df.iloc[:, 0].to_dict()
    return rates

def get_tax_codes_by_query(query_path, year):
    output = run_query(query_path, year)
    tax_codes_by_query = {}
    for entry in output:
        tax_codes_by_query[entry[0]] = clean_row(entry[2])
    return tax_codes_by_query

def clean_row(csv_list):
    row = csv_list.split(",")
    for index, entry in enumerate(row):
        if (len(entry) < 4):
            row[index] = "0" + entry
    return row

by_billing_address = "./queries/by_billing_address"
by_owner_name = "./queries/by_owner_name"

print("2023")

count_exemptions(by_owner_name, "2023")
total = tally_all_deductions(by_owner_name, "2023")
print("Total savings: ", str(round(total, 2)))
print("")
count_exemptions(by_billing_address, "2023")
total = tally_all_deductions(by_billing_address, "2023")
print("Total savings: ", str(total))

print("\n")
print("2024")

count_exemptions(by_owner_name, "2024")
total = tally_all_deductions(by_owner_name, "2024")
print("Total savings: ", str(round(total, 2)))
print("")
count_exemptions(by_billing_address, "2024")
total = tally_all_deductions(by_billing_address, "2024")
print("Total savings: ", str(total))

print("\n")
print("2025")

count_exemptions(by_owner_name, "2025")
total = tally_all_deductions(by_owner_name, "2025")
print("Total savings: ", str(round(total, 2)))
print("")
count_exemptions(by_billing_address, "2025")
total = tally_all_deductions(by_billing_address, "2025")
print("Total savings: ", str(total))

