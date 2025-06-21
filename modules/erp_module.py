from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ERPItem(BaseModel):
    transaction_id: str = Field(..., description="Transaction ID")
    item_code: str = Field(..., description="Item Code")
    item_desc: str = Field(..., description="Item Description")
    book_bulk: int = Field(..., description="Book Bulk Quantity")
    book_actual: int = Field(..., description="Book Actual Quantity")
    float_book: int = Field(..., description="Float Book Quantity")
    float_actual: int = Field(..., description="Float Actual Quantity")

class ERPResponse(BaseModel):
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    data: Optional[List[ERPItem]] = Field(None, description="ERP data")
    total_items: int = Field(0, description="Total number of items")

class ERPModule:
    def __init__(self):
        self.erpList = []
        
        # Dummy data with multiple records per transaction ID
        # Transaction TXN001 - Multiple items
        erp1 = {
            "transaction_id": "TXN001",
            "item_code": "ITEM001",
            "item_desc": "Chicken Biryani",
            "book_bulk": 100,
            "book_actual": 98,
            "float_book": 50,
            "float_actual": 49
        }
        
        erp2 = {
            "transaction_id": "TXN001",
            "item_code": "ITEM002", 
            "item_desc": "Vegetable Curry",
            "book_bulk": 70,
            "book_actual": 72,
            "float_book": 30,
            "float_actual": 28
        }
        
        erp3 = {
            "transaction_id": "TXN001",
            "item_code": "ITEM003",
            "item_desc": "Rice Pilaf",
            "book_bulk": 120,
            "book_actual": 118,
            "float_book": 60,
            "float_actual": 59
        }
        
        # Transaction TXN002 - Multiple items
        erp4 = {
            "transaction_id": "TXN002",
            "item_code": "ITEM004",
            "item_desc": "Naan Bread",
            "book_bulk": 200,
            "book_actual": 198,
            "float_book": 100,
            "float_actual": 99
        }
        
        erp5 = {
            "transaction_id": "TXN002",
            "item_code": "ITEM005",
            "item_desc": "Fruit Salad",
            "book_bulk": 80,
            "book_actual": 79,
            "float_book": 40,
            "float_actual": 39
        }
        
        # Transaction TXN003 - Single item
        erp6 = {
            "transaction_id": "TXN003",
            "item_code": "ITEM006",
            "item_desc": "Beef Steak",
            "book_bulk": 60,
            "book_actual": 59,
            "float_book": 25,
            "float_actual": 24
        }
        
        # Transaction TXN004 - Multiple items
        erp7 = {
            "transaction_id": "TXN004",
            "item_code": "ITEM007",
            "item_desc": "Fish Curry",
            "book_bulk": 90,
            "book_actual": 88,
            "float_book": 45,
            "float_actual": 44
        }
        
        erp8 = {
            "transaction_id": "TXN004",
            "item_code": "ITEM008",
            "item_desc": "Dal Makhani",
            "book_bulk": 110,
            "book_actual": 109,
            "float_book": 55,
            "float_actual": 54
        }
        
        erp9 = {
            "transaction_id": "TXN004",
            "item_code": "ITEM009",
            "item_desc": "Raita",
            "book_bulk": 150,
            "book_actual": 148,
            "float_book": 75,
            "float_actual": 74
        }
        
        # Transaction TXN005 - Multiple items
        erp10 = {
            "transaction_id": "TXN005",
            "item_code": "ITEM010",
            "item_desc": "Paneer Tikka",
            "book_bulk": 70,
            "book_actual": 69,
            "float_book": 35,
            "float_actual": 34
        }
        
        erp11 = {
            "transaction_id": "TXN005",
            "item_code": "ITEM011",
            "item_desc": "Mixed Vegetables",
            "book_bulk": 85,
            "book_actual": 84,
            "float_book": 42,
            "float_actual": 41
        }
        
        # Add all records to the list
        self.erpList.append(erp1)
        self.erpList.append(erp2)
        self.erpList.append(erp3)
        self.erpList.append(erp4)
        self.erpList.append(erp5)
        self.erpList.append(erp6)
        self.erpList.append(erp7)
        self.erpList.append(erp8)
        self.erpList.append(erp9)
        self.erpList.append(erp10)
        self.erpList.append(erp11)

    def get_erp_details(self, transaction_id: str) -> ERPResponse:
        # Check if transaction_id is provided
        if not transaction_id:
            return ERPResponse(
                status="error",
                message="Please provide a valid transaction ID.",
                data=None,
                total_items=0
            )
        
        # Find all ERP records that match the transaction_id
        matching_records = []
        for erp in self.erpList:
            if erp["transaction_id"] == transaction_id:
                matching_records.append(erp)
        
        # Return results based on number of matches
        if len(matching_records) == 0:
            return ERPResponse(
                status="error",
                message="ERP details not found for the given transaction ID",
                data=None,
                total_items=0
            )
        else:
            # Convert to Pydantic models
            erp_items = [ERPItem(**record) for record in matching_records]
            return ERPResponse(
                status="success",
                message=f"Found {len(erp_items)} ERP records for transaction {transaction_id}",
                data=erp_items,
                total_items=len(erp_items)
            ) 