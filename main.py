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
    required=True,
    help='MongoDB collection name to store the data'
)
@click.option(
    '--mongodb-uri',
    default=None,
    help='MongoDB connection URI (defaults to MONGODB_URI env var)'
)
@click.option(
    '--database',
    default=None,
    help='MongoDB database name (defaults to DATABASE_NAME env var)'
)
def main(pdf_dir, keywords, collection, mongodb_uri, database):
    """
    Convert PDFs to MongoDB database based on keyword patterns.
    
    Example:
        python main.py --pdf-dir ./pdfs --keywords "ID,Color,Model,Year" --collection cars
    """
    # Parse keywords
    keyword_list = [k.strip() for k in keywords.split(',')]
    
    if not keyword_list:
        click.echo("Error: At least one keyword is required.", err=True)
        sys.exit(1)
    
    click.echo(f"Processing PDFs from: {pdf_dir}")
    click.echo(f"Keywords: {', '.join(keyword_list)}")
    click.echo(f"Collection: {collection}")
    
    try:
        converter = PDFToDB(mongodb_uri=mongodb_uri, database_name=database)
        
        inserted_count = converter.process_directory(
            pdf_directory=pdf_dir,
            keywords=keyword_list,
            collection_name=collection
        )
        
        click.echo(f"\n✓ Successfully processed {inserted_count} records.")
        converter.close()
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

