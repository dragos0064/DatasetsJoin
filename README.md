#CSV Merging and Cleaning Program#

This program is designed to process, merge, and clean data from three input CSV files: website_dataset.csv, facebook_dataset.csv, and google_dataset.csv. It prioritizes data from website_dataset.csv during merging while combining relevant information from the other two files. The final output is a well-structured, cleaned, and formatted CSV file named final_merged_dataset_cleaned.csv.

Features
Input Validation:

The program checks the existence and content of the input files before processing.
Errors or missing files are handled gracefully with appropriate messages.
Data Cleaning:

Standardizes company names, phone numbers, categories, and addresses for consistency.
Removes unwanted characters, double quotes, and special symbols from addresses.
Concatenates city, region, and country for website_dataset.csv to create a unified address format.
Handles missing values by replacing them with default values such as Not Available.
Data Merging:

Merges the three datasets on a normalized column, company_name_clean.
Resolves conflicts by prioritizing data from website_dataset.csv, followed by google_dataset.csv and facebook_dataset.csv.
Formatting:

Formats phone numbers into readable formats, including international numbers.
Capitalizes the first letter of each word in business categories and addresses for better readability.
Renames columns to more descriptive names for the final output.
Output:

Saves the cleaned and merged data to final_merged_dataset_cleaned.csv.
Removes temporary files used during the process to maintain a clean working directory.
Requirements
Python Libraries:
pandas
numpy
os
re
csv
Install the required libraries using:

bash
Copy code
pip install pandas numpy
Input Format
The program expects three CSV files in the same directory:

website_dataset.csv
Columns: site_name, phone, s_category, main_city, main_region, main_country
facebook_dataset.csv
Columns: name, phone, categories, address
google_dataset.csv
Columns: name, phone, category, address
How It Works
File Validation:

Ensures all three input files exist and are non-empty.
Prints a confirmation for each file loaded successfully.
Data Preprocessing:

Creates a company_name_clean column by converting names to lowercase and stripping spaces for consistent merging.
Cleans and formats phone numbers, categories, and addresses.
Merging Datasets:

Merges the datasets using company_name_clean with an outer join to include all entries.
Resolves conflicts in key fields (Phone, Category, Address) by prioritizing website_dataset.csv.
Final Formatting:

Formats phone numbers for readability.
Cleans and standardizes company names and addresses.
Handles missing values by replacing them with Not Available.
Output:

Saves the final cleaned and formatted dataset to final_merged_dataset_cleaned.csv.
Removes double quotes from the output file to ensure clean formatting.
Example Output
The final CSV file will have the following columns:

Company Name: Cleaned and standardized company name.
Business Category: Capitalized category describing the business.
Full Address: Combined and formatted address.
Contact Number: Well-formatted phone numbers.
Sample Output:

mathematica
Copy code
Company Name, Business Category, Full Address, Contact Number
Example Inc, Technology, 123 Example Road, New York, NY, USA, +1 (123) 456-7890
Sample Ltd, Retail, 456 Sample Street, London, UK, +44 (20) 1234-5678
How to Run
Place the three input CSV files (website_dataset.csv, facebook_dataset.csv, google_dataset.csv) in the same directory as the script.
Run the program:
bash
Copy code
python merge_and_clean_datasets.py
Check the output folder for the final cleaned CSV file:
final_merged_dataset_cleaned.csv
Notes
If any input file contains invalid data or missing values, the program handles them gracefully by using default replacements.
Ensure that the output/ directory exists or is writable for saving the final results.
The program prioritizes website_dataset.csv over the other datasets when merging conflicting data.
Known Limitations
The script assumes that all input files follow the expected column structure.
While the program tries to handle various edge cases (e.g., missing values, invalid phone numbers), further customization may be required for non-standard datasets.
License
This project is open-source and available under the MIT License. Contributions are welcome!
