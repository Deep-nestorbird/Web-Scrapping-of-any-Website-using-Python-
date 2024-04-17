import csv
import psycopg2
con=psycopg2.connect(
    database="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

import requests
cur=con.cursor()
cur.execute("DELETE FROM anime")
from bs4 import BeautifulSoup
url = "https://animesuge.to/movie"
response = requests.get(url)
#print(response)
con.set_client_encoding('UTF8')
soup = BeautifulSoup(response.content, "html.parser")
main_div=soup.find_all('div',class_='item')
# print(main_div)
for div in main_div:
    anchor = div.find_all('a')
    for a in anchor:
    #  print(a['href']+" "+a.text)
     name = a.text.strip().replace(',',"")  
    link = div.a['href'].strip().replace(',',"")        
            # Insert the data into the 'anime' table
    cur.execute("INSERT INTO anime (name, link) VALUES (%s, %s)", (name, link))
     
con.commit()
cur.execute("Select * From anime")
p=cur.fetchall()
#csv_file = "anime.csv"

with open("anime.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([desc[0] for desc in cur.description])
    writer.writerows(p)
for x in p:
    print(x)
cur.close()
con.close()
