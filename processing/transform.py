import pandas as pd


def process_data(dfs):
    # Combine all data
    df = pd.concat(dfs, ignore_index=True)

    # Convert date
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Remove invalid dates
    df = df.dropna(subset=['date'])

    # Handle missing values
    df['units'] = df['units'].fillna(0)
    df['revenue'] = df['revenue'].fillna(0)

    # Ensure numeric
    df['units'] = pd.to_numeric(df['units'], errors='coerce').fillna(0)
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce').fillna(0)

    # Aggregate daily sales
    final_df = df.groupby(
        ['date', 'sku', 'data_source'],
        as_index=False
    ).agg(
        total_units=('units', 'sum'),
        total_revenue=('revenue', 'sum')
    )

    # Rename column
    final_df = final_df.rename(columns={
        'sku': 'product_identifier'
    })

    # Sort
    final_df = final_df.sort_values(by=['date', 'product_identifier'])

    return final_df