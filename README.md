# 🤖 AI Agent Evaluation & Observability Framework

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green)
![DuckDB](https://img.shields.io/badge/Database-DuckDB-yellow)
![Arize Phoenix](https://img.shields.io/badge/Observability-Phoenix-orange)

## 📋 Overview

This project implements a modular **AI Agent** capable of performing complex data analysis tasks by orchestrating multiple tools. The system utilizes a **Router-Tool architecture** to intelligently query databases, perform quantitative analysis, and generate data visualizations based on natural language prompts.

Unlike simple scripts, this project is structured as a production-ready application with a strong focus on **Software Engineering principles** (Separation of Concerns) and **LLM Observability** (using Arize Phoenix for tracing and evaluation).

## 🚀 Key Features

* **Intelligent Routing:** A central router that interprets user intent and dispatches tasks to the appropriate tools.
* **Text-to-SQL Engine:** Automatically converts natural language questions into SQL queries using **DuckDB** for high-performance local analytics.
* **Data Analysis & Reasoning:** Performs qualitative analysis on retrieved data using LLM reasoning capabilities.
* **Dynamic Visualization:** Generates and executes Python code to create charts (Bar, Line, etc.) on the fly.
* **Tracing & Observability:** Integrated with **Arize Phoenix** to trace agent execution paths, debug tool calls, and evaluate performance.



## 🏗️ Agent Architecture

The agent uses a Router-based architecture to handle complex data tasks:

```mermaid
graph TD
    A[👤 User Query] -->|Input| B{🧠 Central Router}
    
    B -->|Need Data?| C[🗄️ SQL Tool (DuckDB)]
    B -->|Need Analysis?| D[📊 Analysis Tool]
    B -->|Need Chart?| E[📈 Visualization Tool]
    
    C -->|Raw Data| B
    D -->|Insights| B
    E -->|Python Code| B
    
    B -->|Synthesis| F[📝 Final Response]

