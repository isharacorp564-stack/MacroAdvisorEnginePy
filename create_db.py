import sqlite3

# Pre-formatted records matching NatWest's test variables
# Expanded pre-formatted records matching NatWest's target variables
mock_data = [
    # --- ORIGINAL DATA RECORDS ---
    ("Retail", "Fiona Gallagher", "EDI", "£8,400", "Ext Fixed (£185k, Ends Oct 2026)", "UK Energy Surcharges"),
    ("Retail", "James Sterling", "LON", "£45,000", "NatWest Tracker (£320k remaining)", "BoE Rate Vulnerability"),
    ("Corporate", "Caledonian Manufacturing Ltd", "MAN", "£245,000", "£50k Overdraft Facility",
     "German Steel Imports / EUR Tariff"),
    ("Corporate", "Apex Global Logistics", "BFS", "£1,200,000", "£250k Credit Line", "Maritime Fuel Surcharges"),

    # --- NEW ADDED DUMMY RETAIL CUSTOMERS ---
    (
        "Retail",
        "Aisha Rahman",
        "BHM",
        "£12,300",
        "NatWest Fixed-Rate Mortgage (£210k, 5.2% Ends Dec 2026)",
        "UK Property Tax / Stamp Duty Changes"
    ),
    (
        "Retail",
        "David Vance",
        "STG",
        "£62,000",
        "None (Outright Homeowner)",
        "UK Services Inflation Erosion on Cash Savings"
    ),
    (
        "Retail",
        "Chloe Jenkins",
        "CRD",
        "£3,100",
        "NatWest Graduate Personal Loan (£8,500 remaining at 6.8%)",
        "UK Domestic Grocery Inflation / High Debt Servicing"
    ),

    # --- NEW ADDED DUMMY CORPORATE SME CUSTOMERS ---
    (
        "Corporate",
        "Mersey Green Energy Solutions",
        "LIV",
        "£410,000",
        "£150k NatWest Climate Transition Loan (Unused)",
        "UK Eco-Tariffs and Variable Carbon Taxes"
    ),
    (
        "Corporate",
        "Thames Tech Distribution",
        "LON",
        "£2,850,000",
        "£500k Commercial Term Loan",
        "Microchip Import Delays / USD to GBP FX Volatility"
    ),
    (
        "Corporate",
        "Highland Agri-Foods",
        "INV",
        "£95,000",
        "£30k NatWest Agriculture Working Capital Line",
        "UK Fertilizer Import Tariffs and Diesel Fuel Volatility"
    )
]

# Establish local connection to write the physical file
db_path = "natwest_guardian.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Build the table schema to fit the SQLAlchemy models
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    segment TEXT NOT NULL,
    name TEXT UNIQUE NOT NULL,
    location TEXT NOT NULL,
    balance_capital TEXT NOT NULL,
    liability_facility TEXT NOT NULL,
    risk_factor TEXT NOT NULL
)
''')

# Seed the records cleanly into the relational matrix
cursor.executemany('''
INSERT OR IGNORE INTO customers (segment, name, location, balance_capital, liability_facility, risk_factor)
VALUES (?, ?, ?, ?, ?, ?)
''', mock_data)

conn.commit()
conn.close()
print("🎯 Success! 'natwest_guardian.db' has been natively compiled in your directory.")
