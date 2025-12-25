#!/usr/bin/env python3
"""Example usage of the PDF to MongoDB converter."""
from pdf_to_db import PDFToDB

# Example 1: Basic usage with environment variables
def example_basic():
    """Basic example using default MongoDB settings from .env file."""
    converter = PDFToDB()
    
    converter.process_directory(
        pdf_directory="./pdfs",
        keywords=["ID", "Color", "Model", "Year"],
        collection_name="cars"
    )
    
    converter.close()


# Example 2: Custom MongoDB connection
def example_custom_mongodb():
    """Example with custom MongoDB URI and database name."""
    converter = PDFToDB(
        mongodb_uri="mongodb://localhost:27017/",
        database_name="my_database"
    )
    
    converter.process_directory(
        pdf_directory="./pdfs",
        keywords=["ID", "Color", "Model", "Year"],
        collection_name="cars"
    )
    
    converter.close()


# Example 3: Different keyword pattern
def example_different_pattern():
    """Example with different keywords (e.g., products)."""
    converter = PDFToDB()
    
    converter.process_directory(
        pdf_directory="./pdfs",
        keywords=["ProductID", "Name", "Price", "Category", "Stock"],
        collection_name="products"
    )
    
    converter.close()


if __name__ == "__main__":
    print("Example usage scripts for PDF to MongoDB converter")
    print("Uncomment the example you want to run:")
    # example_basic()
    # example_custom_mongodb()
    # example_different_pattern()

