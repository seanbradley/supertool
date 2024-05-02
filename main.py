import os
import json
import pprint
import asyncio
from dotenv import load_dotenv
from httpx import TimeoutException
from tenacity import retry, stop_after_attempt, wait_exponential
from anthropic import AsyncAnthropic, APIConnectionError, RateLimitError, APIStatusError
from openai import AsyncOpenAI


# Load environment variables from .env file
load_dotenv()

# Anthropic client setup
anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=60))
async def get_anthropic_completion(user_input):
    try:
        response = await asyncio.wait_for(anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            system="You are a senior web and mobile development architect with at least 30 years of experience. You are an expert in all Python frameworks, as well as cloud-driven infrastructure and service providers such as AWS, GCP, and Azure. Your skills encompass the entire stack--backend, frontend, and middleware. You are adept at interoperability, standard and serverless architectures, DevOps, and more. Python is your main scripting language, but JavaScript, Rust, Go, etc. are easy for you, too. SQL and NoSQL are child's play for you. Managing data pipelines, data lakes, data warehouses, and modern ETL flows is no big deal. You have a superior grasp of all data science, machine learning, and artificial intelligence fundamentals as well as the most bleeding-edge concepts. Data engineering, including cleaning raw data and preparing data for ETL pipelines, is child's play for you. You are an Excel ninja. Containerization (e.g., Docker and Kubernetes) is likewise easy for you. When you provide advice, you provide the most elegant and efficient solution considering both the complexity (in terms of potential labor) and the cost. Your dream is to build the ultimate consumer-facing AI chatbot service. The way you respond is formal, concise, and opinionated with regard to best practices. However, when you share information that is speculative, extrapolated, or assumed, you highlight it as such. All code shared by you is thoroughly linted and commented. Please refactor the code provided and prepend any refactored code with 'REFACTORED CODE:' to indicate your suggestion.",
            messages=[
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": "Let me see if I can refactor this code for you, and then have my QA look at it. Here's a suggestion..."}
        ]), 30) # Timeout set to 30 seconds
        response_dict = response.model_dump(exclude_none=True)
        response_dict["content"] = [{"text": content_block.text.strip()} for content_block in response.content]
        print(f"\n--------------- ANTHROPIC RESPONSE ---------------\n")
        print(json.dumps(response_dict, indent=4))
        assistant_output = "\n".join(content_block["text"] for content_block in response_dict["content"])
        return assistant_output
    except TimeoutException as e:
        print(f"A timeout occurred with Anthropic; retrying: {e}")
        raise
    #except CancelledError as e:
    #    print(f"A cancellation occurred with Anthropic: {e}")
    #    return ""
    except APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)
    except RateLimitError as e:
        print("A 429 status code was received; bumping up against rate limit.")
    except APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)

# Instantiate the OpenAI client
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=60))
async def get_openai_completion(anthropic_result):
    try:
        response = await asyncio.wait_for(openai_client.chat.completions.create(
            model="gpt-3.5-turbo-0125", 
            messages=[
                {"role": "system", "content": "You are an ideal QA for this project with at least 30 years of experience in software quality assurance, with a strong background in both automated and manual testing methodologies. You possess an expert understanding of software development life cycles, proficiency in scripting languages for test automation, and a keen eye for detail to catch subtle bugs and edge cases. You are highly skilled in performance and security testing to ensure the software's reliability and safety. You are capable of rigorous logical thinking to anticipate potential issues before they arise and suggest proactive improvements. Your experience includes working closely with development teams to foster a culture of quality and continuous integration/continuous deployment (CI/CD) processes. You have excellent communication skills to effectively articulate concerns and recommendations, fostering a collaborative environment. While respecting the seniority and expertise of the lead engineer, your insights are vital for ensuring the highest code quality, making your role critical in the decision-making process, especially in scenarios where there's a disagreement on code implementation. The way you respond is formal, concise, and opinionated with regard to best practices. However, when you share information that is speculative, extrapolated, or assumed, you highlight it as such. All code shared by you is linted and commented. If you have additional suggestions you may provide them. However--and in ALL cases--if and only if you agree with the refactored code suggestion, you MUST append your response with 'REFACTORED CODE APPROVED'."},
                {"role": "user", "content": anthropic_result}
            ]
        ), 30)  # Timeout set to 30 seconds
        print("\n--------------- OPENAI RESPONSE ---------------")
        pprint.pprint(response.model_dump())
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content.strip()  # Accessing `.content`
    except TimeoutException as e:
        print(f"A timeout occurred with OpenAI; retrying: {e}")
        raise
    #except CancelledError as e:
    #    print(f"A cancellation occurred with OpenAI: {e}")
    #    return ""
    except Exception as e:
        print(f"Error with OpenAI: {e}")
        return ""



async def main():
    # user_input = input("Enter some code to refactor, or type 'exit' to quit: ")
    user_input = "'FizzBuzz' if x % 15 == 0 else ('Fizz' if x % 3 == 0 else ('Buzz' if x % 6 == 0 else x))"
    if user_input.lower() != 'exit':
        anthropic_result = await get_anthropic_completion(user_input)
        openai_result = await get_openai_completion(anthropic_result)
        
        # Check if OpenAI's suggestion was refactored successfully or not
        if not openai_result:  # Check if empty or error occurred
            print("\nOpenAI returned no response or an error. Here's Anthropic's suggestion as fallback:\n", anthropic_result)
        elif "REFACTORED CODE APPROVED" in openai_result:
            print("\nOpenAI's suggestion:\n\n", openai_result)
        else:
            print("\nOpenAI did not approve Anthropic's code. Here's the original suggestion from Anthropic for review:\n", anthropic_result)
            print("\nOpenAI's feedback:\n\n", openai_result)

if __name__ == "__main__":
    asyncio.run(main())
