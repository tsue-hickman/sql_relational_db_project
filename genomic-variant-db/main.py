"""
Genomic Variant Database Querier
CSE 310 - SQL Relational Databases Module

This program creates and manages a SQLite database for storing and querying
genomic variant data, including genes, variants, samples, and their relationships.

Author: Tayler Hickman
Date: November 2025
"""

import sqlite3
import os

# Database configuration
DB_NAME = "genomic_variants.db"


def create_connection():
    """Create a database connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        print(f"Connected to database: {DB_NAME}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def create_tables(conn):
    """Create all necessary tables: genes, variants, samples, sample_variants"""
    try:
        cursor = conn.cursor()

        # Table: genes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS genes (
                gene_id INTEGER PRIMARY KEY AUTOINCREMENT,
                gene_name TEXT UNIQUE NOT NULL,
                chromosome TEXT,
                function TEXT
            )
        """)
        print("Created table: genes")

        # Table: variants
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS variants (
                variant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                gene_id INTEGER NOT NULL,
                variant_name TEXT UNIQUE NOT NULL,
                position INTEGER,
                mutation_type TEXT,
                clinical_significance TEXT,
                FOREIGN KEY (gene_id) REFERENCES genes(gene_id)
            )
        """)
        print("Created table: variants")

        # Table: samples
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS samples (
                sample_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                tissue_type TEXT,
                collection_date DATE
            )
        """)
        print("Created table: samples")

        # Table: sample_variants (junction)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sample_variants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sample_id INTEGER NOT NULL,
                variant_id INTEGER NOT NULL,
                allele_frequency REAL,
                FOREIGN KEY (sample_id) REFERENCES samples(sample_id),
                FOREIGN KEY (variant_id) REFERENCES variants(variant_id)
            )
        """)
        print("Created table: sample_variants")

        conn.commit()
        print("\nAll tables created successfully!\n")

    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")


def main():
    conn = create_connection()
    if conn:
        create_tables(conn)
        conn.close()


if __name__ == "__main__":
    main()
def insert_gene(conn, gene_name, chromosome, function):
    """INSERT a new gene into the database."""
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO genes (gene_name, chromosome, function) VALUES (?, ?, ?)"
        cursor.execute(sql, (gene_name, chromosome, function))
        conn.commit()
        print(f"Inserted gene: {gene_name} (ID: {cursor.lastrowid})")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"Gene '{gene_name}' already exists")
        return None
    except sqlite3.Error as e:
        print(f"Error inserting gene: {e}")
        return None


def insert_variant(conn, gene_id, variant_name, position, mutation_type, clinical_significance):
    """INSERT a new variant into the database."""
    try:
        cursor = conn.cursor()
        sql = """INSERT INTO variants 
             (gene_id, variant_name, position, mutation_type, clinical_significance) 
             VALUES (?, ?, ?, ?, ?)"""
        cursor.execute(sql, (gene_id, variant_name, position, mutation_type, clinical_significance))
        conn.commit()
        print(f"Inserted variant: {variant_name} (ID: {cursor.lastrowid})")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"Variant '{variant_name}' already exists")
        return None
    except sqlite3.Error as e:
        print(f"Error inserting variant: {e}")
        return None


def insert_sample(conn, patient_id, tissue_type, collection_date):
    """INSERT a new sample into the database."""
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO samples (patient_id, tissue_type, collection_date) VALUES (?, ?, ?)"
        cursor.execute(sql, (patient_id, tissue_type, collection_date))
        conn.commit()
        print(f"Inserted sample: {patient_id} - {tissue_type} (ID: {cursor.lastrowid})")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error inserting sample: {e}")
        return None


def link_sample_variant(conn, sample_id, variant_id, allele_frequency):
    """Link a sample to a variant."""
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO sample_variants (sample_id, variant_id, allele_frequency) VALUES (?, ?, ?)"
        cursor.execute(sql, (sample_id, variant_id, allele_frequency))
        conn.commit()
        print(f"Linked Sample {sample_id} to Variant {variant_id} (AF: {allele_frequency})")
    except sqlite3.Error as e:
        print(f"Error linking sample and variant: {e}")                    