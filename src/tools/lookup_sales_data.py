import pandas as pd
import duckdb
from src.config import DATA_PATH, MODEL_NAME
from src.prompts.sql_generation_prompt import SQL_GENERATION_PROMPT
from src.utils.openai_client import get_openai_client

client = get_openai_client()

def generate_sql_query(prompt: str, columns: list, table_name: str) -> str:
    """Helper function: Asks LLM to convert text to SQL."""
    formatted_prompt = SQL_GENERATION_PROMPT.format(prompt=prompt, 
                                                    columns=columns, 
                                                    table_name=table_name)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": formatted_prompt}],
    )
    return response.choices[0].message.content

def lookup_sales_data(prompt: str) -> str:
    """Tool: Implementation of sales data lookup from parquet file using SQL."""
    try:
        table_name = "sales"
        
        # 1. Read the parquet file
        # Note: In a real production env, we wouldn't load this every time, 
        # but for this demo/lab architecture it's fine.
        df = pd.read_parquet(DATA_PATH)
        
        # Create virtual table in DuckDB
        duckdb.sql(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")

        # 2. Generate the SQL code
        sql_query = generate_sql_query(prompt, list(df.columns), table_name)
        
        # Clean the response (remove markdown code blocks if present)
        sql_query = sql_query.strip().replace("sql", "").replace("```", "").strip()
        
        # 3. Execute the SQL query
        result = duckdb.sql(sql_query).df()
        
        return result.to_string()
    except Exception as e:
        return f"Error accessing data: {str(e)}"