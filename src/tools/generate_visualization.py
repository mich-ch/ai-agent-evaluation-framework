from src.config import MODEL_NAME
from src.prompts.chart_config_prompt import CHART_CONFIGURATION_PROMPT
from src.prompts.chart_code_prompt import CREATE_CHART_PROMPT
from src.tools.visualization_config import VisualizationConfig
from src.utils.openai_client import get_openai_client

client = get_openai_client()

def extract_chart_config(data: str, visualization_goal: str) -> dict:
    """Step 1: Decide what chart to build."""
    formatted_prompt = CHART_CONFIGURATION_PROMPT.format(data=data,
                                                         visualization_goal=visualization_goal)
    
    # Use structured output parsing (new OpenAI feature)
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
        # Fallback if parsing fails
        return {
            "chart_type": "line", 
            "x_axis": "date",
            "y_axis": "value",
            "title": visualization_goal,
            "data": data
        }

def create_chart(config: dict) -> str:
    """Step 2: Write the actual Python code."""
    formatted_prompt = CREATE_CHART_PROMPT.format(config=config)
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": formatted_prompt}],
    )
    
    code = response.choices[0].message.content
    # Clean up code blocks
    code = code.replace("python", "").replace("```", "").strip()
    return code

def generate_visualization(data: str, visualization_goal: str) -> str:
    """Main Tool Function: Generates visualization code."""
    config = extract_chart_config(data, visualization_goal)
    code = create_chart(config)
    return code