from src.config import MODEL_NAME
from src.prompts.chart_config_prompt import CHART_CONFIGURATION_PROMPT
from src.prompts.chart_code_prompt import CREATE_CHART_PROMPT
from src.tools.visualization_config import VisualizationConfig
from src.utils.openai_client import get_openai_client
from src.tracing.phoenix_setup import get_tracer # <--- NEW

client = get_openai_client()
tracer = get_tracer() # <--- NEW

# Χρησιμοποιούμε @tracer.chain αντί για tool εδώ, γιατί είναι βοηθητική συνάρτηση
@tracer.start_as_current_span("extract_chart_config") 
def extract_chart_config(data: str, visualization_goal: str) -> dict:
    formatted_prompt = CHART_CONFIGURATION_PROMPT.format(data=data,
                                                         visualization_goal=visualization_goal)
    
    response = client.beta.chat.completions.parse(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": formatted_prompt}],
        response_format=VisualizationConfig,
    )
    
    try:
        content = response.choices[0].message.parsed
        return {
            "chart_type": content.chart_type,
            "x_axis": content.x_axis,
            "y_axis": content.y_axis,
            "title": content.title,
            "data": data
        }
    except Exception:
        return {
            "chart_type": "line", "x_axis": "date", "y_axis": "value",
            "title": visualization_goal, "data": data
        }

@tracer.start_as_current_span("create_chart_code")
def create_chart(config: dict) -> str:
    formatted_prompt = CREATE_CHART_PROMPT.format(config=config)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": formatted_prompt}],
    )
    code = response.choices[0].message.content
    code = code.replace("python", "").replace("```", "").strip()
    return code

@tracer.tool() # <--- MAIN TOOL DECORATOR
def generate_visualization(data: str, visualization_goal: str) -> str:
    """Main Tool Function: Generates visualization code."""
    config = extract_chart_config(data, visualization_goal)
    code = create_chart(config)
    return code