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
def update_variant_significance(conn, variant_id, new_significance):
    """UPDATE the clinical significance of a variant."""
    try:
        cursor = conn.cursor()
        sql = "UPDATE variants SET clinical_significance = ? WHERE variant_id = ?"
        cursor.execute(sql, (new_significance, variant_id))
        conn.commit()
        print(f"Updated Variant {variant_id} significance to: {new_significance}")
    except sqlite3.Error as e:
        print(f"Error updating variant: {e}")                   
def delete_sample(conn, sample_id):
    """DELETE a sample and its associated variant links."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sample_variants WHERE sample_id = ?", (sample_id,))
        cursor.execute("DELETE FROM samples WHERE sample_id = ?", (sample_id,))
        conn.commit()
        print(f"Deleted Sample {sample_id} and its associations")
    except sqlite3.Error as e:
        print(f"Error deleting sample: {e}")
def query_variants_by_gene(conn, gene_name):
    """SELECT all variants for a given gene using JOIN."""
    try:
        cursor = conn.cursor()
        sql = """
            SELECT v.variant_id, v.variant_name, v.position, v.mutation_type, v.clinical_significance
            FROM variants v
            JOIN genes g ON v.gene_id = g.gene_id
            WHERE g.gene_name = ?
        """
        cursor.execute(sql, (gene_name,))
        results = cursor.fetchall()

        if results:
            print(f"\n=== Variants in Gene: {gene_name} ===")
            for row in results:
                print(f"  ID: {row[0]} | Name: {row[1]} | Position: {row[2]} | "
                      f"Type: {row[3]} | Significance: {row[4]}")
            print(f"Total: {len(results)} variants\n")
        else:
            print(f"No variants found for gene: {gene_name}\n")
        return results
    except sqlite3.Error as e:
        print(f"Error querying variants: {e}")
        return []


def query_pathogenic_variants(conn):
    """SELECT all pathogenic or likely pathogenic variants."""
    try:
        cursor = conn.cursor()
        sql = """
            SELECT v.variant_id, g.gene_name, v.variant_name, v.clinical_significance
            FROM variants v
            JOIN genes g ON v.gene_id = g.gene_id
            WHERE v.clinical_significance IN ('Pathogenic', 'Likely Pathogenic')
        """
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            print(f"\n=== Pathogenic Variants ===")
            for row in results:
                print(f"  Variant ID: {row[0]} | Gene: {row[1]} | Name: {row[2]} | "
                      f"Significance: {row[3]}")
            print(f"Total: {len(results)} pathogenic variants\n")
        else:
            print("No pathogenic variants found\n")
        return results
    except sqlite3.Error as e:
        print(f"Error querying pathogenic variants: {e}")
        return []


def query_samples_with_variant(conn, variant_name):
    """SELECT all samples containing a specific variant."""
    try:
        cursor = conn.cursor()
        sql = """
            SELECT s.sample_id, s.patient_id, s.tissue_type, sv.allele_frequency
            FROM samples s
            JOIN sample_variants sv ON s.sample_id = sv.sample_id
            JOIN variants v ON sv.variant_id = v.variant_id
            WHERE v.variant_name = ?
        """
        cursor.execute(sql, (variant_name,))
        results = cursor.fetchall()

        if results:
            print(f"\n=== Samples Containing Variant: {variant_name} ===")
            for row in results:
                print(f"  Sample ID: {row[0]} | Patient: {row[1]} | Tissue: {row[2]} | "
                      f"Allele Freq: {row[3]:.2f}")
            print(f"Total: {len(results)} samples\n")
        else:
            print(f"No samples found with variant: {variant_name}\n")
        return results
    except sqlite3.Error as e:
        print(f"Error querying samples: {e}")
        return []
from datetime import datetime


def aggregate_stats(conn):
    """Use COUNT, AVG, and JOINs to show database statistics."""
    try:
        cursor = conn.cursor()
        print("\n=== DATABASE STATISTICS ===")

        # Variants per gene (COUNT + JOIN)
        cursor.execute("""
            SELECT g.gene_name, COUNT(v.variant_id) as variant_count
            FROM genes g
            LEFT JOIN variants v ON g.gene_id = v.gene_id
            GROUP BY g.gene_name
            ORDER BY variant_count DESC
        """)
        print("\nVariants per Gene:")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} variants")

        # Average allele frequency per variant (AVG + JOIN)
        cursor.execute("""
            SELECT v.variant_name, AVG(sv.allele_frequency) as avg_freq
            FROM variants v
            JOIN sample_variants sv ON v.variant_id = sv.variant_id
            GROUP BY v.variant_name
        """)
        print("\nAverage Allele Frequency by Variant:")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]:.3f}")

        # Total counts
        cursor.execute("SELECT COUNT(*) FROM samples")
        total_samples = cursor.fetchone()[0]
        print(f"\nTotal Samples in Database: {total_samples}")

        cursor.execute("SELECT COUNT(*) FROM genes")
        total_genes = cursor.fetchone()[0]
        print(f"Total Genes in Database: {total_genes}")

        print("\n" + "="*50 + "\n")

    except sqlite3.Error as e:
        print(f"Error calculating statistics: {e}")


def populate_sample_data(conn):
    """Populate database with realistic sample data."""
    print("\n=== POPULATING DATABASE WITH SAMPLE DATA ===\n")

    # Insert genes
    brca1_id = insert_gene(conn, "BRCA1", "17", "DNA repair, tumor suppressor")
    tp53_id = insert_gene(conn, "TP53", "17", "Cell cycle regulation, apoptosis")
    egfr_id = insert_gene(conn, "EGFR", "7", "Cell growth and division")
    brca2_id = insert_gene(conn, "BRCA2", "13", "DNA repair, homologous recombination")

    print()

    # Insert variants
    if brca1_id:
        v1 = insert_variant(conn, brca1_id, "rs80357906", 43091434, "SNP", "Pathogenic")
        v2 = insert_variant(conn, brca1_id, "rs80357914", 43094692, "Deletion", "Pathogenic")

    if tp53_id:
        v3 = insert_variant(conn, tp53_id, "rs28934576", 7577548, "SNP", "Likely Pathogenic")
        v4 = insert_variant(conn, tp53_id, "rs11540652", 7579472, "SNP", "Benign")

    if egfr_id:
        v5 = insert_variant(conn, egfr_id, "rs121434568", 55259515, "Insertion", "Pathogenic")
        v6 = insert_variant(conn, egfr_id, "rs1050171", 55249063, "SNP", "Uncertain")

    if brca2_id:
        v7 = insert_variant(conn, brca2_id, "rs80359550", 32929232, "SNP", "Pathogenic")

    print()

    # Insert samples
    s1 = insert_sample(conn, "PATIENT001", "Blood", "2024-01-15")
    s2 = insert_sample(conn, "PATIENT001", "Tumor", "2024-01-16")
    s3 = insert_sample(conn, "PATIENT002", "Blood", "2024-02-10")
    s4 = insert_sample(conn, "PATIENT003", "Saliva", "2024-03-05")
    s5 = insert_sample(conn, "PATIENT004", "Blood", "2024-04-12")

    print()

    # Link samples to variants
    if s1 and v1: link_sample_variant(conn, s1, v1, 0.48)
    if s2 and v1: link_sample_variant(conn, s2, v1, 0.92)
    if s2 and v3: link_sample_variant(conn, s2, v3, 0.85)
    if s3 and v4: link_sample_variant(conn, s3, v4, 0.51)
    if s3 and v6: link_sample_variant(conn, s3, v6, 0.48)
    if s4 and v5: link_sample_variant(conn, s4, v5, 0.47)
    if s5 and v7: link_sample_variant(conn, s5, v7, 0.50)

    print("\nSample data populated successfully!\n")


def display_menu():
    """Display the interactive menu."""
    print("\n" + "="*60)
    print("      GENOMIC VARIANT DATABASE QUERIER")
    print("="*60)
    print("1.  Insert new gene")
    print("2.  Insert new variant")
    print("3.  Insert new sample")
    print("4.  Link sample to variant")
    print("5.  Update variant clinical significance")
    print("6.  Delete a sample")
    print("7.  Query: Show all variants in a gene")
    print("8.  Query: Show all pathogenic variants")
    print("9.  Query: Show samples containing a specific variant")
    print("10. Show database statistics (AGGREGATE functions)")
    print("11. Populate database with sample data")
    print("0.  Exit")
    print("="*60)


def main():
    print("\n" + "="*60)
    print("  GENOMIC VARIANT DATABASE QUERIER")
    print("  CSE 310 - SQL Relational Databases Project")
    print("="*60 + "\n")

    conn = create_connection()
    if not conn:
        return

    create_tables(conn)

    while True:
        display_menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            gene_name = input("Enter gene name (e.g., BRCA1): ").strip()
            chromosome = input("Enter chromosome (e.g., 17): ").strip()
            function = input("Enter gene function: ").strip()
            insert_gene(conn, gene_name, chromosome, function)

        elif choice == "2":
            gene_id = int(input("Enter gene ID: "))
            variant_name = input("Enter variant name (e.g., rs123456): ").strip()
            position = int(input("Enter chromosome position: "))
            mutation_type = input("Enter mutation type (SNP/Insertion/Deletion): ").strip()
            significance = input("Enter clinical significance: ").strip()
            insert_variant(conn, gene_id, variant_name, position, mutation_type, significance)

        elif choice == "3":
            patient_id = input("Enter patient ID: ").strip()
            tissue_type = input("Enter tissue type: ").strip()
            collection_date = input("Enter collection date (YYYY-MM-DD): ").strip()
            insert_sample(conn, patient_id, tissue_type, collection_date)

        elif choice == "4":
            sample_id = int(input("Enter sample ID: "))
            variant_id = int(input("Enter variant ID: "))
            allele_freq = float(input("Enter allele frequency (0.0-1.0): "))
            link_sample_variant(conn, sample_id, variant_id, allele_freq)

        elif choice == "5":
            variant_id = int(input("Enter variant ID to update: "))
            new_sig = input("Enter new clinical significance: ").strip()
            update_variant_significance(conn, variant_id, new_sig)

        elif choice == "6":
            sample_id = int(input("Enter sample ID to delete: "))
            delete_sample(conn, sample_id)

        elif choice == "7":
            gene_name = input("Enter gene name: ").strip()
            query_variants_by_gene(conn, gene_name)

        elif choice == "8":
            query_pathogenic_variants(conn)

        elif choice == "9":
            variant_name = input("Enter variant name: ").strip()
            query_samples_with_variant(conn, variant_name)

        elif choice == "10":
            aggregate_stats(conn)

        elif choice == "11":
            populate_sample_data(conn)

        elif choice == "0":
            print("\nClosing database connection...")
            conn.close()
            print("Goodbye!\n")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()