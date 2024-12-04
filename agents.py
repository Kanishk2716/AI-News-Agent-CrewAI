from crewai import Agent , LLM
from tools import tool
import litellm
import os

from dotenv import load_dotenv
load_dotenv()


# Configure LiteLLM - use environment variables or direct configuration
litellm.set_verbose = True
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

# Create LLM
llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

news_researcher = Agent(
    role = "Senior Researcher",
    goal = "Uncover ground breaking technologies in {topic}" ,
    verbose = True ,
    memory = True ,
    backstory = (
        "Driven of curiosity, you,re at the forefront of"
        "innovation, eager to   explore and share knowledge that could change"
        "the world"
    ),
    tools = [tool],
    llm = llm ,
    allow_delegation = True
)

# Creating Writer agent with custom tools responsible in writing news blog

news_writer = Agent(
    role = "Writer",
    goal = "Narrate compelling tech stories about {topic}" ,
    verbose = True ,
    memory = True ,
    backstory = (
        "With a flair for simplifying complex topics, you craft"
        "engaging narratives that captivate and educate, bringing new"
        "discoveries to light in an accessible manner"
    ),
    tools = [tool],
    llm = llm ,
    allow_delegation = False
)