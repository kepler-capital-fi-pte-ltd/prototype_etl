import pandas as pd
import easygui as easy
import os
"""
AKA FILE OPERATIONS
"""

class FileLoading(object):
    """
    Contains the functions that handle very first contact with files. Getting a list of files in the dataset
    to work on and splitting any excel files into individual CSVs.
    """
    
    def __init__(self, gui=True, path=None):
        if gui is False:
            self.path = path
            self.files = [os.path.join(dp, f) for dp, dn, fn in os.walk(path) for f in fn]
        else:
             self.path = easy.diropenbox(msg="Select the directory that contains the files to ETL", title="Select Directory", default=os.getcwd())
             self.files = [os.path.join(dp, f) for dp, dn, fn in os.walk(self.path) for f in fn]
        self.csv_files = [x for x in self.files if x[-3:] == "csv"]

    
    def split_excel_files(self):
        """
        Function to split excel files into indivdual csv's and then delete.
        """
        for x in self.files:
            if x[-4:] not in [".xls", "xlsx"]:
                continue
            else:
                files = pd.read_excel(x, sheet_name=None)
                for k, v in files.items():
                    #get name with the extension stripped
                    name = k.split(".")[0]
                    out_path = x.split(".")[0]
                    try:
                        os.mkdir(out_path)
                    except:
                        print("directory exists")
                    v.to_csv(f"{out_path}/{name}.csv", index=False)
                os.remove(x)
        self.files = [os.path.join(dp, f) for dp, dn, fn in os.walk(self.path) for f in fn]
        self.csv_files = [x for x in self.files if x[-3:] == "csv"]
        
    def create_dates(self, FindHeader, datemaker):
        all_cols = pd.Series()
        #get all of the columns in one list
        for x in self.files:
            try:
                df = pd.read_csv(x, skiprows=FindHeader.chosen_header)
                dates = []
                for index, row in df.iterrows():
                    try:
                        dates.append(eval(datemaker))
                    except:
                        dates.append(None)
                df["deciml_date"]=dates
                df.to_csv(x, index=False)
            except Exception as e:
                print(e)
        return
                    