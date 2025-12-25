"""Main module combining PDF extraction, pattern matching, and MongoDB storage."""
from pdf_extractor import PDFExtractor
from pattern_matcher import PatternMatcher
from mongodb_handler import MongoDBHandler
from typing import List


class PDFToDB:
    """Main class for converting PDFs to MongoDB database."""
    
    def __init__(self, mongodb_uri: str = None, database_name: str = None):
        """
        Initialize PDF to DB converter.
        
        Args:
            mongodb_uri: MongoDB connection URI
            database_name: Database name
        """
        self.pdf_extractor = PDFExtractor()
        self.mongodb_handler = MongoDBHandler(mongodb_uri, database_name)
    
    def process_directory(
        self,
        pdf_directory: str,
        keywords: List[str],
        collection_name: str
    ) -> int:
        """
        Process all PDFs in a directory and store extracted data in MongoDB.
        
        Args:
            pdf_directory: Path to directory containing PDFs
            keywords: List of keywords to extract (e.g., ["ID", "Color", "Model", "Year"])
            collection_name: MongoDB collection name to store data
            
        Returns:
            Number of records inserted
        """
        print(f"Extracting text from PDFs in {pdf_directory}...")
        text = self.pdf_extractor.extract_text_from_directory(pdf_directory)
        
        print(f"Extracting records using keywords: {', '.join(keywords)}...")
        pattern_matcher = PatternMatcher(keywords)
        records = pattern_matcher.extract_records(text)
        
        print(f"Found {len(records)} records.")
        
        if records:
            print(f"Inserting records into MongoDB collection '{collection_name}'...")
            inserted_count = self.mongodb_handler.insert_records(collection_name, records)
            return inserted_count
        else:
            print("No records found to insert.")
            return 0
    
    def close(self):
        """Close MongoDB connection."""
        self.mongodb_handler.close()

