import pandas as pd
import os
import numpy as np
import re
import csv

#I tried to explain this code as much as possible, to show you the way I thought and created my code to this project

print(os.listdir())
#listing all the files in the current directory

files = ['facebook_dataset.csv', 'google_dataset.csv', 'website_dataset.csv']

for file in files:
    if os.path.exists(file):
        print(f"{file} exists!")
    else:
        print(f"Error: {file} not found!")

    with open(file, 'r') as f:
        content = f.read(100)
        if content:
            print(f"{file} loaded successfully and has content.")
        else:
            print(f"{file} is empty.")

try:

    facebook_dataset = pd.read_csv('facebook_dataset.csv', sep=',', on_bad_lines='skip', header=0, low_memory=False)
    google_dataset = pd.read_csv('google_dataset.csv', sep=',', on_bad_lines='skip', header=0, low_memory=False)
    website_dataset = pd.read_csv('website_dataset.csv', sep=';', on_bad_lines='skip', header=0, low_memory=False)

    print("Files loaded successfully!")
except FileNotFoundError as e:
    print(f"Error: {e}")

print("Facebook dataset columns:", facebook_dataset.columns)
print("Google dataset columns:", google_dataset.columns)
print("Website dataset columns:", website_dataset.columns)

facebook_dataset['company_name_clean'] = facebook_dataset['name'].str.strip().str.lower()
google_dataset['company_name_clean'] = google_dataset['name'].str.strip().str.lower()
website_dataset['company_name_clean'] = website_dataset['site_name'].str.strip().str.lower()
#creates a new column, company_name_clean, which contains the company names converted to lowercase (str.lower()) and stripped of incoming spaces (str.strip()).
#I believe this reasoning is beneficial, because it simplifies the code above and the one below, all named "clean".

#I used astype(str) because I thought of striping leading spaces from phone numbers, categories and addresses, and converting them into strings.
facebook_dataset['Phone_clean'] = facebook_dataset['phone'].astype(str).str.strip()
google_dataset['Phone_clean'] = google_dataset['phone'].astype(str).str.strip()
website_dataset['Phone_clean'] = website_dataset['phone'].astype(str).str.strip()

facebook_dataset['Category_clean'] = facebook_dataset['categories'].astype(str).str.strip()
google_dataset['Category_clean'] = google_dataset['category'].astype(str).str.strip()
website_dataset['Category_clean'] = website_dataset['s_category'].astype(str).str.strip()

facebook_dataset['Address_clean'] = facebook_dataset['address'].astype(str).str.strip()
google_dataset['Address_clean'] = google_dataset['address'].astype(str).str.strip()
website_dataset['Address_clean'] = website_dataset['main_city'].astype(str) + ', ' + website_dataset[
    'main_region'].astype(str) + ', ' + website_dataset['main_country'].astype(str)
#in the Website dataset, I here concatenate the city, region, and country into a single address string.


#r'\D+' matches any non-numeric characters, which are then removed
facebook_dataset['Phone_clean'] = facebook_dataset['Phone_clean'].str.replace(r'\D+', '', regex=True)
google_dataset['Phone_clean'] = google_dataset['Phone_clean'].str.replace(r'\D+', '', regex=True)
website_dataset['Phone_clean'] = website_dataset['Phone_clean'].str.replace(r'\D+', '', regex=True)

print("Cleaned Facebook phone, category, and address:")
print(facebook_dataset[['Phone_clean', 'Category_clean', 'Address_clean']].head())
#here I'm verifying if the phone numbers, categories, and addresses were cleaned correctly, for facebook_dataset

print("Cleaned Google phone, category, and address:")
print(google_dataset[['Phone_clean', 'Category_clean', 'Address_clean']].head())
#here I'm verifying if the phone numbers, categories, and addresses were cleaned correctly, for google_dataset

print("Cleaned Website phone, category, and address:")
print(website_dataset[['Phone_clean', 'Category_clean', 'Address_clean']].head())
#here I'm verifying if the phone numbers, categories, and addresses were cleaned correctly, for website_dataset

