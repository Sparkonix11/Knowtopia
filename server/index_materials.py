#!/usr/bin/env python3
"""
Command-line script to index all materials in the RAG system
This script is used for initial setup or bulk reindexing of materials
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from flask import Flask

# Load environment variables
load_dotenv()

def create_app():
    """Create a Flask application context for database operations"""
    from factory import create_app as factory_create_app
    app = factory_create_app()
    return app

def index_all_materials():
    """Index all materials in the database into the RAG system"""
    # Import here to avoid circular imports
    from services.rag.indexer import MaterialIndexer
    
    print("Starting indexing of all materials...")
    indexer = MaterialIndexer()
    results = indexer.index_all_materials()
    
    print(f"Indexing complete!")
    print(f"Successfully indexed: {results['success']} materials")
    print(f"Failed to index: {results['failed']} materials")
    print(f"Total materials processed: {results['total']} materials")
    
    return results

def index_material(material_id):
    """Index a specific material by ID"""
    # Import here to avoid circular imports
    from services.rag.indexer import MaterialIndexer
    from models.material import Material
    
    print(f"Looking up material ID: {material_id}...")
    
    app = create_app()
    with app.app_context():
        material = Material.query.get(material_id)
        if not material:
            print(f"Error: Material with ID {material_id} not found.")
            return False
        
        print(f"Found material: {material.name} (ID: {material_id})")
        print(f"Starting indexing process...")
        
        indexer = MaterialIndexer()
        success = indexer.reindex_material(material_id)
        
        if success:
            print(f"Successfully indexed material: {material.name} (ID: {material_id})")
        else:
            print(f"Failed to index material: {material.name} (ID: {material_id})")
        
        return success

def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Index materials in the RAG system')
    parser.add_argument('--material-id', type=int, help='ID of a specific material to index')
    parser.add_argument('--all', action='store_true', help='Index all materials')
    args = parser.parse_args()
    
    if not args.all and args.material_id is None:
        parser.print_help()
        return
    
    app = create_app()
    with app.app_context():
        if args.all:
            print("Indexing all materials...")
            index_all_materials()
        elif args.material_id is not None:
            print(f"Indexing material ID: {args.material_id}")
            index_material(args.material_id)

if __name__ == "__main__":
    main()