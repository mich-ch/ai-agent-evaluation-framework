# 🤖 AI Agent Evaluation & Observability Framework

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green)
![DuckDB](https://img.shields.io/badge/Database-DuckDB-yellow)
![Arize Phoenix](https://img.shields.io/badge/Observability-Phoenix-orange)

## 📋 Overview

A comprehensive framework for building and **evaluating** AI Agents. This project implements a sophisticated agent capable of performing Data Analysis by orchestrating specialized tools (SQL, Python Code, Reasoning). 

Crucially, it includes a robust **Evaluation Pipeline** using "LLM-as-a-Judge" techniques to measure performance, correctness, and safety, visualized through **Arize Phoenix**.

## 🏗️ Agent Architecture

The agent uses a Router-based architecture to handle complex data tasks:

graph TD
    A[👤 User Query] -->|Input| B{🧠 Central Router}
    
    B -->|Need Data?| C["🗄️ SQL Tool (DuckDB)"]
    B -->|Need Analysis?| D["📊 Analysis Tool"]
    B -->|Need Chart?| E["📈 Visualization Tool"]
    
    C -->|Raw Data| B
    D -->|Insights| B
    E -->|Python Code| B
    
    B -->|Synthesis| F[📝 Final Response]