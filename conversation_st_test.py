import streamlit as st
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

st.title("ChatGPT Clone")

if not (api_key := st.text_input("Enter your `OPENAI_API_KEY`", type="password")):
    st.stop()

if not api_key.startswith("sk-"):
    st.error("Invalid API key. Must start with `sk-`.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()


def format_history(messages):
    history = ""
    for msg in messages:
        if msg["role"] == "user":
            history += f"Human: {msg['content']}\n"

        if msg["role"] == "ai":
            history += f"AI: {msg['content']}\n"

    return history


conversation = ConversationChain(
    # llm=ChatGoogleGenerativeAI(model="gemini-pro"),
    llm=ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key),
    memory=st.session_state.memory,
)

# render past messages first
for message in st.session_state.messages:
    # message schema: {role: user/ai, content: actual message}
    with st.chat_message(message["role"]):
        st.write(message["content"])

# next message
if next_message := st.chat_input():
    # add user message to session
    st.session_state.messages.append({"role": "user", "content": next_message})
    with st.chat_message("user"):
        st.write(next_message)

    # generate llm response
    response = conversation.invoke(input=next_message)["response"]

    # add llm response to session
    st.session_state.messages.append({"role": "ai", "content": response})
    with st.chat_message("ai"):
        st.write(response)
