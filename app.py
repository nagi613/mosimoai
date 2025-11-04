import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import random

st.title("🔮もしもAI（IFシミュレーター）")
st.write("あなたの『もしも〜したら？』の未来を、AIが日本語で予測します。")

# 入力欄
user_input = st.text_input("もしも○○したら？（例：もし今日勉強をサボったら？）")

# モデル読み込み（最初だけ）
@st.cache_resource
def load_model():
    model_name = "rinna/japanese-gpt2-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)

generator = load_model()

# ボタン押下時
if st.button("予測する！"):
    if user_input.strip() == "":
        st.warning("『もしも〜』の文章を入力してください。")
    else:
        with st.spinner("AIが未来を予測中...🔮"):
            result = generator(
                user_input,
                max_length=80,
                do_sample=True,
                temperature=0.9,
                top_p=0.95,
                num_return_sequences=1
            )[0]['generated_text']

        st.subheader("✨ AIの未来予測 ✨")
        st.write(result)
        st.caption(random.choice([
            "※この未来はAIの想像です。",
            "※信じるか信じないかは、あなた次第。",
            "※AIがあなたの運命を見守っています。"
        ]))
