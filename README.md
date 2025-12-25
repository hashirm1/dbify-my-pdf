# PDF to MongoDB/JSON Converter

A tool that extracts structured data from PDFs based on keyword patterns and stores it in MongoDB or JSON files.

## Features

- Extract structured data from PDF files based on customizable keyword patterns
- Process single or multiple PDFs from a directory
- Store extracted data in MongoDB collections or JSON files
- Flexible pattern matching for various data formats
- No MongoDB required when using JSON output mode

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

**For MongoDB output only:** Create a `.env` file in the project root:

```
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=pdf_data
```

**Note:** Configuration is only needed when using MongoDB output. JSON output mode doesn't require any configuration or MongoDB installation.

## Usage

### Command Line Interface

**Output to MongoDB:**
```bash
python main.py --pdf-dir /path/to/pdfs --keywords "ID,Color,Model,Year" --collection cars
```

**Output to JSON file (no MongoDB required):**
```bash
python main.py --pdf-dir /path/to/pdfs --keywords "ID,Color,Model,Year" --json-file output.json
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
4. **Storage**: Stores each extracted record either:
   - In a MongoDB collection (if `--collection` is provided)
   - In a JSON file (if `--json-file` is provided)

## Example

Given a PDF with content:
```
ID: 1 Color: red Model: chevy Year: 2020
ID: 2 Color: blue Model: ford Year: 2021
```

With keywords: `["ID", "Color", "Model", "Year"]`

The tool will create records (MongoDB documents or JSON array):
```json
[
  {"ID": "1", "Color": "red", "Model": "chevy", "Year": "2020"},
  {"ID": "2", "Color": "blue", "Model": "ford", "Year": "2021"}
]
```

