"""
Logistics Portfolio - Upload CSV files to Azure Blob Storage
=============================================================
Install required library:
    pip install azure-storage-blob

Set environment variable before running:
    Windows PowerShell:
        $env:AZURE_STORAGE_CONNECTION_STRING = "your_connection_string_here"

How to run:
    python upload_to_blob.py
"""

import os
from pathlib import Path
from azure.storage.blob import BlobServiceClient

# ============================================================
# Configuration
# ============================================================
CONTAINER_NAME = "raw-data"
DATA_FOLDER    = "data"

# Load connection string from environment variable
CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")

if not CONNECTION_STRING:
    raise EnvironmentError(
        "Environment variable 'AZURE_STORAGE_CONNECTION_STRING' is not set.\n"
        "Run this in PowerShell first:\n"
        "  $env:AZURE_STORAGE_CONNECTION_STRING = 'your_connection_string_here'"
    )

# ============================================================
# Upload files
# ============================================================
def upload_csv_files():
    client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container = client.get_container_client(CONTAINER_NAME)

    csv_files = list(Path(DATA_FOLDER).glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in '{DATA_FOLDER}' folder.")
        return

    print(f"Found {len(csv_files)} CSV files. Starting upload...\n")

    success = 0
    failed  = 0

    for filepath in sorted(csv_files):
        blob_name = filepath.name
        try:
            with open(filepath, "rb") as f:
                container.upload_blob(
                    name=blob_name,
                    data=f,
                    overwrite=True  # Overwrite if file already exists
                )
            size_kb = filepath.stat().st_size / 1024
            print(f"  Uploaded: {blob_name:<35} ({size_kb:>8.1f} KB)")
            success += 1
        except Exception as e:
            print(f"  Failed:   {blob_name:<35} -> {e}")
            failed += 1

    # ============================================================
    # Summary
    # ============================================================
    print(f"\n=== Upload complete ===")
    print(f"  Success : {success} files")
    if failed > 0:
        print(f"  Failed  : {failed} files")


if __name__ == "__main__":
    upload_csv_files()