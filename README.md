# PDF to MongoDB Converter

A tool that extracts structured data from PDFs based on keyword patterns and stores it in MongoDB.

## Features

- Extract structured data from PDF files based on customizable keyword patterns
- Process single or multiple PDFs from a directory
- Store extracted data in MongoDB collections
- Flexible pattern matching for various data formats

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=pdf_data
```

## Usage

### Command Line Interface

```bash
python main.py --pdf-dir /path/to/pdfs --keywords ID Color Model Year --collection cars
```

### Python API

```python
from pdf_to_db import PDFToDB

converter = PDFToDB(
    mongodb_uri="mongodb://localhost:27017/",
    database_name="pdf_data"
)

converter.process_directory(
    pdf_directory="/path/to/pdfs",
    keywords=["ID", "Color", "Model", "Year"],
    collection_name="cars"
)
```

## How It Works

1. **PDF Extraction**: Extracts text from all PDFs in the specified directory
2. **Pattern Matching**: Searches for patterns like "ID: 1 Color: red Model: chevy Year: 2020"
3. **Data Extraction**: Groups data by the first keyword (typically an ID) and extracts all property values
4. **MongoDB Storage**: Stores each extracted record as a document in the specified collection

## Example

Given a PDF with content:
```
ID: 1 Color: red Model: chevy Year: 2020
ID: 2 Color: blue Model: ford Year: 2021
```

With keywords: `["ID", "Color", "Model", "Year"]`

The tool will create MongoDB documents:
```json
{"ID": "1", "Color": "red", "Model": "chevy", "Year": "2020"}
{"ID": "2", "Color": "blue", "Model": "ford", "Year": "2021"}
```

