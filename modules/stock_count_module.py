from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class StockCountItem(BaseModel):
    transaction_id: str = Field(..., description="Transaction ID")
    item_code: str = Field(..., description="Item Code")
    item_desc: str = Field(..., description="Item Description")
    book_bulk: int = Field(..., description="Book Bulk Quantity")
    book_actual: int = Field(..., description="Book Actual Quantity")
    float_book: int = Field(..., description="Float Book Quantity")
    float_actual: int = Field(..., description="Float Actual Quantity")
    is_review_yn: str = Field(..., description="Review Status (Y/N)")

class StockCountResponse(BaseModel):
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    data: Optional[List[StockCountItem]] = Field(None, description="Stock count data")
    total_items: int = Field(0, description="Total number of items")

class StockCountModule:
    def __init__(self):
        self.stockCountList = []
        
        # Dummy data with multiple records per transaction ID
        # Transaction TXN001 - Multiple items
        stock1 = {
            "transaction_id": "TXN001",
            "item_code": "ITEM001",
            "item_desc": "Chicken Biryani",
            "book_bulk": 100,
            "book_actual": 95,
            "float_book": 50,
            "float_actual": 48,
            "is_review_yn": "N"
        }
        
        stock2 = {
            "transaction_id": "TXN001",
            "item_code": "ITEM002", 
            "item_desc": "Vegetable Curry",
            "book_bulk": 75,
            "book_actual": 72,
            "float_book": 30,
            "float_actual": 29,
            "is_review_yn": "N"
        }
        
        stock3 = {
            "transaction_id": "TXN001",
            "item_code": "ITEM003",
            "item_desc": "Rice Pilaf",
            "book_bulk": 120,
            "book_actual": 118,
            "float_book": 60,
            "float_actual": 58,
            "is_review_yn": "N"
        }
        
        # Transaction TXN002 - Multiple items
        stock4 = {
            "transaction_id": "TXN002",
            "item_code": "ITEM004",
            "item_desc": "Naan Bread",
            "book_bulk": 200,
            "book_actual": 195,
            "float_book": 100,
            "float_actual": 97,
            "is_review_yn": "N"
        }
        
        stock5 = {
            "transaction_id": "TXN002",
            "item_code": "ITEM005",
            "item_desc": "Fruit Salad",
            "book_bulk": 80,
            "book_actual": 78,
            "float_book": 40,
            "float_actual": 39,
            "is_review_yn": "N"
        }
        
        # Transaction TXN003 - Single item
        stock6 = {
            "transaction_id": "TXN003",
            "item_code": "ITEM006",
            "item_desc": "Beef Steak",
            "book_bulk": 60,
            "book_actual": 58,
            "float_book": 25,
            "float_actual": 24,
            "is_review_yn": "N"
        }
        
        # Transaction TXN004 - Multiple items
        stock7 = {
            "transaction_id": "TXN004",
            "item_code": "ITEM007",
            "item_desc": "Fish Curry",
            "book_bulk": 90,
            "book_actual": 87,
            "float_book": 45,
            "float_actual": 43,
            "is_review_yn": "N"
        }
        
        stock8 = {
            "transaction_id": "TXN004",
            "item_code": "ITEM008",
            "item_desc": "Dal Makhani",
            "book_bulk": 110,
            "book_actual": 108,
            "float_book": 55,
            "float_actual": 53,
            "is_review_yn": "N"
        }
        
        stock9 = {
            "transaction_id": "TXN004",
            "item_code": "ITEM009",
            "item_desc": "Raita",
            "book_bulk": 150,
            "book_actual": 147,
            "float_book": 75,
            "float_actual": 73,
            "is_review_yn": "N"
        }
        
        # Transaction TXN005 - Multiple items
        stock10 = {
            "transaction_id": "TXN005",
            "item_code": "ITEM010",
            "item_desc": "Paneer Tikka",
            "book_bulk": 70,
            "book_actual": 68,
            "float_book": 35,
            "float_actual": 34,
            "is_review_yn": "N"
        }
        
        stock11 = {
            "transaction_id": "TXN005",
            "item_code": "ITEM011",
            "item_desc": "Mixed Vegetables",
            "book_bulk": 85,
            "book_actual": 83,
            "float_book": 42,
            "float_actual": 41,
            "is_review_yn": "N"
        }
        
        # Add all records to the list
        self.stockCountList.append(stock1)
        self.stockCountList.append(stock2)
        self.stockCountList.append(stock3)
        self.stockCountList.append(stock4)
        self.stockCountList.append(stock5)
        self.stockCountList.append(stock6)
        self.stockCountList.append(stock7)
        self.stockCountList.append(stock8)
        self.stockCountList.append(stock9)
        self.stockCountList.append(stock10)
        self.stockCountList.append(stock11)

    def get_stock_count_details(self, transaction_id: str) -> StockCountResponse:
        # Check if transaction_id is provided
        if not transaction_id:
            return StockCountResponse(
                status="error",
                message="Please provide a valid transaction ID.",
                data=None,
                total_items=0
            )
        
        # Find all stock count records that match the transaction_id
        matching_records = []
        for stock in self.stockCountList:
            if stock["transaction_id"] == transaction_id:
                matching_records.append(stock)
        
        # Return results based on number of matches
        if len(matching_records) == 0:
            return StockCountResponse(
                status="error",
                message="Stock count details not found for the given transaction ID",
                data=None,
                total_items=0
            )
        else:
            # Convert to Pydantic models
            stock_count_items = [StockCountItem(**record) for record in matching_records]
            return StockCountResponse(
                status="success",
                message=f"Found {len(stock_count_items)} stock count records for transaction {transaction_id}",
                data=stock_count_items,
                total_items=len(stock_count_items)
            ) 