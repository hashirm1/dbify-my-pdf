#!/usr/bin/env python3
"""Command-line interface for PDF to MongoDB converter."""
import click
import sys
from pathlib import Path
from pdf_to_db import PDFToDB


@click.command()
@click.option(
    '--pdf-dir',
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help='Directory containing PDF files to process'
)
@click.option(
    '--keywords',
    required=True,
    help='Comma-separated list of keywords (e.g., "ID,Color,Model,Year")'
)
@click.option(
    '--collection',
    default=None,
    help='MongoDB collection name to store the data (required if not using --json-file)'
)
@click.option(
    '--json-file',
    default=None,
    type=click.Path(),
    help='Output JSON file path (if provided, data will be written to JSON instead of MongoDB)'
)
@click.option(
    '--mongodb-uri',
    default=None,
    help='MongoDB connection URI (defaults to MONGODB_URI env var, ignored if --json-file is used)'
)
@click.option(
    '--database',
    default=None,
    help='MongoDB database name (defaults to DATABASE_NAME env var, ignored if --json-file is used)'
)
def main(pdf_dir, keywords, collection, json_file, mongodb_uri, database):
    """
    Convert PDFs to MongoDB database or JSON file based on keyword patterns.
    
    Examples:
        # Output to MongoDB
        python main.py --pdf-dir ./pdfs --keywords "ID,Color,Model,Year" --collection cars
        
        # Output to JSON file
        python main.py --pdf-dir ./pdfs --keywords "ID,Color,Model,Year" --json-file output.json
    """
    # Parse keywords
    keyword_list = [k.strip() for k in keywords.split(',')]
    
    if not keyword_list:
        click.echo("Error: At least one keyword is required.", err=True)
        sys.exit(1)
    
    # Validate that either collection or json_file is provided
    if not collection and not json_file:
        click.echo("Error: Either --collection or --json-file must be provided.", err=True)
        sys.exit(1)
    
    if collection and json_file:
        click.echo("Error: Cannot use both --collection and --json-file. Choose one.", err=True)
        sys.exit(1)
    
    click.echo(f"Processing PDFs from: {pdf_dir}")
    click.echo(f"Keywords: {', '.join(keyword_list)}")
    
    if json_file:
        click.echo(f"Output: JSON file -> {json_file}")
        use_mongodb = False
    else:
        click.echo(f"Output: MongoDB collection -> {collection}")
        use_mongodb = True
    
    try:
        converter = PDFToDB(
            mongodb_uri=mongodb_uri if use_mongodb else None,
            database_name=database if use_mongodb else None,
            use_mongodb=use_mongodb
        )
        
        processed_count = converter.process_directory(
            pdf_directory=pdf_dir,
            keywords=keyword_list,
            collection_name=collection,
            json_file=json_file
        )
        
        click.echo(f"\n✓ Successfully processed {processed_count} records.")
        converter.close()
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

