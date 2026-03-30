import pandas as pd
import os
import re


def extract_date_from_filename(filename):
    patterns = [
        r'\d{4}-\d{2}-\d{2}',
        r'\d{2}-\d{2}-[A-Za-z]{3}-\d{4}',
        r'\d{8}'
    ]

    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            return match.group(0)

    return None


def detect_source(filename):
    filename = filename.lower()

    if 'blinkit' in filename:
        return 'blinkit'
    elif 'nykaa' in filename:
        return 'nykaa'
    elif 'myntra' in filename:
        return 'myntra'
    elif 'zepto' in filename:
        return 'zepto'
    else:
        return 'unknown'


def standardize_columns(df):
    df.columns = df.columns.str.lower().str.strip()

    mapping = {
        # Blinkit
        'item_id': 'sku',
        'qty_sold': 'units',
        'mrp': 'price',

        # Zepto
        'sku number': 'sku',
        'sales (qty) - units': 'units',
        'gross merchandise value': 'revenue',
        'date': 'date',

        # Nykaa
        'sku code': 'sku',
        'total qty': 'units',
        'selling price': 'price',

        # Myntra
        'order_created_date': 'date',
        'style_id': 'sku',
        'sales': 'units',
        'mrp_revenue': 'revenue',

        # Generic fallback
        'product_id': 'sku',
        'sku_id': 'sku',
        'id': 'sku',
        'quantity': 'units',
        'qty': 'units',
        'count': 'units',
        'units_sold': 'units',
        'amount': 'revenue',
        'total_price': 'revenue',
        'gmv': 'revenue'
    }

    df = df.rename(columns=mapping)

    # Remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    return df


def load_file(path):
    df = pd.read_csv(path)

    filename = os.path.basename(path)
    source = detect_source(filename)

    df = standardize_columns(df)

    # Extract date if missing
    if 'date' not in df.columns:
        df['date'] = extract_date_from_filename(filename)

    # Revenue calculation
    if source in ['blinkit', 'nykaa']:
        if 'units' in df.columns and 'price' in df.columns:
            df['units'] = pd.to_numeric(df['units'], errors='coerce')
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df['revenue'] = df['units'] * df['price']

    # Ensure numeric
    if 'units' in df.columns:
        df['units'] = pd.to_numeric(df['units'], errors='coerce')

    if 'revenue' in df.columns:
        df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')

    df['data_source'] = source

    return df[['date', 'sku', 'units', 'revenue', 'data_source']]