import requests
import pandas as pd
def download_odds():
  # API endpoint for upcoming UFC fights
  url = 'https://api.the-odds-api.com/v4/sports?apiKey=5fc94d760669a4d993e2e5fd1d1e38d2'
  url2 =  "https://api.the-odds-api.com/v4/sports/mma_mixed_martial_arts/odds/?apiKey=5fc94d760669a4d993e2e5fd1d1e38d2&regions=us&markets=h2h,spreads&oddsFormat=decimal"
  # API key
  api_key = '5fc94d760669a4d993e2e5fd1d1e38d2'

  # API parameters
  params = {
      'apiKey': api_key,
      'sport': 'Mixed Martial Arts',
  }

  # Send API request
  response = requests.get(url2)
  result = response.json()

  f1 = []
  f2 = []
  f1_odd = []
  f2_odd = []
  bookie = []
  for res in result:
    for books in res['bookmakers']:
      bookie.append(books['title'])
      f1.append(books['markets'][0]['outcomes'][0]['name'])
      f2.append(books['markets'][0]['outcomes'][1]['name'])
      f1_odd.append(books['markets'][0]['outcomes'][0]['price'])
      f2_odd.append(books['markets'][0]['outcomes'][1]['price'])

  dict_res = {"fighter1": f1, "fighter2": f2, "odds_f1": f1_odd, "odds_f2": f2_odd, "bookmaker": bookie}
  df = pd.DataFrame(dict_res)
  df.to_csv('df_odds.csv',index=False)
  return(df)


def get_odds(fighter1, fighter2, df):
  prijmeni1 = fighter1.split(' ')[-1].lower()[:-1]
  prijmeni2 = fighter2.split(' ')[-1].lower()[:-1]
  if \
  df[(df['fighter1'].str.lower().str.contains(prijmeni1)) & (df['fighter2'].str.lower().str.contains(prijmeni2))].shape[
    0] > 0:
    df = df[(df['fighter1'].str.lower().str.contains(prijmeni1)) & (df['fighter2'].str.lower().str.contains(prijmeni2))]

    f1_min = float(df['odds_f1'].min())
    f1_max = float(df['odds_f1'].max())
    best_bookie_f1 = df.sort_values('odds_f1', ascending=False).iloc[0, 4]

    f2_min = float(df['odds_f2'].min())
    f2_max = float(df['odds_f2'].max())
    best_bookie_f2 = df.sort_values('odds_f2', ascending=False).iloc[0, 4]
    return {"f1_min": f1_min, "f1_max": f1_max, "bookmaker1": best_bookie_f1, "f2_min": f2_min, "f2_max": f2_max,
            "bookmaker2": best_bookie_f2}
  elif \
  df[(df['fighter1'].str.lower().str.contains(prijmeni2)) & (df['fighter2'].str.lower().str.contains(prijmeni1))].shape[
    0] > 0:
    df = df[(df['fighter1'].str.lower().str.contains(prijmeni2)) & (df['fighter2'].str.lower().str.contains(prijmeni1))]
    f1_min = float(df['odds_f1'].min())
    f1_max = float(df['odds_f1'].max())
    best_bookie_f1 = df.sort_values('odds_f1', ascending=False).iloc[0, 4]

    f2_min = float(df['odds_f2'].min())
    f2_max = float(df['odds_f2'].max())
    best_bookie_f2 = df.sort_values('odds_f2', ascending=False).iloc[0, 4]
    return {"f2_min": f1_min, "f2_max": f1_max, "bookmaker2": best_bookie_f1, "f1_min": f2_min, "f1_max": f2_max,
            "bookmaker1": best_bookie_f2}

  else:
    return []
