+"""
+Genomic Variant Database Querier
+CSE 310 - SQL Relational Databases Module
+
+This program creates and manages a SQLite database for storing and querying
+genomic variant data, including genes, variants, samples, and their relationships.
+Perfect for bioinformatics applications and understanding genetic mutations.
+
+Author: Tayler Hickman
+Date: November 2025
+"""
+
+import sqlite3
+import os
+
+# Database configuration
+DB_NAME = "genomic_variants.db"
+
+
+def create_connection():
+    """
+    Create a database connection to the SQLite database.
+    
+    Returns:
+        conn: Connection object or None
+    """
+    try:
+        conn = sqlite3.connect(DB_NAME)
+        print(f"✓ Connected to database: {DB_NAME}")
+        return conn
+    except sqlite3.Error as e:
+        print(f"✗ Error connecting to database: {e}")
+        return None
+
+
+def create_tables(conn):
+    """
+    Create all necessary tables in the database.
+    Tables: genes, variants, samples, sample_variants
+    """
+    try:
+        cursor = conn.cursor()
+        
+        # Table 1: genes
+        cursor.execute("""
+            CREATE TABLE IF NOT EXISTS genes (
+                gene_id INTEGER PRIMARY KEY AUTOINCREMENT,
+                gene_name TEXT UNIQUE NOT NULL,
+                chromosome TEXT,
+                function TEXT
+            )
+        """)
+        print("✓ Created table: genes")
+        
+        # Table 2: variants
+        cursor.execute("""
+            CREATE TABLE IF NOT EXISTS variants (
+                variant_id INTEGER PRIMARY KEY AUTOINCREMENT,
+                gene_id INTEGER NOT NULL,
+                variant_name TEXT UNIQUE NOT NULL,
+                position INTEGER,
+                mutation_type TEXT,
+                clinical_significance TEXT,
+                FOREIGN KEY (gene_id) REFERENCES genes(gene_id)
+            )
+        """)
+        print("✓ Created table: variants")
+        
+        # Table 3: samples
+        cursor.execute("""
+            CREATE TABLE IF NOT EXISTS samples (
+                sample_id INTEGER PRIMARY KEY AUTOINCREMENT,
+                patient_id TEXT NOT NULL,
+                tissue_type TEXT,
+                collection_date DATE
+            )
+        """)
+        print("✓ Created table: samples")
+        
+        # Table 4: sample_variants (junction table)
+        cursor.execute("""
+            CREATE TABLE IF NOT EXISTS sample_variants (
+                id INTEGER PRIMARY KEY AUTOINCREMENT,
+                sample_id INTEGER NOT NULL,
+                variant_id INTEGER NOT NULL,
+                allele_frequency REAL,
+                FOREIGN KEY (sample_id) REFERENCES samples(sample_id),
+                FOREIGN KEY (variant_id) REFERENCES variants(variant_id)
+            )
+        """)
+        print("✓ Created table: sample_variants")
+        
+        conn.commit()
+        print("\n✓ All tables created successfully!\n")
+        
+    except sqlite3.Error as e:
+        print(f"✗ Error creating tables: {e}")
+
+
+def main():
+    conn = create_connection()
+    if not conn:
+        return
+    create_tables(conn)
+    conn.close()
+
+
+if __name__ == "__main__":
+    main()