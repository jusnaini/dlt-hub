# Demo: Ingesting REST API Data into DuckDB with dlt

This demo walks through the minimal steps to load data from a REST API and ingest into DuckDB using [dlt](https://dlthub.com/).


We’ll use **fake JSON** data from [JSONPlaceholder](https://jsonplaceholder.typicode.com/) to demonstrate the basics:

1. Install dlt
2. Initialize a new project
3. Create and run a pipeline
4. Inspect data with Streamlit
5. Add a primary key manually
6. Apply simple filtering and transformations

👉 The goal is to show **just the essentials** of data loading and ingestion from an API source to DuckDB.

📖 Reference pipeline: [REST API Walkthrough](https://dlthub.com/docs/walkthroughs/create-a-pipeline)

## 🔧 Installation & Project Setup
```bash
# Install dlt
pip install dlt

# Initialize a new project with REST API source and DuckDB destination
dlt init rest_api duckdb

# Install dependencies for DuckDB
pip install -r requirements.txt
```

**Project structure**

After running `dlt init`, you’ll see:

```Plain Text
rest_api_pipeline.py
requirements.txt
.dlt/
    config.toml
    secrets.toml
```
- `rest_api_pipeline.py` → Main script defining your data pipeline
- `requirements.txt` → Lists required Python dependencies
- `.dlt/` → Stores project configuration
- `config.toml` → General project settings
- `secrets.toml` → API keys, tokens, and other secrets

## 🚀 Create & Run the Pipeline

Modify `rest_api_pipeline.py`:

```python
import dlt
from dlt.sources.rest_api import rest_api_source 

restapi_source = rest_api_source({
    "client": {"base_url": "https://jsonplaceholder.typicode.com/"},
    "resources": ["users", "posts", "comments"]
})

pipeline = dlt.pipeline(
    pipeline_name="rest_api_minimal",
    destination="duckdb",
    dataset_name="rest_api_data",
)

if __name__ == "__main__":
    pipeline.run(restapi_source)
```


Run the pipeline:

```bash
python rest_api_pipeline.py
```

## 📊 Inspect Data with Streamlit

Install and launch Streamlit:

```bash
pip install streamlit

dlt pipeline rest_api_minimal show
```


You’ll see 3 tables created in DuckDB:

- `users`

- `posts`

- `comments`

## 🔑 Manually Add Primary Keys

DuckDB doesn’t infer primary keys automatically. You can add them manually:

```python
if __name__ == "__main__":
    pipeline.run(restapi_source)

    with pipeline.sql_client() as conn:
        conn.execute("""
            ALTER TABLE rest_api_data.users 
            ADD CONSTRAINT users_pk PRIMARY KEY (id)
        """)

```

⚠️ If a `.duckdb` file already exists, delete it first to avoid conflicts.

## 🛠️ Data Filtering & Transformation

To apply transformations before ingestion, create `rest_api_pipeline_with_tx.py` (optional to create new script):

```python
import dlt
from dlt.sources.rest_api import rest_api_source 

def lowercase_email(record):
    record["email"] = record["email"].lower()
    return record

restapi_source = rest_api_source({
    "client": {"base_url": "https://jsonplaceholder.typicode.com/"},
    "resources": [
        {
            "name": "users",
            "processing_steps": [
                {"filter": lambda x: x["id"] % 2 != 0},   # keep odd IDs only
                {"map": lowercase_email}                  # lowercase emails
            ]
        },
        "posts",
        "comments"
    ]
})

pipeline = dlt.pipeline(
    pipeline_name="rest_api_minimal",
    destination="duckdb",
    dataset_name="rest_api_data",
)

if __name__ == "__main__":
    pipeline.run(restapi_source)
```

📚 References
- [dlt](https://dlthub.com/)
- [Building a pipeline](https://dlthub.com/docs/build-a-pipeline-tutorial)
- [REST API source](https://dlthub.com/docs/dlt-ecosystem/verified-sources/rest_api/)
- [dlt + Streamlit](https://dlthub.com/docs/general-usage/dataset-access/streamlit)