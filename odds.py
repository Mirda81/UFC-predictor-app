import requests
import pandas as pd
def download_odds():
  # API endpoint for upcoming UFC fights
  url = 'https://api.the-odds-api.com/v4/sports?apiKey=5fc94d760669a4d993e2e5fd1d1e38d2'
  url2 =  "https://api.the-odds-api.com/v4/sports/mma_mixed_martial_arts/odds/?apiKey=5fc94d760669a4d993e2e5fd1d1e38d2&regions=us&markets=h2h,spreads&oddsFormat=decimal&bookmakers=unibet"
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

  f1=[]
  f2=[]
  f1_odd=[]
  f2_odd=[]
  for res in result:
    try:
      fight = res['bookmakers'][0]['markets'][0]['outcomes']
      f1.append(fight[0]['name'])
      f2.append(fight[1]['name'])
      f1_odd.append(fight[0]['price'])
      f2_odd.append(fight[1]['price'])
    except:
      pass

  dict_res={"fighter1":f1,"fighter2":f2, "odds_f1":f1_odd,"odds_f2":f2_odd}
  df = pd.DataFrame(dict_res)
  df.to_csv('df_odds.csv',index=False)
  return(df)

