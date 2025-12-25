"""Module for MongoDB database operations."""
from pymongo import MongoClient
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()


class MongoDBHandler:
    """Handles MongoDB connection and data insertion."""
    
    def __init__(self, mongodb_uri: str = None, database_name: str = None):
        """
        Initialize MongoDB handler.
        
        Args:
            mongodb_uri: MongoDB connection URI (defaults to MONGODB_URI env var)
            database_name: Database name (defaults to DATABASE_NAME env var)
        """
        self.mongodb_uri = mongodb_uri or os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.database_name = database_name or os.getenv("DATABASE_NAME", "pdf_data")
        
        try:
            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client[self.database_name]
            # Test connection
            self.client.admin.command('ping')
            print(f"Connected to MongoDB: {self.database_name}")
        except Exception as e:
            raise Exception(f"Failed to connect to MongoDB: {str(e)}")
    
    def insert_records(self, collection_name: str, records: List[Dict[str, Any]]) -> int:
        """
        Insert records into a MongoDB collection.
        
        Args:
            collection_name: Name of the collection
            records: List of dictionaries to insert
            
        Returns:
            Number of records inserted
        """
        if not records:
            print("No records to insert.")
            return 0
        
        collection = self.db[collection_name]
        
        # Check for duplicates based on first field (typically ID)
        inserted_count = 0
        skipped_count = 0
        
        for record in records:
            # Use the first key as the unique identifier for duplicate checking
            first_key = list(record.keys())[0] if record else None
            if first_key:
                # Check if record with same first key value already exists
                existing = collection.find_one({first_key: record[first_key]})
                if existing:
                    # Update existing record
                    collection.update_one(
                        {first_key: record[first_key]},
                        {"$set": record}
                    )
                    skipped_count += 1
                else:
                    # Insert new record
                    collection.insert_one(record)
                    inserted_count += 1
            else:
                # If no first key, just insert
                collection.insert_one(record)
                inserted_count += 1
        
        print(f"Inserted {inserted_count} new records, updated {skipped_count} existing records.")
        return inserted_count
    
    def close(self):
        """Close MongoDB connection."""
        if hasattr(self, 'client'):
            self.client.close()
            print("MongoDB connection closed.")

