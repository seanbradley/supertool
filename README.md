# SUPERTOOL

## OVERVIEW

Supertool is a simple multi-actor AI agentic workflow between a human, Claude 
(Anthropic's AI Assistant) and ChatGPT (OpenAI's AI Assistant).

Via leveraging a Persona based prompt engineering technique, Claude serves as a 
senior full stack software engineer and OpenAI serves as a senior QA engineer. 
Together they collaborate to refactor and review the user's untested Python code.

User input is hardcoded in the main.py...but you an easily adjust for leveraging 
input via the CLI.

## WORKFLOW

Presently, this workflow is a Directed Acyclic Graph (DAG) or state machine between 
a human user, Claude, and ChatGPT.

1. A user inputs a USER PROMPT of untested Python code
2. Claude refactors the code in accord with best practice (algorighmic efficiency, 
cyclomatic complexity, PEP8, etc.)
3. ChatGPT reviews the refactor and either accepts or rejects the refactored code.

## TODO

Implement LangGraph, CrewAI, or similar.

## LICENSE (MIT)

Copyright (c) 2024 by Sean Bradley. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


