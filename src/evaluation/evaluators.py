import pandas as pd
import re
from phoenix.evals import llm_classify, OpenAIModel
from src.config import MODEL_NAME

# Μοντέλο "Δικαστής"
eval_model = OpenAIModel(model="gpt-4o")

# --- Prompts ---
SQL_EVAL_PROMPT = """
You are tasked with determining if the SQL generated appropriately answers the instruction.

Data:
- [Instruction]: {question}
- [Generated Query]: {sql_code}

Evaluation:
Your response must be exactly "correct" or "incorrect".
Assume the database schema exists as described in the prompt.
"""

CLARITY_EVAL_PROMPT = """
Evaluate the clarity of the answer.
Query: {query}
Answer: {response}

Response must be exactly "clear" or "unclear".
"""

# --- Helper Function ---
def extract_code_block(text: str, lang: str = "python") -> str:
    """Βρίσκει κώδικα ανάμεσα σε ```...```"""
    pattern = rf"```{lang}\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    # Αν δεν έχει backticks, ίσως είναι σκέτος κώδικας
    if "def " in text or "import " in text or "SELECT " in text:
        return text
    return ""

# --- Evaluators ---

def evaluate_code_runnability(output: dict, input_val: dict) -> int:
    """
    Ελέγχει αν ο Python κώδικας που παρήχθη τρέχει χωρίς λάθη.
    """
    generated_code = output.get("generated_python_code")
    
    if not generated_code:
        # Αν η ερώτηση απαιτούσε γράφημα αλλά δεν παράχθηκε κώδικας -> Fail
        if "chart" in input_val.get("question", "").lower():
            return 0
        return 1 # Αν δεν χρειαζόταν κώδικας, όλα καλά.

    # Καθαρισμός του κώδικα
    clean_code = generated_code.replace("python", "").replace("```", "").strip()
    
    try:
        # Δοκιμαστική εκτέλεση σε απομονωμένο περιβάλλον
        exec_globals = {}
        exec(clean_code, exec_globals)
        return 1 # Success
    except Exception as e:
        print(f"Code Eval Failed: {e}")
        return 0 # Fail

def evaluate_sql_correctness(output: dict, input_val: dict) -> int:
    """
    Χρησιμοποιεί LLM για να κρίνει αν το SQL query βγάζει νόημα.
    """
    sql_code = output.get("generated_sql")
    question = input_val.get("question")
    
    if not sql_code:
        # Αν η ερώτηση δεν απαιτούσε SQL, το αγνοούμε
        return 1 
        
    df = pd.DataFrame({
        "question": [question],
        "sql_code": [sql_code]
    })
    
    try:
        eval_result = llm_classify(
            dataframe=df,
            template=SQL_EVAL_PROMPT,
            rails=["correct", "incorrect"],
            model=eval_model,
            provide_explanation=False
        )
        return 1 if eval_result['label'][0] == 'correct' else 0
    except Exception as e:
        print(f"SQL Eval Error: {e}")
        return 0

def evaluate_clarity(output: dict, input_val: dict) -> int:
    """
    Ελέγχει αν η τελική απάντηση είναι σαφής.
    """
    response_text = output.get("final_response")
    
    if not response_text:
        return 0

    df = pd.DataFrame({
        "query": [input_val.get("question")],
        "response": [response_text]
    })
    
    eval_result = llm_classify(
        dataframe=df,
        template=CLARITY_EVAL_PROMPT,
        rails=["clear", "unclear"],
        model=eval_model,
        provide_explanation=False
    )
    
    return 1 if eval_result['label'][0] == 'clear' else 0