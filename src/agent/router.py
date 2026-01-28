import json
from src.config import MODEL_NAME
from src.utils.openai_client import get_openai_client
from src.tools.tool_registry import TOOLS_SCHEMA, TOOL_IMPLEMENTATIONS
from src.agent.system_prompt import SYSTEM_PROMPT
from src.tracing.phoenix_setup import get_tracer

client = get_openai_client()
tracer = get_tracer()

def handle_tool_calls(tool_calls, messages):
    """Executes the tools requested by the LLM."""
    for tool_call in tool_calls:   
        function_name = tool_call.function.name
        
        if function_name not in TOOL_IMPLEMENTATIONS:
            continue

        function_to_call = TOOL_IMPLEMENTATIONS[function_name]
        function_args = json.loads(tool_call.function.arguments)
        
        print(f"--> Executing Tool: {function_name}") 
        
        # Το Tool Span δημιουργείται αυτόματα από τον decorator @tracer.tool μέσα στη συνάρτηση
        result = function_to_call(**function_args)
        
        messages.append({
            "role": "tool", 
            "content": str(result), 
            "tool_call_id": tool_call.id
        })
    return messages

def run_agent(user_input):
    """Main entry point for the agent with Tracing."""
    
    # Ξεκινάμε το βασικό Span (Το "κουτί" που περιέχει όλη τη συνομιλία)
    with tracer.start_as_current_span("Agent_Workflow_Run") as span:
        span.set_attribute("user.input", user_input)
        
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.append({"role": "user", "content": user_input})

        while True:
            print("Thinking...") 
            
            # OpenAI Call (Καταγράφεται αυτόματα από το instrumentor)
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=TOOLS_SCHEMA,
            )
            
            message = response.choices[0].message
            messages.append(message)
            
            if message.tool_calls:
                # Αν έχουμε tool calls, τα καταγράφουμε
                messages = handle_tool_calls(message.tool_calls, messages)
            else:
                span.set_attribute("agent.final_output", message.content)
                return message.content