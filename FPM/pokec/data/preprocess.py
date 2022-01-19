import pandas as pd


class Preprocess:
    def __init__(self, data):
        self.df = data
        self.out = pd.DataFrame()

    def filter_cols(self):
        # cols = ['AGE', 'GenderMF', 'Height', 'Weight', 'BMI', 'MaritalStatus', 'SmokingStatus', 'DrinkingStatus',
        #         'AgeGroup', 'YearsSinceReg', 'BMIGroup', 'ProfileStatus', 'region']
        cols = ['AgeGroup', 'BMIGroup', 'GenderMF', 'MaritalStatus', 'SmokingStatus', 'DrinkingStatus',
                'ProfileStatus', 'BodyType', 'EyeSight', 'EyeColor']
        self.out = self.df[cols]
        self.out['AgeGroup'] = "Age: " + self.out['AgeGroup']
        self.out['BMIGroup'] = "BMI: " + self.out['BMIGroup'].fillna('Missing')
        self.out['MaritalStatus'] = "Marital Status: " + self.out['MaritalStatus'].fillna('Missing')
        self.out['SmokingStatus'] = "Smoking Status: " + self.out['SmokingStatus'].fillna('Missing')
        self.out['DrinkingStatus'] = "Drinking Status: " + self.out['DrinkingStatus'].fillna('Missing')
        pass

    def run(self):
        self.filter_cols()
