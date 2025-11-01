import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

st.title("LLMアプリ（初心者版）")
st.write("① 専門家を選ぶ → ② 質問を書く → ③ 送信ボタン")

expert = st.radio("どんな専門家に聞きますか？", ["旅行プランナー", "栄養士"])
user_text = st.text_input("質問を入力してください")

def system_message(expert_name: str) -> str:
    if expert_name == "旅行プランナー":
        return "あなたは旅行プランナーです。日本語で旅行の提案をしてください。"
    return "あなたは栄養士です。日本語で健康的な食事のアドバイスをしてください。"

def ask_llm(text: str, expert_name: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "⚠️ OPENAI_API_KEY が見つかりません。.env を確認してください。"
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7, openai_api_key=api_key)
    messages = [
        SystemMessage(content=system_message(expert_name)),
        HumanMessage(content=text),
    ]
    result = llm(messages)
    return result.content

if st.button("送信"):
    if user_text.strip() == "":
        st.warning("質問を入力してください。")
    else:
        st.write("AIが考え中…")
        answer = ask_llm(user_text, expert)
        st.subheader("AIからの回答")
        st.write(answer)
