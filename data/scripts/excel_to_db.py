
import argparse, sqlite3, pandas as pd

class excel_to_db:
    def set_input(self, excel_filename):
        self.excel_filename = excel_filename

    def set_database(self, db_name):
        self.db_name = db_name

    def set_table(self, table_name):
        self.table_name = table_name

    def save_arguments(self):
        self.args = self.parser.parse_args()
        self.excel_filename = self.args.excel_filename
        self.db_name = self.args.db_name
        self.table_name = self.args.table_name

    def parse_arguments(self):
        self.parser = argparse.ArgumentParser(prog="excel to db", description="Takes in a excel file and converts it to a db file")
        self.parser.add_argument("excel_filename", help="Relative path to the .xlsx or .xls file")
        self.parser.add_argument("db_name", help="Name for the database")
        self.parser.add_argument("table_name", help="Name for the table")

    def convert_to_db(self):
        db_con = sqlite3.connect(self.db_name) 
        df = pd.read_excel(self.excel_filename, dtype=str)
        df.to_sql(self.table_name, db_con, if_exists='replace', index=False)

if __name__ == "__main__":
    program = excel_to_db()
    program.parse_arguments()
    program.save_arguments()
    program.convert_to_db()
