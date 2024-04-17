## Anime Scraper and Database Exporter

This Python script scrapes anime titles and their links from the website [animesuge.to](https://animesuge.to/movie), stores them in a PostgreSQL database, and exports the data to a CSV file named `anime.csv`.

### Detailed Steps
**Requirement**
To run the provided Python script successfully, you need to ensure you have the necessary libraries installed. Here are the requirements:

1. **psycopg2**: This library is required for connecting to PostgreSQL databases from Python.

   You can install it using pip:
   ```
   pip install psycopg2
   ```

2. **requests**: This library is used for sending HTTP requests and retrieving data from websites.

   You can install it using pip:
   ```
   pip install requests
   ```

3. **Beautiful Soup**: This library is utilized for parsing HTML and XML documents, particularly for web scraping tasks.

   You can install it using pip:
   ```
   pip install beautifulsoup4
   ```

Make sure you install these dependencies before running the script to avoid any import errors. Once installed, you should be able to execute the provided Python script without any issues.

#### 1. Database Connection

The script establishes a connection to a PostgreSQL database. It specifies the database name as "postgres" with the username "postgres" and password "1234". The host is set to "localhost" and the port to "5432".

```python
import psycopg2

con = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="Enter Preferred password",
    host="localhost",
    port="5432"
)
```

#### 2. Web Scraping

Using the `requests` library, the script sends a GET request to the URL "https://animesuge.to/movie" to retrieve the HTML content of the webpage. Then, it utilizes `BeautifulSoup` to parse the HTML content and extract the desired data. Specifically, it searches for `<div>` elements with the class name "item" which contain the anime titles and links.

```python
import requests
from bs4 import BeautifulSoup

url = "https://animesuge.to/movie"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
main_div = soup.find_all('div', class_='item')
```

#### 3. Data Handling

The script iterates over each `<div>` element found in the webpage's content. Within each `<div>`, it searches for `<a>` elements which contain the anime titles and links. It then cleans up the data by stripping unnecessary whitespace and removing commas from the titles. Finally, it inserts the cleaned data into the PostgreSQL database table named "anime".

```python
for div in main_div:
    anchor = div.find_all('a')
    for a in anchor:
        name = a.text.strip().replace(',',"")
        link = div.a['href'].strip().replace(',',"")
        cur.execute("INSERT INTO anime (name, link) VALUES (%s, %s)", (name, link))
```

#### 4. CSV Export

After inserting the data into the database, the script retrieves all the records from the "anime" table. It then opens a CSV file named "anime.csv" in write mode and uses the `csv.writer` to write the data into the CSV file. The first row of the CSV file contains the column names retrieved from the database table.

```python
import csv

cur.execute("Select * From anime")
p = cur.fetchall()

with open("anime.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([desc[0] for desc in cur.description])
    writer.writerows(p)
```

#### 5. Closing Connections

Finally, the script closes the cursor and the database connection to release the resources.

```python
cur.close()
con.close()
```

### How to Use

1. **Setup PostgreSQL**: Ensure PostgreSQL is installed and running on localhost with the specified credentials.
2. **Install Dependencies**: Install the required Python libraries: `psycopg2`, `requests`, `BeautifulSoup`.
   ```bash
   pip install psycopg2 requests beautifulsoup4
   ```
3. **Run the Script**: Execute the Python script.
   ```bash
   python anime_scraper.py
   ```

### Notes

- Ensure internet connectivity to scrape data from the website.
- Customize the database connection details if required.
- The exported CSV file (`anime.csv`) will contain two columns: "name" and "link" representing the anime title and its corresponding link.

### Author

This script was authored by Deep Prakash Srivastava. Feel free to reach out for any questions or improvements.


### License

This project is licensed under the [MIT License](LICENSE). Copyright © 2024 Deep Prakash Srivasytava.
