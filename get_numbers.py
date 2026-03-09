from pprint import pprint
import sqlite3
import pandas as pd

con = sqlite3.connect("./data/tax_data.db")
cur = con.cursor()
output = ""

def run_query(query_path, year):
    with open(query_path, "r") as query:
        cur.execute(query.read().replace("{year}", year))
    return cur.fetchall()

def count_exemptions(query_path, year):
    output = run_query(query_path, year)
    owner_count = 0
    total_exemptions = 0

    for entry in output:
        owner_count += 1
        total_exemptions += entry[1]

    return (owner_count, total_exemptions)

def sum_deductions(query_path, year):
    taxes_dict = tally_deductions_by_distinct(query_path, year)
    return sum(taxes_dict.values())

def get_sorted_savings(query_path, year):
    taxes_dict = tally_deductions_by_distinct(query_path, year)
    sorted_taxes_dict = sorted(taxes_dict.items(), key=lambda x:x[1], reverse=True)
    return(sorted_taxes_dict)

def get_median_savings(query_path, year):
    taxes_dict = tally_deductions_by_distinct(query_path, year)
    deduction_list = list(taxes_dict.values())
    deduction_list.sort()
    return get_median_element(deduction_list)

def get_median_element(sorted_list):
    length = len(sorted_list)
    
    if length % 2 == 0:
        return ((sorted_list[length // 2 - 1] + sorted_list[length // 2]) / 2)
    return sorted_list[length // 2]

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

by_owner_name_old = "./queries/by_owner_name_old"
by_owner_name = "./queries/by_owner_name"

for year in range(2020, 2026):
    query = by_owner_name
    if (year <= 2022):
        query = by_owner_name_old

    year_str = str(year)
    print(year_str)
    owner_count, total_exemptions = count_exemptions(query, year_str)
    print("owner_count: " + str(owner_count), "exemption_count: " + str(total_exemptions))
    print("median savings per person: " + str(get_median_savings(query, year_str)))

    total = sum_deductions(query, year_str)
    print("total savings: ", str(round(total, 2)), "\n")

    print("top 10 savers:")
    pprint(get_sorted_savings(query, year_str)[:10])
    print("")
