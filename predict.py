from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from numpy import *
from datetime import date
from keras.models import load_model






def prediction(f1, f2,model):
    df = pd.read_csv('Preprocessing/fight_with_stats_precomp.csv')
    df_fighters = pd.read_csv('Preprocessing/fighter_total_stats.csv')
    df_fighters_details = pd.read_csv('Preprocessing/fighter_details.csv', parse_dates=True)
    df_model = pd.read_csv('model/df_model.csv', parse_dates=True)

    today = date.today()
    df_fighters_details['AGE'] = (pd.to_datetime(today) - pd.to_datetime(df_fighters_details['DOB'])).astype('<m8[Y]')

    def predict(f1, f2):
        f1_df = df_fighters.loc[df_fighters['FIGHTER'] == f1]
        f2_df = df_fighters.loc[df_fighters['FIGHTER'] == f2]
        agediff = df_fighters_details[df_fighters_details['FIGHTER'] == f1]['AGE'].values[0] - \
                  df_fighters_details[df_fighters_details['FIGHTER'] == f2]['AGE'].values[0]
        formy = [f1_df['form_skore_fighter'].values[0], f2_df['form_skore_fighter'].values[0]]
        no_of_fights = [f1_df['Fights'].values[0], f2_df['Fights'].values[0]]
        W_D_NC = f1_df[['Win', 'DRAW', 'No_contest']].values.tolist()[0] + \
                 f2_df[['Win', 'DRAW', 'No_contest']].values.tolist()[0]

        sloupce2 = df_fighters.columns.tolist()[10:]
        stats_f1 = []
        stats_f2 = []
        for sloupec in sloupce2:
            splited = sloupec.split('_')
            if 'CTRL' in splited:
                stats_f1.append((f1_df[sloupec] / f1_df['TotalTime']).values[0])
                stats_f2.append((f2_df[sloupec] / f2_df['TotalTime']).values[0])
            if 'attemps' in splited:
                stats_f1.append((f1_df[sloupec.replace('attemps', 'landed')] / f1_df[sloupec]).values[0])
                stats_f1.append((f1_df[sloupec.replace('attemps', 'landed')] / f1_df['TotalTime']).values[0] * 300)

                stats_f2.append((f2_df[sloupec.replace('attemps', 'landed')] / f2_df[sloupec]).values[0])
                stats_f2.append((f2_df[sloupec.replace('attemps', 'landed')] / f2_df['TotalTime']).values[0] * 300)
        stats_list = stats_f1 + stats_f2
        vstup = np.array([1] + [f1_df.iloc[0][col] - f2_df.iloc[0][col] for col in ['HEIGHT_fighter', 'REACH_fighter']] + [
            agediff] + formy + no_of_fights + W_D_NC + stats_list)
        scaler = MinMaxScaler(feature_range=(0, 1))
        vstup_scaled = scaler.fit_transform(
            df_model.append(pd.DataFrame(vstup.reshape(1, -1), columns=list(df_model)), ignore_index=True))[-200:, 1:]
        where_are_NaNs = isnan(vstup_scaled)
        vstup_scaled[where_are_NaNs] = 0
        new_data = np.reshape(vstup_scaled, (1, 200, vstup_scaled.shape[1]))
        y_pred = model.predict(new_data)
        return y_pred


    f1_proba = float(((1 - predict(f1, f2)) + predict(f2, f1)) / 2)
    return round(f1_proba * 100, 2), round((1 - f1_proba) * 100, 2)


