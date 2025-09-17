# Python Developer Coding Exam: Data Extraction from Unstructured Address Data

## Overview
This Python script extracts property details and address components from unstructured text data. 
It parses fields such as:

- `street_number`
- `street_name`
- `city`
- `state`
- `zip_code`
- `country`
- `property_id`
- `contact_name`
- `contact_type`
- `contact_email`
- `year_built`
- `square_footage`
- `lot_size`
- `date_extracted`

The extracted data is saved in **CSV, JSON, and XLSX** formats.

## Requirements
- Python 3.x
- Libraries: `os`, `csv`, `json`, `openpyxl`, `datetime`, `re`

## Usage
1. Run the script:
   ```bash
   python python_exam_data_extraction.py
2. The script extracts data from a sample text block.
3. Output files are saved in the folder Output_Files:
    - `property_details.csv`
    - `property_details.json`
    - `property_details.xlsx`

## Notes
- Extraction is done using regular expressions for key fields.
- The Output_Files folder is created automatically if it does not exist.
- Address components are merged with property details to form a complete dataset.
- **This code is only works for the sample dataset, may not work for others**
- **The unit test scirpt is on `/tests` directory**