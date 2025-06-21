import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class ExportTextModule:
    def __init__(self):
        self.export_directory = os.getcwd()  # Current working directory
    
    def export_to_text(self, data: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """
        Export data to text file with tabular formatting.
        
        Args:
            data: List of dictionaries containing the data to export
            filename: Optional filename. If not provided, generates a timestamped filename
            
        Returns:
            str: Path to the exported text file
        """
        try:
            # Convert single dict to list for consistent processing
            if isinstance(data, dict):
                data = [data]
            
            # Validate data
            if not data or not isinstance(data, list):
                return "Error: Invalid data format. Expected a list of dictionaries or a single dictionary."
            
            if not data[0] or not isinstance(data[0], dict):
                return "Error: Invalid data format. Each item should be a dictionary."
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"exported_data_{timestamp}.txt"
            
            # Ensure filename has .txt extension
            if not filename.endswith('.txt'):
                filename += '.txt'
            
            # Create full file path
            file_path = os.path.join(self.export_directory, filename)
            
            # Get all unique keys from all dictionaries
            all_keys = set()
            for item in data:
                all_keys.update(item.keys())
            keys = sorted(list(all_keys))
            
            # Calculate column widths
            col_widths = {}
            for key in keys:
                col_widths[key] = len(str(key))
                for item in data:
                    col_widths[key] = max(col_widths[key], len(str(item.get(key, ''))))
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                # Write header
                header = " | ".join(str(key).ljust(col_widths[key]) for key in keys)
                f.write(header + "\n")
                
                # Write separator line
                separator = "-" * len(header)
                f.write(separator + "\n")
                
                # Write data rows
                for item in data:
                    row = " | ".join(str(item.get(key, '')).ljust(col_widths[key]) for key in keys)
                    f.write(row + "\n")
            
            return f"Successfully exported data to: {file_path}"
            
        except Exception as e:
            return f"Error exporting data: {str(e)}"
    
    def export_stock_count_to_text(self, stock_data: List[Dict[str, Any]], transaction_id: Optional[str] = None) -> str:
        """
        Specialized function to export stock count data with meaningful filename.
        
        Args:
            stock_data: Stock count data to export
            transaction_id: Optional transaction ID for filename
            
        Returns:
            str: Path to the exported text file
        """
        try:
            # Generate filename based on transaction ID
            if transaction_id:
                filename = f"stock_count_{transaction_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            else:
                filename = f"stock_count_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            return self.export_to_text(stock_data, filename)
            
        except Exception as e:
            return f"Error exporting stock count data: {str(e)}"
    
    def export_pre_approval_data(self, data: List[Dict[str, Any]]) -> str:
        """
        Specialized function for exporting pre-approval data with specific filename.
        
        Args:
            data: Pre-approval data to export
            
        Returns:
            str: Path to the exported text file
        """
        try:
            # Generate filename with date and time for pre-approval data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pre_approval_{timestamp}.txt"
            
            return self.export_to_text(data, filename)
            
        except Exception as e:
            return f"Error exporting pre-approval data: {str(e)}"

    def export_post_approval_data(self, data: List[Dict[str, Any]]) -> str:
        """
        Specialized function for exporting post-approval ERP data with specific filename.
        
        Args:
            data: Post-approval ERP data to export
            
        Returns:
            str: Path to the exported text file
        """
        try:
            # Generate filename with date and time for post-approval data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"post_approval_{timestamp}.txt"
            
            return self.export_to_text(data, filename)
            
        except Exception as e:
            return f"Error exporting post-approval data: {str(e)}" 