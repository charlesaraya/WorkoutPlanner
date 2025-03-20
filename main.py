from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

def main():
    model = init_chat_model("gemini-2.0-flash-001", model_provider="google_vertexai")

    prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")
    prompt = prompt_template.invoke({"topic": "cats"})

    prompt_template = ChatPromptTemplate([
        ("system", "You are a comedian whose jokes create uncomfortable situations"),
        ("user", "Tell me a joke about {topic}")
    ])
    prompt = prompt_template.invoke({"topic": "cats"})

    prompt_template = ChatPromptTemplate([
        ("system", "You are a comedian with a dark humour style"),
        MessagesPlaceholder("msgs")
    ])

    prompt = prompt_template.invoke({"msgs": [HumanMessage(content="Tell me a joke about climate change!")]})

    response = model.invoke(prompt)
    print(response.content)

main()