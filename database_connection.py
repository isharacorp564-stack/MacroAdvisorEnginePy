from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import json

# Define database location
DB_FILE = "natwest_guardian.db"
DATABASE_URL = f"sqlite:///{DB_FILE}"

Base = declarative_base()

# --- DATABASE TABLE SCHEMA MODEL ---
class CustomerRecord(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    segment = Column(String, nullable=False)
    name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    balance_capital = Column(String, nullable=False)
    liability_facility = Column(String, nullable=False)
    risk_factor = Column(String, nullable=False)


# --- DATABASE MANAGER CLASS (Separation of Concerns) ---
class NatWestDatabaseManager:
    def __init__(self):
        # check_same_thread=False is mandatory for asynchronous Streamlit operations
        self.engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo=False
        )
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_customer_names_by_segment(self, segment_name: str) -> list:
        """Retrieves a list of customer names filtered by segment."""
        session = self.SessionLocal()
        try:
            # Query only the name column to save database execution memory
            records = session.query(CustomerRecord.name).filter(CustomerRecord.segment == segment_name).all()
            return [row.name for row in records]
        finally:
            session.close()

    def get_customer_profile(self, customer_name: str) -> dict:
        """Retrieves a full customer record and maps it to a standard dictionary payload."""
        session = self.SessionLocal()
        try:
            customer = session.query(CustomerRecord).filter(CustomerRecord.name == customer_name).first()
            if customer:
                return {
                    "Location": customer.location,
                    "Balance": customer.balance_capital,
                    "Mtg/Facility": customer.liability_facility,
                    "Risk": customer.risk_factor
                }
            return {}
        finally:
            session.close()

# --- 🔌 MODEL CONTEXT PROTOCOL (MCP) INTERFACE ENVIRONMENT ---
# Encapsulates traditional data lookups into standardized JSON-RPC MCP Client Tool schemas
class NatWestMCPServerClient:
    def __init__(self, db_manager: NatWestDatabaseManager):
        self.db = db_manager

    def get_mcp_tool_definitions(self) -> list:
        """Returns the formal standard MCP Tool Schema manifest for LLM Tool Binding."""
        return [{
            "type": "function",
            "function": {
                "name": "mcp_query_customer_profile",
                "description": "Securely fetches complete internal bank ledger details from the natwest_guardian database core schema via MCP protocol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_name": {"type": "string", "description": "The exact name of the customer profile record to search."}
                    },
                    "required": ["customer_name"]
                }
            }
        }]

    def execute_mcp_tool_call(self, tool_name: str, arguments: dict) -> str:
        """Acts as the MCP Host Server Executor, processing tool string blocks."""
        if tool_name == "mcp_query_customer_profile":
            name_param = arguments.get("customer_name")
            session = self.db.SessionLocal()
            try:
                customer = session.query(CustomerRecord).filter(CustomerRecord.name == name_param).first()
                if customer:
                    payload = {
                        "mcp_status": "200_OK",
                        "location": customer.location,
                        "capital_balance": customer.balance_capital,
                        "facility_liability": customer.liability_facility,
                        "macro_vulnerability": customer.risk_factor
                    }
                    return json.dumps(payload)
                return json.dumps({"mcp_status": "404_NOT_FOUND", "error": "Profile match failed."})
            finally:
                session.close()
        return json.dumps({"mcp_status": "501_NOT_IMPLEMENTED"})