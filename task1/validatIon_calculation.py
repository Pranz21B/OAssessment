import sys
import subprocess
import os

# --- AUTO-SETUP SECTION ---
def install_and_restart():
    print("First run detected. Installing required libraries...")
    try:
        # Install packages silently
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "openpyxl"])
        print("Installation complete. Restarting script...")
        # Restart the script so imports work
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print(f"Auto-install failed: {e}")
        print("Please run: pip install pandas openpyxl")
        input("Press Enter to exit...")
        sys.exit()

try:
    import sqlite3
    import pandas as pd
except ImportError:
    install_and_restart()

# --- MAIN LOGIC STARTS HERE ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load CSVs into SQLite
conn = sqlite3.connect(":memory:")
source = pd.read_csv("source_calculations.csv")
output = pd.read_csv("distribution_output.csv")
source.to_sql("source_calculations", conn, index=False)
output.to_sql("distribution_output", conn, index=False)

# Run validation queries
queries = {
    "MISSING_RECORD": """
        SELECT s.client_id, s.client_name, 'MISSING_RECORD' AS discrepancy_type
        FROM source_calculations s
        LEFT JOIN distribution_output d ON s.client_id = d.client_id
        WHERE d.client_id IS NULL
    """,
    "ORPHAN_RECORD": """
        SELECT d.client_id, d.client_name, 'ORPHAN_RECORD' AS discrepancy_type
        FROM distribution_output d
        LEFT JOIN source_calculations s ON d.client_id = s.client_id
        WHERE s.client_id IS NULL
    """,
    "AMOUNT_MISMATCH": """
        SELECT s.client_id, s.client_name, 'AMOUNT_MISMATCH' AS discrepancy_type
        FROM source_calculations s
        INNER JOIN distribution_output d ON s.client_id = d.client_id
        WHERE ABS(s.expected_net_amount - d.distributed_amount) > 0.005
    """,
    "DUPLICATE_RECORD": """
        SELECT d.client_id, d.client_name, 'DUPLICATE_RECORD' AS discrepancy_type
        FROM distribution_output d
        GROUP BY d.client_id, d.client_name
        HAVING COUNT(*) > 1
    """
}

all_results = []
for name, query in queries.items():
    df = pd.read_sql(query, conn)
    all_results.append(df)

details = pd.concat(all_results, ignore_index=True)

# Build pivot summary
summary = details.groupby("discrepancy_type").agg(
    discrepancy_count=("client_id", "count"),
    affected_clients=("client_id", lambda x: ", ".join(x))
).reset_index().sort_values("discrepancy_count", ascending=False)

# Export to Excel
with pd.ExcelWriter("findings.xlsx", engine="openpyxl") as writer:
    summary.to_excel(writer, sheet_name="Pivot_Summary", index=False)
    details.to_excel(writer, sheet_name="All_Discrepancies", index=False)

print("=== PIVOT SUMMARY ===")
print(summary.to_string(index=False))
print("\n=== ALL DISCREPANCIES ===")
print(details.to_string(index=False))
print("\nSaved to findings.xlsx")

conn.close()
input("\nPress Enter to exit...")