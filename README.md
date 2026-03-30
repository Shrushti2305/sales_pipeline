Sales Data Pipeline
Overview

This project implements a data pipeline to ingest, clean, standardize, and aggregate sales data from multiple B2B vendors. Each vendor provides data in different formats with inconsistent schemas, so the pipeline standardizes the data into a unified structure and generates a final daily sales dataset.

The pipeline processes data from multiple sources such as Blinkit, Nykaa, Myntra, and Zepto and produces a consolidated daily sales table.

Technical Approach

The pipeline is designed using a modular structure with separate ingestion and processing layers.

1. Ingestion Layer

The ingestion layer is responsible for:

Reading all CSV files from the data/ directory
Detecting the data source from the filename
Standardizing different column names into a common schema
Extracting date from the dataset or filename when required
Calculating revenue for sources where only price per unit is available

After ingestion, all datasets are converted into the following standardized schema:

date | sku | units | revenue | data_source
2. Processing / Transformation Layer

The processing layer performs:

Combining data from all sources
Cleaning and validating data
Converting date fields to standard datetime format
Handling missing values
Ensuring numeric consistency for units and revenue
Aggregating data at daily SKU level per data source

Aggregation logic used:

total_units = sum(units)
total_revenue = sum(revenue)
3. Output Layer

The final processed dataset is saved to:

output/final_sales.csv

Final output schema:

date
product_identifier (sku)
total_units
total_revenue
data_source
Project Structure
sales_pipeline/
│
├── data/                  # Raw vendor input files
├── ingestion/
│   └── ingest.py          # Ingestion and schema standardization
├── processing/
│   └── transform.py       # Data cleaning and aggregation
├── output/
│   └── final_sales.csv    # Final output file
├── main.py                # Pipeline execution script
├── requirements.txt
└── README.md
How to Run the Pipeline
Install dependencies:
pip install -r requirements.txt
Place all vendor CSV files inside the data/ folder.
Run the pipeline:
python main.py
The final output will be generated at:
output/final_sales.csv
Assumptions
SKU identifiers are unique within each data source.
Revenue is calculated as units × price where only unit price is available.
If revenue is already provided (e.g., Gross Merchandise Value), it is used directly.
Missing values in units and revenue are treated as 0.
Dates are either present in the dataset or extracted from filenames.
All input files belong to known vendors (Blinkit, Nykaa, Myntra, Zepto).
Challenges Encountered
Different vendors provided data with different schemas and column naming conventions.
Some datasets contained revenue values while others only had price per unit.
Date formats varied across datasets and sometimes had to be extracted from filenames.
Duplicate column names appeared after column standardization and had to be handled.
Ensuring a consistent schema across all sources before aggregation.
Summary

This pipeline standardizes heterogeneous vendor data into a unified schema, performs data cleaning and aggregation, and produces a final daily sales dataset. The modular design allows new data sources to be added easily by updating the ingestion mapping without changing the processing logic.