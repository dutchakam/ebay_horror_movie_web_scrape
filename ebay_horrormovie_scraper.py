import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

display_width = 320
pd.set_option('display.width', display_width)
pd.set_option('display.max_columns', 6)

final_df = pd.DataFrame(columns=['Title', 'Quality', 'Type', 'Price', 'Shipping', 'Returns'])

for page in range(1, 21):

    print(final_df)
    print(page)

    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw=movies&_sacat=0&Genre=Horror&_dcat=617&rt=nc&LH_BIN=1&_pgn={page}'

    headers = {'user-agent': 'Chrome/91.0.4469.4'}
    html_req = requests.get(url, headers=headers)

    time.sleep(5)

    soup = BeautifulSoup(html_req.text, 'html.parser')

    titles = soup.findAll('h3', {'class': 's-item__title'})
    title_lst = []
    for title in titles:
        title_lst.append(title.text)

    qualities = soup.findAll('div', {'class': 's-item__subtitle'})
    q_lst = []
    t_lst = []
    for quality in qualities:
        txt = quality.text.split('·')[0].strip()
        if txt in ['Pre-Owned', 'Brand New', 'New (Other)']:
            q_lst.append(txt)
            try:
                txt2 = quality.text.split('·')[1].strip()
                t_lst.append(txt2)
            except IndexError:
                t_lst.append('Unknown')

    prices = soup.findAll('span', {'class': 's-item__price'})
    price_lst = []
    for price in prices:
        price_lst.append(price.text)

    ship_ret = soup.findAll('div', {'class': 's-item__details clearfix'})
    shipping_lst = []
    for item in ship_ret:
        if 'free shipping' in item.text.lower():
            shipping_lst.append('Free')
        else:
            shipping_lst.append('Unknown')

    returns_lst = []
    for item in ship_ret:
        if 'free returns' in item.text.lower():
            returns_lst.append('Free')
        else:
            returns_lst.append('Unknown')

    try:
        df = pd.DataFrame({'Title': title_lst,
                           'Quality': q_lst,
                           'Type': t_lst,
                           'Price': price_lst,
                           'Shipping': shipping_lst,
                           'Returns': returns_lst})
    except ValueError:
        print(len(title_lst), len(q_lst), len(t_lst), len(price_lst), len(shipping_lst), len(returns_lst))
        print(set(q_lst))
        print(set(t_lst))

    final_df = pd.concat([final_df, df], ignore_index=True, sort=False)

    html_req.close()

    time.sleep(5)

final_df.to_csv('ebay_horror_movies.csv')
