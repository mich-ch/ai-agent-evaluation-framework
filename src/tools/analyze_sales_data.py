from src.config import MODEL_NAME
from src.prompts.analysis_prompt import DATA_ANALYSIS_PROMPT
from src.utils.openai_client import get_openai_client
from src.tracing.phoenix_setup import get_tracer # <--- NEW

client = get_openai_client()
tracer = get_tracer() # <--- NEW

@tracer.tool() # <--- NEW DECORATOR
def analyze_sales_data(prompt: str, data: str) -> str:
    """Tool: AI-powered sales data analysis."""
    formatted_prompt = DATA_ANALYSIS_PROMPT.format(data=data, prompt=prompt)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": formatted_prompt}],
    )
    
    analysis = response.choices[0].message.content
    return analysis if analysis else "No analysis could be generated"