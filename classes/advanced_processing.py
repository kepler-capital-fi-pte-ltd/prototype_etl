from string import Template
import pandas as pd
from dateparser import parse

"""
AKA EXTRACT INDICATORS
"""

class Indicator(object):
    
    def __init__(self, file, value_col, name=None,   uom=None, geoscope=None, source=None, date_col="deciml_date"):
        self.name = name
        self.value_col = value_col
        self.file = file
        self.values = []
        self.uom = uom
        self.geoscope = geoscope
        self.source = source
        self.date_col = "deciml_date"
        self.search_key = ""
        #this is the name of the date column
        return
            
    def orm(self):
        out = {"name" : self.name, "file": self.file, "values" : self.values, 
               "uom" : self.uom, "geoscope" : self.geoscope, "source" : self.source, "search_key" : self.search_key}
        return out
    
    def create_attribute(self, indicator : str, constructor : str):
        """
        Makes a search key, key constructor should be a string template with placeholders for appropriate name.
        elements. Placeholders may reference the $name, $col, $file, $values, $uom, $geoscope, $source or free text.
        Example permitted constructor is "{file} - {geoscope} - {col}")
        """
        file = self.file
        value_col = self.value_col
        uom = self.uom
        geoscope = self.geoscope
        source = self.source
        search_key = self.search_key
        #eugh, was in a rush
        exec(f"self.{indicator} = f'{constructor}'")
    
    def create_values(self, FindHeader=None):
        if FindHeader is not None:
            df = pd.read_csv(self.file, skiprows=FindHeader.chosen_header)
        else:
            df = pd.read_csv(self.file)
        print(self.value_col, self.date_col)
        cols = [self.date_col, self.value_col]
        self.values = df[cols].rename(columns={self.value_col:"value"})
        
            
