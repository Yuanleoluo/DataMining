from requests_html import HTMLSession
import pandas as pd
from progress.bar import Bar
import time


s = HTMLSession()
productList = []

def request(url):
  r = s.get(url)
  r.html.render(sleep=1)
  # get the links of all products on this page
  return r.html.xpath('//*[@id="categoryContent"]/section[4]', first=True)


def parse(products):
  bar = Bar('Processing', max=len(products.absolute_links))
  # loop through each products
  for item in products.absolute_links:
    r = s.get(item)
    
    # see if div.info_table exist
    try:
       specs = r.html.find('#RacquetSpecsTable', first=True).text.split("\n")
       price = r.html.find('#pricing', first=True).text.split("#")[0]
       brand = r.html.find('#name', first=True).text.split(" ")[0]
       product = {
          'brand': brand,
       	  'price': price,
          'head_size': specs[1],
          'length': specs[3],
          'weight': specs[5],
          'tension': specs[7],
          'balance': specs[9],
          'beam_width': specs[11],
          'composition': specs[13],
          'flex': specs[15],
          'grip_type': specs[17],
          'power_lv': specs[19],
          'string_pa': specs[21] + specs[22] + specs[23] + specs[24],
          'swing_sp': specs[26],
          'swing_we': specs[28]
      }
       productList.append(product)
    except:
       specs = "none"

    bar.next()
  bar.finish()


def output():
  df = pd.DataFrame(productList)
  df.to_csv('tennisRacquets.csv', index=False)
  print('saved to CSV file.')


x = 1
while x <= 4:
  products = request(f'https://www.tennisexpress.com/tennis-racquets#?Category0=Racquets&search_return=all&page={x}')
  print(f'Getting items from page {x}.')
  parse(products)
  print(" Total items: ", len(productList))
  x = x + 1
  time.sleep(2)

print("no more items")

output()