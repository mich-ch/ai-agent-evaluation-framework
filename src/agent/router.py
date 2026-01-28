import json
from src.config import MODEL_NAME
from src.utils.openai_client import get_openai_client
from src.tools.tool_registry import TOOLS_SCHEMA, TOOL_IMPLEMENTATIONS
from src.agent.system_prompt import SYSTEM_PROMPT

client = get_openai_client()

def handle_tool_calls(tool_calls, messages):
    """Executes the tools requested by the LLM."""
    for tool_call in tool_calls:   
        function_name = tool_call.function.name
        
        if function_name not in TOOL_IMPLEMENTATIONS:
            print(f"Error: Tool {function_name} not found!")
            continue

        function_to_call = TOOL_IMPLEMENTATIONS[function_name]
        
        try:
            function_args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError:
            print(f"Error decoding arguments for {function_name}")
            continue
        
        print(f"--> Executing Tool: {function_name}") # Debugging print
        
        # Execute tool
        result = function_to_call(**function_args)
        
        messages.append({
            "role": "tool", 
            "content": str(result), 
            "tool_call_id": tool_call.id
        })
    return messages

def run_agent(user_input):
    """Main entry point for the agent."""
    
    # Initialize messages
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add user message
    messages.append({"role": "user", "content": user_input})

    while True:
        print("Thinking...") # User feedback
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS_SCHEMA,
        )
        
        message = response.choices[0].message
        messages.append(message)
        
        # If the model wants to call tools
        if message.tool_calls:
            messages = handle_tool_calls(message.tool_calls, messages)
        else:
            # Final answer
            return message.content