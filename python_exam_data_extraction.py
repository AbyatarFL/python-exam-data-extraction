import os
import sys
import re
import csv
import json
import openpyxl
from datetime import datetime

#1. Extract Address Components
def extract_address_components(text):
    # Cari 'Location:'
    match = re.search(r"Location:\s*(.+)", text)
    if not match:
        return {}

    # Ambil group 1 seteleh 'Location:'
    location_line = match.group(1).strip()

    # Pecah berdasarkan koma
    parts = [p.strip() for p in location_line.split(",")]

    # masukkan bagian-bagian ke variabel
    street_part = parts[0] if len(parts) > 0 else ""
    city = parts[1] if len(parts) > 1 else ""
    state_zip = parts[2] if len(parts) > 2 else ""
    country = parts[3] if len(parts) > 3 else ""

    # Exteact nomor dan nama jalan
    # Pattern: number + space + street name
    street_match = re.match(r"(\d+)\s+(.*)", street_part)
    if street_match:
        street_number = street_match.group(1)
        street_name = street_match.group(2)
    else:
        street_number = ""
        street_name = street_part

    # Extract State dan kode pos
    # Pattern: two uppercase letters + optional spaces + numbers
    sz_match = re.match(r"([A-Z]{2})\s*(\d+)", state_zip)
    if sz_match:
        state = sz_match.group(1)
        zip_code = sz_match.group(2)
    else:
        state = ""
        zip_code = ""

    # 5. Bentuk struktur data
    return {
        "street_number": street_number,
        "street_name": street_name,
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "country": country
    }

#2. Parse Property Details
def extract_property_details(text):
    # Property ID
    prop_match = re.search(r"ID:\s*([A-Z0-9\-]+)", text)
    if prop_match:
        property_id = prop_match.group(1)
    else:
        property_id = ""

    # Contact
    contact_match = re.search(r"Contact:\s*(.+?)\((.+?)\)\s*\|\s*(\S+@\S+)", text)
    contact_name = ""
    contact_type = ""
    contact_email = ""
    if contact_match:
        contact_name = contact_match.group(1).strip()
        contact_type = contact_match.group(2).strip()
        contact_email = contact_match.group(3).strip()

    # Year Built
    year_match = re.search(r"Built\s+(\d{4})", text)
    if year_match:
        year_built = year_match.group(1)
    else:
        year_built = ""

    # Square Footage
    sqft_match = re.search(r"Sq Ft:\s*([\d,]+)", text)
    if sqft_match:
        square_footage = sqft_match.group(1).replace(",", "")
    else:
        square_footage = ""

    # Lot Size
    lot_match = re.search(r"Lot:\s*([\d\.]+\s*\w+)", text)
    if lot_match:
        lot_size = lot_match.group(1)
    else:
        lot_size = ""

    # Address, pakai fungsi sebelumnya
    address_data = extract_address_components(text)

    # Tanggal ekstraksi
    date_extracted = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # Final dictionary
    result = {
        "property_id": property_id,
        "contact_name": contact_name,
        "contact_type": contact_type,
        "Contact_email": contact_email,
        "year_built": year_built,
        "square_footage": square_footage,
        "lot_size": lot_size,
        "date_extracted": date_extracted
    }

    # Merge address data
    result.update(address_data)

    return result

import os

def ensure_output_folder():
    """Buat folder output di lokasi yang sama dengan main script"""
    base_dir = os.path.dirname(os.path.abspath(__file__))  # folder di mana file .py ini berada
    folder_name = os.path.join(base_dir, "Output_Files")

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    return folder_name

def save_to_csv(data, filename):
    """Save dalam bentuk CSV"""
    folder = ensure_output_folder()
    full_path = os.path.join(folder, filename)

    with open(full_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)

def save_to_json(data, filename):
    """Save dalam bentuk JSON"""
    folder = ensure_output_folder()
    full_path = os.path.join(folder, filename)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def save_to_xlsx(data, filename):
    """Save dalam bentuk XLSX"""
    folder = ensure_output_folder()
    full_path = os.path.join(folder, filename)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(list(data.keys()))
    ws.append(list(data.values()))
    wb.save(full_path)

def main():
    # Sample data
    sample_text = """
    PROPERTY DETAILS - ID: PRO-2024-0123 
    Location: 742 Evergreen Terrace, Springfield, ST 12345, United States 
    Contact: Jane Doe (Primary) | john.doe@email.com 
    Additional Details: Built 1983 | Sq Ft: 2,400 | Lot: 0.25 acres 
    Last Updated: March 15, 2024 by Agent#A552 
    """
    # 1. Extract data
    data = extract_property_details(sample_text)

    # 2. print hasil
    print(data)

    # 3. Save ke berbagai format
    save_to_csv(data, "property_details.csv")
    save_to_json(data, "property_details.json")
    save_to_xlsx(data, "property_details.xlsx")

    print("\nFiles saved in Output_Files folder.")

# Jalankan program
if __name__ == "__main__":
    main()