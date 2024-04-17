# Import the csv module for handling CSV files
import csv

# Import the psycopg2 module for interacting with PostgreSQL databases
import psycopg2

# Establish a connection to the PostgreSQL database
con = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

# Import the requests module for sending HTTP requests
import requests

# Create a cursor object to execute SQL commands within the connected database
cur = con.cursor()

# Execute an SQL command to delete all records from the 'anime' table
cur.execute("DELETE FROM anime")

# Import the BeautifulSoup class from the bs4 module for HTML parsing
from bs4 import BeautifulSoup

# Define the URL of the webpage to scrape
url = "https://animesuge.to/movie"

# Send an HTTP GET request to the URL and store the response
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content of the webpage
soup = BeautifulSoup(response.content, "html.parser")

# Find all <div> elements with the class 'item' which contain anime data
main_div = soup.find_all('div', class_='item')

# Iterate over each <div> element containing anime data
for div in main_div:
    # Find all <a> elements (links) within the <div>
    anchor = div.find_all('a')
    # Iterate over each link
    for a in anchor:
        # Extract and clean the anime title
        name = a.text.strip().replace(',', "")
        # Extract and clean the anime link
        link = div.a['href'].strip().replace(',', "")
        # Insert the cleaned data into the 'anime' table
        cur.execute("INSERT INTO anime (name, link) VALUES (%s, %s)", (name, link))

# Commit the changes to the database
con.commit()

# Execute an SQL command to retrieve all records from the 'anime' table
cur.execute("SELECT * FROM anime")

# Fetch all the retrieved records
p = cur.fetchall()

# Export the fetched records to a CSV file named 'anime.csv'
with open("anime.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row with column names obtained from the cursor description
    writer.writerow([desc[0] for desc in cur.description])
    # Write the data rows
    writer.writerows(p)

# Print each fetched record
for x in p:
    print(x)

# Close the cursor and the database connection
cur.close()
con.close()
