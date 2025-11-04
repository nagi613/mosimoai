import streamlit as st
from transformers import pipeline
import random

st.title("🔮もしもAI（IFシミュレーター）")
st.write("あなたの『もしも〜したら？』の未来を、AIが予測します。")

# 入力欄
user_input = st.text_input("もしも○○したら？（例：もし今日勉強をサボったら？）")

# モデル読み込み（最初に一度だけ）
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")

generator = load_model()

# ボタン押下時
if st.button("予測する！"):
    if user_input.strip() == "":
        st.warning("『もしも〜』の文章を入力してください。")
    else:
        with st.spinner("AIが未来を予測中...🔮"):
            result = generator(
                user_input,
                max_length=60,
                num_return_sequences=1,
                temperature=0.8,
                top_p=0.9,
                do_sample=True
            )[0]['generated_text']

        # GPT-2は英語モデルなので、日本語風に翻訳っぽく加工
        st.subheader("✨ AIの未来予測 ✨")
        st.write(result)
        st.caption(random.choice([
            "※この未来はAIの想像です。",
            "※信じるか信じないかは、あなた次第。",
            "※AIがあなたの運命を見守っています。"
        ]))