#here I'm checking if there are any missing values, using isnull().any(axis=1). If there are any found values, they are printed for review.
print("\nMissing values in Facebook dataset (Phone, Category, Address):")
print(facebook_dataset[facebook_dataset[['Phone_clean', 'Category_clean', 'Address_clean']].isnull().any(axis=1)])

print("\nMissing values in Google dataset (Phone, Category, Address):")
print(google_dataset[google_dataset[['Phone_clean', 'Category_clean', 'Address_clean']].isnull().any(axis=1)])

print("\nMissing values in Website dataset (Phone, Category, Address):")
print(website_dataset[website_dataset[['Phone_clean', 'Category_clean', 'Address_clean']].isnull().any(axis=1)])

#Merging Google and Facebook datasets onto the company_name_clean, using an outer join ( how="outer" ), which makes sure that all companies from bothdatasets are included.
merged_data = pd.merge(facebook_dataset, google_dataset, on="company_name_clean", how="outer",
                       suffixes=('_facebook', '_google'))
#After the code above, I merge the result with the website_dataset, using the same method
merged_data = pd.merge(merged_data, website_dataset, on="company_name_clean", how="outer", suffixes=('', '_website'))


#Here, we are resolving conflicts by prioritizing website data, then google, then facebook for key fields
def resolve_conflict(row, column_base):
    website_col = f'{column_base}_website'
    google_col = f'{column_base}_google'
    facebook_col = f'{column_base}_facebook'

    if website_col in row and not pd.isnull(row[website_col]):
        return row[website_col]
    elif google_col in row and not pd.isnull(row[google_col]):
        return row[google_col]
    elif facebook_col in row and not pd.isnull(row[facebook_col]):
        return row[facebook_col]
    else:
        return None


#applying the resolve_conflict function to key fields: Phone, Category, Address
#apply() checks the website, google, and facebook columns for the cleaned data
#lambda here resolves data conflicts for the columns Category, Address, Phone
merged_data['Category'] = merged_data.apply(lambda row: resolve_conflict(row, 'Category_clean'), axis=1)
merged_data['Address'] = merged_data.apply(lambda row: resolve_conflict(row, 'Address_clean'), axis=1)
merged_data['Phone'] = merged_data.apply(lambda row: resolve_conflict(row, 'Phone_clean'), axis=1)

#drop any unnecessary columns after resolve_conflict if required
final_columns = ['company_name_clean', 'Category', 'Address', 'Phone']
final_data = merged_data[final_columns]

#saving the final merged dataset
final_data.to_csv('final_merged_dataset.csv', index=False)
#index=False means we are saving the csv file without row numbers

final_data = pd.read_csv('final_merged_dataset.csv', low_memory=False)


#function to format phone numbers
def format_phone_number(number):
    number = str(number).strip()
    if number == '' or number.lower() in ['nan', 'none', 'not available']:
        return 'Unknown Number'

    number = re.sub(r'\D', '', number)

    if number == '':
        return 'Unknown Number'
    if pd.isna(number) or number.strip() == "" or number == 'Unknown Number':
        return 'Unknown Number'
    #US
    if len(number) == 10:
        return f"( {number[:3]}) {number[3:6]}-{number[6:]}"
    #international
    elif len(number) > 10:
        country_code = number[:-10]
        return f" +{country_code} ({number[-10:-7]}) {number[-7:-4]}-{number[-4:]}"
    else:
        return number


#applying the format function
final_data['Phone'] = final_data['Phone'].astype(str).apply(format_phone_number)

#capitalizing the first letter of each word in Category and Address
final_data['Category'] = final_data['Category'].str.title().str.strip()
final_data['Address'] = final_data['Address'].str.title().str.strip()

#now, we are entering the formatting phase
#renaming columns to be more clear and easily readable
final_data.rename(columns={
    'company_name_clean': 'Company Name',
    'Category': 'Business Category',
    'Address': 'Full Address',
    'Phone': 'Contact Number'
}, inplace=True)


