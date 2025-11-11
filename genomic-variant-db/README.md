# Genomic Variant Database Querier

**CSE 310 – SQL Relational Databases Project**

## Overview

As a software engineering major interested in **bioinformatics** and **health informatics**, I wanted hands-on experience designing and using relational databases to manage real-world biological data. Understanding schema design, SQL query writing, and Python-database integration is essential for working with genomic data, electronic health records (EHRs), or medical research datasets.

This **Genomic Variant Database Querier** stores and manages:

- Genes
- Genetic variants (mutations)
- Patient tissue samples
- Many-to-many relationships between samples and variants

Users can **insert**, **update**, **delete**, and **query** data interactively. The system supports complex SQL operations such as `JOIN`s and aggregate functions (`COUNT`, `AVG`) — skills directly applicable to **precision medicine**, where a patient’s unique mutations guide treatment.

This project helped me master:

- Normalized relational schema design
- Full CRUD operations in SQL
- Python application integration with SQLite
- Realistic bioinformatics data modeling

[Software Demo Video](http://youtube.link.goes.here)

---

## Relational Database

The database file is **`genomic_variants.db`** and contains **four normalized tables**:

### 1. `genes` – Gene metadata

| Column       | Type    | Constraints                      |
| ------------ | ------- | -------------------------------- |
| `gene_id`    | INTEGER | PRIMARY KEY, AUTOINCREMENT       |
| `gene_name`  | TEXT    | UNIQUE, NOT NULL (e.g., "BRCA1") |
| `chromosome` | TEXT    | e.g., "17", "X"                  |
| `function`   | TEXT    | Gene biological role             |

### 2. `variants` – Genetic mutations

| Column                  | Type    | Constraints                                              |
| ----------------------- | ------- | -------------------------------------------------------- |
| `variant_id`            | INTEGER | PRIMARY KEY, AUTOINCREMENT                               |
| `gene_id`               | INTEGER | FOREIGN KEY → `genes(gene_id)`                           |
| `variant_name`          | TEXT    | UNIQUE, NOT NULL (e.g., "rs80357906")                    |
| `position`              | INTEGER | Chromosomal position                                     |
| `mutation_type`         | TEXT    | "SNP", "Insertion", "Deletion"                           |
| `clinical_significance` | TEXT    | "Pathogenic", "Likely Pathogenic", "Benign", "Uncertain" |

### 3. `samples` – Patient tissue samples

| Column            | Type    | Constraints                      |
| ----------------- | ------- | -------------------------------- |
| `sample_id`       | INTEGER | PRIMARY KEY, AUTOINCREMENT       |
| `patient_id`      | TEXT    | NOT NULL (e.g., "PATIENT001")    |
| `tissue_type`     | TEXT    | "Blood", "Tumor", "Saliva", etc. |
| `collection_date` | DATE    | YYYY-MM-DD format                |

### 4. `sample_variants` – Junction table (many-to-many)

| Column             | Type    | Constraints                                |
| ------------------ | ------- | ------------------------------------------ |
| `id`               | INTEGER | PRIMARY KEY, AUTOINCREMENT                 |
| `sample_id`        | INTEGER | FOREIGN KEY → `samples(sample_id)`         |
| `variant_id`       | INTEGER | FOREIGN KEY → `variants(variant_id)`       |
| `allele_frequency` | REAL    | 0.0 – 1.0 (fraction of cells with variant) |

> **Normalization**: Eliminates redundancy and ensures referential integrity.  
> **Many-to-many**: One sample can have many variants; one variant can appear in many samples.

---

## Development Environment

- **IDE**: Visual Studio Code (with Python extension)
- **Language**: Python 3.x
- **Core Libraries**:
  - `sqlite3` – Built-in SQLite interface
  - `datetime` – Date handling
  - `os` – File system checks
- **Database Engine**: **SQLite** – Lightweight, serverless, ideal for prototyping and education

---

## Useful Websites & Resources

- [SQLite Tutorial](https://www.sqlitetutorial.net/) – Full SQL syntax & SQLite guide
- [Python sqlite3 Documentation](https://docs.python.org/3/library/sqlite3.html) – Official API reference
- [W3Schools SQL](https://www.w3schools.com/sql/) – Quick SQL command lookup
- [Database Normalization](https://www.guru99.com/database-normalization.html) – Schema best practices
- [SQL JOIN Explained](https://www.sqlitetutorial.net/sqlite-join/) – Visual JOIN examples
- [NCBI dbSNP](https://www.ncbi.nlm.nih.gov/snp/) – Real variant database (project inspiration)
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) – Clinical significance data source
- **Claude AI** – Helpful for code structure and SQL query ideas
- **Grok AI** – Assisted with commit message organization and code splitting

---

## Future Work

| Feature                  | Description                                                        |
| ------------------------ | ------------------------------------------------------------------ |
| **VCF Import**           | Parse standard Variant Call Format files to auto-load variants     |
| **Date Range Queries**   | Filter samples by collection period (e.g., Q1 2024)                |
| **Top Variant Report**   | Show most frequent variants across all samples                     |
| **Export to CSV/PDF**    | Generate patient summary reports                                   |
| **User Authentication**  | Add login system for multi-user access                             |
| **Web Interface**        | Build Flask/Django frontend                                        |
| **API Integration**      | Pull live data from ClinVar or gnomAD                              |
| **Data Visualization**   | Plot variant density per chromosome or allele frequency histograms |
| **Statistical Analysis** | Chi-square tests for variant-outcome associations                  |

---

**Author**: Tayler Hickman  
**Date**: November 2025  
**Course**: CSE 310 – SQL Relational Databases

---
