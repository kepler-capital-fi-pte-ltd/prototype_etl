import pandas as pd
from dateparser import parse
import easygui as easy

"""
AKA DATA PROFILING WORK AUTOMATION
"""

class FindHeader(object):
    """
    Class to define the optimal inset for the headers.Each of the functions is a
    header ID strategy that can be used. 
    """
    def __init__(self, path : str, specify_header=None):
        self.path = path
        self.file = pd.read_csv(path)
        self.chosen_header = specify_header
        self.header = {}
        return

    def skip_missing(self):
        stripped = pd.read_csv(self.path, skip_blank_lines=True)
        original = len(self.file)
        proposed = len(stripped)
        self.header.update({"skip_missing" : original - proposed})
        return original - proposed
    
    def manual_select(self, skip=None):
        self.header.update({"manual_select" : skip})
        return skip
    
    #TODO change all functions of this type to freeze / lock
    def fix_header(self, method):
        self.chosen_header = self.header[method]
        return self.chosen_header
    
    def show(self, method=all):
        to_show = {}
        for key, value in self.header.items():
            to_show.update({key : pd.read_csv(self.path, skiprows=value).head()})
        return to_show

class GetCols(object):
    """
    Class to select all of the columns we want from a datasource.
    """
    def __init__(self, FileLoading):
        self.files = FileLoading
        return
    
    def get_cols(self):
        files = self.files.csv_files
        cols = pd.Series()
        for i in files:
            tmp = pd.read_csv(i)
            cols = cols.append(pd.Series(list(tmp)))
        self.all_cols = cols.values.tolist()
        self.unique_cols = pd.Series(cols.unique()).values.tolist()
        self.filtered_cols = self.unique_cols
        self.cols_dict = {}
    
    def gui_choose_subset(self):
        """
        Simple gui to allow selection of indicators
        """
        choices = easy.multchoicebox(msg="choose which columns to drop", title="drop cols", choices=self.unique_cols)
        try:
            for choice in choices:
                self.filtered_cols.remove(choice)
        except: 
            print("nothing to drop")
        return
    
    def lock(self):
        """
        Locks in a dictionary with the final column definitions
        """        
        for i in self.files.csv_files:
            tmp = list(pd.read_csv(i))
            tmp = [x for x in tmp if x in self.filtered_cols]
            name = [i for x in tmp]
            tmp_dict = dict(zip(name, tmp))
            self.cols_dict.update(tmp_dict)