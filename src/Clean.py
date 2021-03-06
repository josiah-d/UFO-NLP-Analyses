from bs4 import BeautifulSoup as BS
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re


class CleanUFOs:
    def __init__(self, file_path):
        self.file_path = file_path
        self.rows = []
        self.load_data()
        self.clean_reports()
        
    def load_data(self):
        self.reports = []
        with open(self.file_path) as f:
            for idx,i in enumerate(f):
                # if idx < 98:
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
            duration = self.adjust_duration(duration)

            description = text_lst[-1].split('">')[3].split('</font>')[0].replace('<br/>', '').strip()

            data_dct = {'occured': occured, 'reported': reported, 'city': city, 'state': state,
                        'shape': shape, 'duration': duration, 'description': description}

            self.rows.append(data_dct)
        except:
            pass
    
    def adjust_duration(self, duration):
        e = re.search('[0-9]+',duration)
        num = -1
        multiplier = 1
        if e is not None:
            num = e[0]
        if re.search('min',duration):
            multiplier = 60
        if re.search('h',duration):
            multiplier = 3600

        return int(num)*multiplier

    def clean_reports(self):
        for i, report in enumerate(self.reports):
            # print(i)
            self.parse_html(report)
    
    def to_pandas(self):
        df = pd.DataFrame(self.rows)
        df['occured'] = pd.to_datetime(df['occured'],errors = 'coerce')
        df['reported'] = pd.to_datetime(df['reported'],errors = 'coerce')

        return df