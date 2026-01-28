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

## 🏗️ Project Architecture

The codebase follows a modular structure to ensure scalability and maintainability:

```text
├── data/                   # Dataset files (Parquet format)
├── src/
│   ├── agent/              # Core Agent Logic & Router (The "Brain")
│   ├── tools/              # Tool definitions (The "Hands")
│   │   ├── lookup_sales.py     # SQL Tool
│   │   ├── analyze_data.py     # Analysis Tool
│   │   └── visualize.py        # Charting Tool
│   ├── prompts/            # Centralized Prompt Templates (Separation of Logic/Prompts)
│   ├── tracing/            # Phoenix Observability instrumentation
│   └── utils/              # Helper functions (API Clients, Config)
├── notebooks/              # Experimental Lab Notebooks
├── tests/                  # Unit tests
└── requirements.txt        # Project dependencies