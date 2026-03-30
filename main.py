import glob
import os
from ingestion.ingest import load_file
from processing.transform import process_data


def main():
    files = glob.glob('data/*.csv')

    dfs = []
    for file in files:
        dfs.append(load_file(file))

    final_df = process_data(dfs)

    # Create output directory if not exists
    os.makedirs('output', exist_ok=True)

    final_df.to_csv('output/final_sales.csv', index=False)
    print("Final sales file generated at output/final_sales.csv")


if __name__ == "__main__":
    main()