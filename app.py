import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="もしもAI（リアル未来予測）", page_icon="🔮")
st.title("🔮もしもAI（リアル未来予測）")
st.write("あなたの『もしも〜したら？』に対して、AIが現実的な未来を予測します。")

query = st.text_input("もしも○○したら？（例：もし今日勉強をサボったら？）")

if st.button("未来を予測する"):
    generator = pipeline("text-generation", model="elyza/ELYZA-japanese-Llama-2-7b")
    prompt = f"{query} この状況の未来を、現実的に日本語で予測してください。"
    result = generator(prompt, max_new_tokens=120, do_sample=True, temperature=0.7)
    st.markdown("### ✨ AIの未来予測 ✨")
    st.write(result[0]['generated_text'])
