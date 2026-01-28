from pydantic import BaseModel, Field

class VisualizationConfig(BaseModel):
    chart_type: str = Field(..., description="Type of chart to generate (e.g., bar, line)")
    x_axis: str = Field(..., description="Name of the x-axis column")
    y_axis: str = Field(..., description="Name of the y-axis column")
    title: str = Field(..., description="Title of the chart")