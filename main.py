from pathlib import Path
from datetime import datetime

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser

from schemas.candidate import Candidate
from extractor.candidate import prompt_template

def main():
    llm = init_chat_model("gemini-2.0-flash-001", model_provider="google_vertexai")

    inpath = Path('./db')
    file_name = Path('resume_example.txt')
    text = ''
    with open(inpath / file_name, 'r') as infile:
        for line in infile:
            text += line

    # Parser
    parser = PydanticOutputParser(pydantic_object=Candidate)

    # Prompt
    prompt = prompt_template.partial(format_instructions=parser.get_format_instructions())

    chain = prompt | llm | parser
    response = chain.invoke({"text": text})
    print(response)

main()