# Namaste_challenge

## Task 1: Python. Data Manipulation and usage of external APIs

The full script can be found in  the file called [**main_script.py**](main_script.py)

- First task was to read the JSON into python as a list of dictionaries

- Next step was to loop through the list, extract the dates and grap the rates from the API, using the function below. Then added the rates ito the data
```python
# Create a function that takes in a date argument and returns the rate for that day
def get_exchange(date):
    # Assign the API url to a variable based on website: 
    # https://exchangeratesapi.io/
    url = f"https://api.exchangeratesapi.io/{date}?symbols=CAD&base=USD"
    # Make request and store response
    response = requests.get(url)
    # Extract the json from the response &return the exchange rate
    return response.json()["rates"]["CAD"]
```

- Exported the data into JSON, for use later in Tableau


## Task 2: SQL
The full script can be found in  the file called [main_script.py](main_script.py)

The second task was achieved using the *SQLAlchemy library* 

- For this, I first imported the data into pandas
```python
#create a datfram frame from the data for easy manipulation
complete_df = pd.DataFrame(orders_data)
```

- I then exploded the dataframe to extract the data from the line_items column.

- I used this new dataframe to create three tables using the data, one for the **items**, another for **customers**, and one for **orders**
 
 - Then loaded the data into a database already created using the schema (schema.sql file) here: [Schema](schema.sql)
```python
#Establish a connection to postgreSQL
connection_string = f"postgres:{password}@localhost:5432/orders_db"
engine = create_engine(f'postgresql://{connection_string}')


#name refers to database name
#if_exist = 'append', bbecause the table was already created in PostGres using PgAdmin
item_df.to_sql(name='item', con=engine, if_exists='append', index=False)
cust_df.to_sql(name='customer', con=engine, if_exists='append', index=False)
orders_df.to_sql(name='orders', con=engine, if_exists='append', index=False)
```

## Task 3: Reporting
The last step was a very brief dive into the data, there weren't that many data points, so not a lot of insights. 

Data was gotten from the JSON created in part 1 - [updated_orders_data.json](output/updated_orders_data), and read directly into Tableau.

**Link to Tableau solution ->** <https://public.tableau.com/profile/dami.osayomi#!/vizhome/Namaste_challenge/orders_dashboard?publish=yes>


## Things that can be improved
- there is room to draw more visuals from Tableau
- Running checks before adding data to tables in pandas, that way you don't have to drop_duplicates after.
- Connect Tableau to database for consistency

## Key takeaway

- This task really exposed me to some of the exciting work that Namaste does, and shows that the team is forward-looking and up-to-date with current technologies.
- I'm confident that my skills and experience will be put to good use at Namaste!

