import json
import requests
from pprint import pprint
import sqlalchemy
from sqlalchemy import create_engine
import json
import pandas as pd
#This is where the database is stored for security
from config import password
 


####--------------------------------------------------------######
####                 SECTION 1                              ######
####--------------------------------------------------------######
# read the data in the file and store in variable
with open('orders.json', 'r') as j:
    orders_data = json.load(j)
    #print(pprint(orders_data))

# Create a function that takes in a date argument and returns the rate for that day
def get_exchange(date):
    # Assign the API url to a variable based on website: 
    # https://exchangeratesapi.io/
    url = f"https://api.exchangeratesapi.io/{date}?symbols=CAD&base=USD"
    # Make request and store response
    response = requests.get(url)
    # Extract the json from the response &return the exchange rate
    return response.json()["rates"]["CAD"]

#Loop through the list of dictionaries and add the currency_rate to each one
#By calling the get_exchange function created earlier
for item in orders_data:
    #use a try & except here in case the API call fails,
    #So it doesn't break the run if we can't get some data.
    try:
        date = item["created_at"].split("T")[0]
        exch_rate = get_exchange(date)
        item["currency_rate"] = exch_rate
        #print(exch_rate)
    except:
        item["currency_rate"] = None

#optional to view result before writing
#print(pprint(orders_data))

#write the data into a new file
with open('output/updated_orders_data.json', 'w') as outfile:
    json.dump(orders_data, outfile)




####--------------------------------------------------------######
####                 SECTION 2                              ######
####--------------------------------------------------------######
#create a datfram frame from the data for easy manipulation
complete_df = pd.DataFrame(orders_data)
#create empty dataframes for customer and items
cust_columns = ["id", "name", "email"]
cust_df = pd.DataFrame(columns = cust_columns)

item_columns = ["id", "product_id", "product_sku", "product_name", "price"]
item_df = pd.DataFrame(columns = item_columns)

#check for duplicates
#print(len(complete_df[complete_df["id"].duplicated()]))

#Expanding the multiple items inside the lists in the line_item coluumn
orders_df = complete_df
orders_df = orders_df.explode('line_items').reset_index(drop=True)
#orders_df.head()

#Extract all the items from customer using a for loop
for index, row in orders_df.iterrows():
    #update the item_df & cust_df, will drop duplicates later
    #to improve code you can do a check before this step
    item_df = item_df.append(row["line_items"], ignore_index=True)
    cust_df = cust_df.append(row["customer"], ignore_index=True)
    #now that we've stored the item data and customer data elsewhere
    #we can now leave just the id's for both columns
    orders_df.at[index, "customer"] = row["customer"]["id"]
    orders_df.at[index,"line_items"] = row["line_items"]["id"]

## Remove duplicates from the items & customer tables
# sorting by first name 
cust_df.sort_values("id", inplace=True) 
item_df.sort_values("id", inplace=True)
# dropping duplicate values 
cust_df.drop_duplicates(keep="first",inplace=True) 
item_df.drop_duplicates(keep="first",inplace=True) 
#reset index
cust_df.reset_index(drop=True, inplace=True)
item_df.reset_index(drop=True, inplace=True)

#rename the columns for readability
orders_df.rename(columns={"customer": "customer_id",
                            "line_items": "item_id"}, inplace=True)

#Establish a connection to postgreSQL
connection_string = f"postgres:{password}@localhost:5432/orders_db"
engine = create_engine(f'postgresql://{connection_string}')

# Confirm tables & connection
print(engine.table_names())

#name refers to database name
#Push data into the database
##### Refer to schema.sql for schema
#if_exist = 'append', bbecause the table was already created in PostGres using PgAdmin
item_df.to_sql(name='item', con=engine, if_exists='append', index=False)
cust_df.to_sql(name='customer', con=engine, if_exists='append', index=False)
orders_df.to_sql(name='orders', con=engine, if_exists='append', index=False)
