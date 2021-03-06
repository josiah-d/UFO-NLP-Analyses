from bs4 import BeautifulSoup as BS
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class CleanUFOs:
    def __init__(self, file_path):
        self.file_path = file_path
        self.rows = []
        self.load_data()
        
    def load_data(self):
        self.reports = []
        with open(self.file_path) as f:
            for i in f:
                self.reports.append(json.loads(i))
                
    def parse_html(self, report):
        try:
            bs = BS(report['html'], 'html.parser')

            text = str(bs.find('tbody'))
            text_lst = text.split(' : ')
            occured = text_lst[1]
            occured = occured.split('  ')[0].strip()

            body = text_lst[2]
            body_lst = body.split(': ')

            reported = body_lst[1]
            reported = reported.split('<')[0].strip()

            location = body_lst[3]
            location = location.split('<')[0]

            city, state = location.split(', ')

            shape = body_lst[4].split('<')[0].strip()

            body = body_lst[4].split(':')

            duration = body[1]
            duration = duration.split('<')[0]

            description = text_lst[-1].split('">')[3].split('</font>')[0].replace('<br/>', '').strip()

            data_dct = {'occured': occured, 'reported': reported, 'city': city, 'state': state,
                        'shape': shape, 'duration': duration, 'description': description}

            self.rows.append(data_dct)
        except:
            pass
    
    def clean_reports(self):
        for report in self.reports:
            self.parse_html(report)
    
    def to_pandas(self):
        return pd.DataFrame(self.rows)