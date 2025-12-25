"""Module for extracting text from PDF files."""
import pdfplumber
from pathlib import Path
from typing import List


class PDFExtractor:
    """Extracts text content from PDF files."""
    
    def __init__(self):
        pass
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract all text from a single PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise Exception(f"Error extracting text from {pdf_path}: {str(e)}")
        
        return text
    
    def extract_text_from_directory(self, directory_path: str) -> str:
        """
        Extract text from all PDF files in a directory.
        
        Args:
            directory_path: Path to directory containing PDFs
            
        Returns:
            Combined text from all PDFs
        """
        directory = Path(directory_path)
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        pdf_files = list(directory.glob("*.pdf"))
        if not pdf_files:
            raise ValueError(f"No PDF files found in {directory_path}")
        
        all_text = ""
        for pdf_file in pdf_files:
            print(f"Processing {pdf_file.name}...")
            text = self.extract_text_from_pdf(str(pdf_file))
            all_text += text + "\n\n"
        
        return all_text

