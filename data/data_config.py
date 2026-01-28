TEST_DATASET = [
    {
        "question": "What was the most popular product SKU?",
        "expected_tool": "lookup_sales_data"
    },
    {
        "question": "Which store had the highest sales volume?",
        "expected_tool": "lookup_sales_data"
    },
    {
        "question": "Create a bar chart showing total sales by store",
        "expected_tool": "generate_visualization"
    },
    {
        "question": "What percentage of items were sold on promotion?",
        "expected_tool": "lookup_sales_data"
    },
    {
        "question": "Analyze the sales trends for store 1320",
        "expected_tool": "analyze_sales_data"
    }
]