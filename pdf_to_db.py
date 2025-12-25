"""Main module combining PDF extraction, pattern matching, and MongoDB storage."""
from pdf_extractor import PDFExtractor
from pattern_matcher import PatternMatcher
from mongodb_handler import MongoDBHandler
from typing import List, Optional
import json
from pathlib import Path


class PDFToDB:
    """Main class for converting PDFs to MongoDB database or JSON file."""
    
    def __init__(self, mongodb_uri: str = None, database_name: str = None, use_mongodb: bool = True):
        """
        Initialize PDF to DB converter.
        
        Args:
            mongodb_uri: MongoDB connection URI
            database_name: Database name
            use_mongodb: If False, skip MongoDB initialization (for JSON output mode)
        """
        self.pdf_extractor = PDFExtractor()
        self.use_mongodb = use_mongodb
        if use_mongodb:
            self.mongodb_handler = MongoDBHandler(mongodb_uri, database_name)
        else:
            self.mongodb_handler = None
    
    def process_directory(
        self,
        pdf_directory: str,
        keywords: List[str],
        collection_name: str = None,
        json_file: str = None
    ) -> int:
        """
        Process all PDFs in a directory and store extracted data in MongoDB or JSON.
        
        Args:
            pdf_directory: Path to directory containing PDFs
            keywords: List of keywords to extract (e.g., ["ID", "Color", "Model", "Year"])
            collection_name: MongoDB collection name to store data (required if using MongoDB)
            json_file: Path to JSON file to write data (required if not using MongoDB)
            
        Returns:
            Number of records processed
        """
        print(f"Extracting text from PDFs in {pdf_directory}...")
        text = self.pdf_extractor.extract_text_from_directory(pdf_directory)
        
        print(f"Extracting records using keywords: {', '.join(keywords)}...")
        pattern_matcher = PatternMatcher(keywords)
        records = pattern_matcher.extract_records(text)
        
        print(f"Found {len(records)} records.")
        
        if not records:
            print("No records found.")
            return 0
        
        if json_file:
            # Write to JSON file
            return self._write_to_json(json_file, records)
        elif self.use_mongodb:
            # Write to MongoDB
            if not collection_name:
                raise ValueError("collection_name is required when using MongoDB")
            print(f"Inserting records into MongoDB collection '{collection_name}'...")
            inserted_count = self.mongodb_handler.insert_records(collection_name, records)
            return inserted_count
        else:
            raise ValueError("Either json_file must be provided or MongoDB must be enabled")
    
    def _write_to_json(self, json_file: str, records: List[dict]) -> int:
        """
        Write records to a JSON file.
        
        Args:
            json_file: Path to JSON file
            records: List of records to write
            
        Returns:
            Number of records written
        """
        json_path = Path(json_file)
        # Create parent directory if it doesn't exist
        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Writing {len(records)} records to {json_file}...")
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Successfully wrote {len(records)} records to {json_file}")
        return len(records)
    
    def close(self):
        """Close MongoDB connection."""
        if self.mongodb_handler:
            self.mongodb_handler.close()

