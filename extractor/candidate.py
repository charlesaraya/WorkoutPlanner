from typing import Optional

from langchain_core.prompts import ChatPromptTemplate

#prompt_template = ChatPromptTemplate.from_template(
""""You are an expert extraction algorithm specialised in resumes.
Extract all relevant candidate information from the resume {text}

If you do not know the value of an attribute asked to extract, return None for the attribute's value.
"""
#)
prompt_template = ChatPromptTemplate.from_template(
    """"
    You are an expert extraction algorithm specialised in resumes.
    Extract all relevant candidate information from the following resume:
    {text}

    If you do not know the value of an attribute asked to extract, return None for the attribute's value.
    Wrap the output in `json` tags
    {format_instructions}
    """
)