import pandas as pd



class Fighter():
    def __init__(self,name):
        df = pd.read_csv('Preprocessing/df_skills.csv')
        self.name = name
        self.df = df[df['FIGHTER'] == name]
        self.Age =int(self.df['AGE'])
        self.Height= round(float((self.df['HEIGHT_fighter'] * 2.54)) / 100, 2)
        self.Weight= round(float(self.df['WEIGHT_fighter'] * 0.4535), 1)
        self.Reach = round(float((self.df['REACH_fighter'] * 2.54)) / 100, 2)

        self.Wins = int(self.df['Win'])
        self.Win_striking = int(self.df['Win-striking'])
        self.Wins_Decision =int(self.df['Win_Decision'])
        self.Wins_ground =int(self.df['Win-ground'])

        self.Losts = int(self.df['Lost'])
        self.Lost_striking =int(self.df['Lost-striking'])
        self.Lost_Decision =int(self.df['Lost_Decision'])
        self.Lost_ground =int(self.df['Lost-ground'])

fighter1 = Fighter('Conor McGregor')
print(fighter1.Lost_ground)