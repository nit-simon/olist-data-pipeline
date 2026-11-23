import pandas as pd
import logging
import os
from datetime import datetime

# 1. SETUP PRODUCTION LOGGING FRAMEWORK
# This writes to both a file (for audits) and your console terminal.
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/pipeline_run_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

logging.info("🚀 Data Ingestion Pipeline Framework Initialized Successfully.")

# 2. DEFINE PROJECT DIRECTORIES
RAW_DATA_DIR = "raw_data"
CLEAN_ZONE_DIR = "clean_landing_zone"
QUARANTINE_DIR = "rejected_records"


# Ensure target directories exist before running extraction
os.makedirs(CLEAN_ZONE_DIR, exist_ok=True)
os.makedirs(QUARANTINE_DIR, exist_ok=True)


def ingest_order_items():
    file_path = os.path.join(RAW_DATA_DIR, "olist_order_items_dataset.csv")
    logging.info(f"Starting extraction from: {file_path}")

    # 1. Defensive File Check
    if not os.path.exists(file_path):
        logging.error(f"Source file missing: {file_path}")
        return

    df = pd.read_csv(file_path)
    initial_count = len(df)
    logging.info(f"Loaded {initial_count} raw records.")

    # 2. Data Quality Validation Rules
    # Rule A: Primary/Foreign keys cannot be null
    # Rule B: Price must be strictly greater than 0, and freight_value cannot be negative
    valid_mask = (
        df["order_id"].notna() &
        df["product_id"].notna() &
        df["seller_id"].notna() &
        (df["price"] > 0) &
        (df["freight_value"] >= 0)
    )

    clean_df = df[valid_mask].copy()
    rejected_df = df[~valid_mask].copy()

    # 3. Route Data to Appropriate Zones
    clean_output = os.path.join(CLEAN_ZONE_DIR, "clean_order_items.csv")
    clean_df.to_csv(clean_output, index=False)
    logging.info(f"Saved {len(clean_df)} valid records to {clean_output}")

    if len(rejected_df) > 0:
        reject_output = os.path.join(QUARANTINE_DIR, "rejected_order_items.csv")
        rejected_df.to_csv(reject_output, index=False)
        logging.warning(f"Quarantined {len(rejected_df)} invalid records to {reject_output}")
    else:
        logging.info("Zero invalid records found. Data quality check passed 100%.")

if __name__ == "__main__":
    ingest_order_items()

