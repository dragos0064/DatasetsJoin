# **CSV Merging and Cleaning Program**

This program is designed to process, merge, and clean data from three input CSV files: `website_dataset.csv`, `facebook_dataset.csv`, and `google_dataset.csv`. It prioritizes data from `website_dataset.csv` during merging while combining relevant information from the other two files. The final output is a well-structured, cleaned, and formatted CSV file named `final_merged_dataset_cleaned.csv`.

---

## **Features**

1. **Input Validation**:
   - The program checks the existence and content of the input files before processing.
   - Errors or missing files are handled gracefully with appropriate messages.

2. **Data Cleaning**:
   - Standardizes company names, phone numbers, categories, and addresses for consistency.
   - Removes unwanted characters, double quotes, and special symbols from addresses.
   - Concatenates city, region, and country for `website_dataset.csv` to create a unified address format.
   - Handles missing values by replacing them with default values such as `Not Available`.

3. **Data Merging**:
   - Merges the three datasets on a normalized column, `company_name_clean`.
   - Resolves conflicts by prioritizing data from `website_dataset.csv`, followed by `google_dataset.csv` and `facebook_dataset.csv`.

4. **Formatting**:
   - Formats phone numbers into readable formats, including international numbers.
   - Capitalizes the first letter of each word in business categories and addresses for better readability.
   - Renames columns to more descriptive names for the final output.

5. **Output**:
   - Saves the cleaned and merged data to `final_merged_dataset_cleaned.csv`.
   - Removes temporary files used during the process to maintain a clean working directory.

---

## **Requirements**

- **Python Libraries**:
  - `pandas`
  - `numpy`
  - `os`
  - `re`
  - `csv`

Install the required libraries using:
```bash
pip install pandas numpy

The script assumes that all input files follow the expected column structure.
While the program tries to handle various edge cases (e.g., missing values, invalid phone numbers), further customization may be required for non-standard datasets.
License
This project is open-source and available under the MIT License. Contributions are welcome!
