import pandas as pd
import duckdb
from src.config import DATA_PATH, MODEL_NAME
from src.prompts.sql_generation_prompt import SQL_GENERATION_PROMPT
from src.utils.openai_client import get_openai_client
from src.tracing.phoenix_setup import get_tracer  # <--- NEW IMPORT

client = get_openai_client()
tracer = get_tracer()  # <--- GET TRACER

def generate_sql_query(prompt: str, columns: list, table_name: str) -> str:
    formatted_prompt = SQL_GENERATION_PROMPT.format(prompt=prompt, 
                                                    columns=columns, 
                                                    table_name=table_name)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": formatted_prompt}],
    )
    return response.choices[0].message.content

@tracer.tool()  # <--- NEW DECORATOR: Καταγράφει αυτή τη συνάρτηση στο Phoenix
def lookup_sales_data(prompt: str) -> str:
    """Tool: Implementation of sales data lookup from parquet file using SQL."""
    try:
        table_name = "sales"
        df = pd.read_parquet(DATA_PATH)
        duckdb.sql(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")

        # Start a sub-span for the SQL generation part (Optional but good for detail)
        with tracer.start_as_current_span("generate_sql_query") as span:
            sql_query = generate_sql_query(prompt, list(df.columns), table_name)
            span.set_attribute("sql.query", sql_query) # Log the generated SQL

        sql_query = sql_query.strip().replace("sql", "").replace("```", "").strip()
        
        result = duckdb.sql(sql_query).df()
        return result.to_string()
    except Exception as e:
        return f"Error accessing data: {str(e)}"