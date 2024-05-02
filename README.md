# SUPERTOOL

## OVERVIEW

Supertool is a simple multi-actor AI agentic workflow between Claude (Anthropic's 
AI Assistant) and ChatGPT (OpenAI's AI Assistant).

Via leveraging a Persona based prompt engineering technique, Claude serves as a 
senior full stack software engineer and OpenAI serves as a senior QA engineer. 
Together they collaborate to build, test, and deploy any best-in-class Python 
application.

## WORKFLOW

Presently, this workflow is a Directed Acyclic Graph (DAG) or state machine between 
a human user, Claude, and ChatGPT.

1. A user inputs a USER PROMPT of untested Python code
2. Claude refactors the code in accord with best practice (algorighmic efficiency, 
cyclomatic complexity, PEP8, etc.)
3. ChatGPT reviews the refactor and either accepts or refects the refactored code.

## TODO

Implement LangGraph or other 

## LICENSE

This project is proprietary and not licensable.