#this function cleans up company names by removing leading digits,handling special cases for # symbols,
#removing unwanted symbols like punctuation, converting the cleaned name to title case and handling empty or invalid names by returning 'Unknown Company'.
def clean_company_name(name):
    if isinstance(name, str):
        #here I removed the leading digits
        name = re.sub(r'^\d+', '', name)
        #in the space of 2 units
        if re.search(r'^#\s{0,2}\d', name):
            #keep only valid characters
            name = re.sub(r'[^a-zA-Z0-9\s\(\)#]', '', name)
        else:
            #remove # if not followed by a number
            name = re.sub(r'^#\s*', '', name)
        #remove unwanted symbols
        name = re.sub(r'[\'\"/@$%^&*_+=<>?,;:{}[\]\\|~`.-]', '', name)
        name = name.strip()
        if name == "" or re.fullmatch(r'\(*\)*', name):
            name = "Unknown Company"
            #empty names

        if name == "()" or name == "" or name == "()":
            name = "Unknown Company"
            #empty names
        name = name.strip().title()
        if not name:
            name = "Unknown Company"
            #empty names
        return name
    return "Unknown Company"


#applying the clean_company_name() function to the Company Name column to model the company names.
final_data['Company Name'] = final_data['Company Name'].apply(clean_company_name)


#in this function, I tried desperately to eliminate the double quotes:(.
#in the end, I managed to do it, but more into the code, not in this function.
#this function removes double and curly quotes(tries), special chars, replaces multiple commas with a single comma, and capitalizes the first letter of each word
def clean_address(address):
    if isinstance(address, str):
        address = re.sub(r'["“”]', '', address)
        address = re.sub(r'[!@#$%^&*()_+=<>?;:{}[\]\\|~`]', '', address)
        address = re.sub(r',+', ',', address)
        address = address.strip(', ')
        address = address.title()
        address = address.replace(' St.', ' Street')
        address = address.replace(' Rd.', ' Road')
        address = address.replace(' Ave.', ' Avenue')
        address = address.replace(' Blvd.', ' Boulevard')

    return address


#applying the clean_address() function to the Full Address column.
final_data['Full Address'] = final_data['Full Address'].apply(clean_address)

#if given NaN values in the given CSVs, the code replaces them with 'Not Available'
final_data['Business Category'] = final_data['Business Category'].replace(np.nan, 'Not Available')
final_data['Full Address'] = final_data['Full Address'].replace(np.nan, 'Not Available')
final_data['Contact Number'] = final_data['Contact Number'].replace(np.nan, 'Not Available')

#makes the business category in title chars
final_data['Business Category'] = final_data['Business Category'].str.title()

#astype(str) converts the 'Contact Number' column to a string data type
#replaces the .0 with an empty string, in favour of formatting the phone numbers
final_data['Contact Number'] = final_data['Contact Number'].astype(str).str.replace('.0', '', regex=False)

#replaces string nan with Not Available
#if NaN is converted to a string, it can be shown as nan
final_data['Contact Number'] = final_data['Contact Number'].replace('nan', 'Not Available')

final_data['Full Address'] = final_data['Full Address'].str.title()
final_data['Full Address'] = final_data['Full Address'].apply(clean_address)

#saved the cleaned and formatted data to a new CSV file; here, I tried to eliminate the quotes, but it didn't work
final_data.to_csv('final_merged_dataset_cleaned.csv', index=False, quoting=csv.QUOTE_MINIMAL)

#here, I tried to remove the double quotes,like in the clean_addresses function, but there it didn't work. I don't know why, I tried many possible variants.
#fortunately, by opening the file, I managed to delete the double quotes from the addresses column, by replacing them with an empty space.
#I hope this method is still ok for formatting the CSV output file.
with open('final_merged_dataset_cleaned.csv', 'r') as file:
    file_data = file.read()

file_data = file_data.replace('"', '')

with open('final_merged_dataset_cleaned.csv', 'w') as file:
    file.write(file_data)

#this just deletes the file used previously
if os.path.exists('final_merged_dataset.csv'):
    os.remove('final_merged_dataset.csv')
    print("'final_merged_dataset.csv' has been deleted.")
else:
    print("The file 'final_merged_dataset.csv' does not exist.")

print("The cleaned and easily readable dataset has been saved as 'final_merged_dataset_cleaned.csv'.")
