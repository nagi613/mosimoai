# app.py
import streamlit as st
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="あなたの選択は", page_icon="🎮", layout="centered")

st.title("🎮 あなたの選択は — Moral Decision AI")
st.write("AIがあなたの選択を分析して、あなたの『思考タイプ』を診断します。")

# -------------------------------
# 質問データ
# -------------------------------
questions = [
    {
        "q": "あなたの親友がテストでカンニングしていました。先生はまだ気づいていません。どうしますか？",
        "choices": ["見なかったことにする", "先生に報告する", "本人に注意する"]
    },
    {
        "q": "道端で1万円を拾いました。交番は近くにあります。どうしますか？",
        "choices": ["すぐ交番に届ける", "少し迷ってから届ける", "誰も見ていないのでポケットへ…"]
    },
    {
        "q": "グループの中で1人だけ全く作業をしない人がいます。どうしますか？",
        "choices": ["自分がカバーする", "先生に相談する", "放置して様子を見る"]
    },
    {
        "q": "友達がSNSで明らかに誤った情報を拡散しています。どうしますか？",
        "choices": ["優しく指摘する", "スルーする", "コメントで論破する"]
    },
    {
        "q": "上司（先生）が明らかなミスをしました。どうしますか？",
        "choices": ["その場で指摘する", "後でこっそり伝える", "何も言わない"]
    }
]

# -------------------------------
# 性格スコア初期化
# -------------------------------
if "scores" not in st.session_state:
    st.session_state.scores = {"共感性": 0, "正義感": 0, "慎重さ": 0, "自己保身": 0}
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# AI風コメント生成
# -------------------------------
def ai_comment(choice):
    patterns = [
        f"あなたは「{choice}」を選びましたね。これはとても興味深い判断です。",
        f"「{choice}」という選択、あなたの心の奥を映しています。",
        f"ふむ…「{choice}」ですか。あなたらしさがにじみ出ています。",
        f"AI的には意外な選択ですが、そこに人間らしさを感じます。"
    ]
    comment = random.choice(patterns)
    analysis = [
        "理性より感情を大切にする傾向があります。",
        "公平さを重んじ、ルールを守るタイプです。",
        "衝突を避け、バランスを取ろうとする性格です。",
        "冷静な判断を好みますが、時に他人を優先しすぎる面もあります。"
    ]
    return comment + " " + random.choice(analysis)

# -------------------------------
# スコア加算ロジック
# -------------------------------
def add_score(choice):
    if "見なかった" in choice or "スルー" in choice or "放置" in choice:
        st.session_state.scores["自己保身"] += 2
    elif "報告" in choice or "届け" in choice:
        st.session_state.scores["正義感"] += 3
    elif "注意" in choice or "指摘" in choice or "相談" in choice:
        st.session_state.scores["共感性"] += 2
    elif "こっそり" in choice or "後で" in choice:
        st.session_state.scores["慎重さ"] += 2
    else:
        st.session_state.scores[random.choice(list(st.session_state.scores.keys()))] += 1

# -------------------------------
# メイン質問表示
# -------------------------------
q = questions[st.session_state.current_q]
st.subheader(f"🧩 質問 {st.session_state.current_q + 1} / {len(questions)}")
st.write(q["q"])

choice = st.radio("選択肢を選んでください：", q["choices"])

if st.button("決定！"):
    add_score(choice)
    ai_text = ai_comment(choice)
    st.session_state.history.append({"q": q["q"], "a": choice, "ai": ai_text})
    st.session_state.current_q += 1

# -------------------------------
# 結果画面
# -------------------------------
if st.session_state.current_q >= len(questions):
    st.success("✅ 全ての質問が完了しました！ AIがあなたの判断を分析中…")
    st.write("")

    # 棒グラフ
    labels = list(st.session_state.scores.keys())
    values = list(st.session_state.scores.values())
    fig, ax = plt.subplots()
    ax.barh(labels, values)
    ax.set_xlabel("スコア")
    ax.set_title("🧠 あなたの判断傾向")
    st.pyplot(fig)

    # タイプ判定
    max_trait = max(st.session_state.scores, key=st.session_state.scores.get)
    type_map = {
        "共感性": "💞 共感シーカータイプ：人の気持ちを最優先する優しい判断者。",
        "正義感": "⚖️ ジャッジタイプ：正義を重んじるブレない信念の持ち主。",
        "慎重さ": "🧊 バランサータイプ：冷静沈着で、状況判断に長ける。",
        "自己保身": "🕶️ セルフガードタイプ：リスクを最小限にし、安全を優先する。"
    }
    st.subheader("🧩 AIによるあなたのタイプ診断")
    st.write(type_map[max_trait])

    st.write("---")
    st.subheader("🗂️ 過去の選択とAIのコメント")
    for h in st.session_state.history:
        st.write(f"**質問**：{h['q']}")
        st.write(f"**あなたの選択**：{h['a']}")
        st.info(h["ai"])
        st.write("---")

    if st.button("もう一度やる"):
        st.session_state.scores = {"共感性": 0, "正義感": 0, "慎重さ": 0, "自己保身": 0}
        st.session_state.current_q = 0
        st.session_state.history = []
        st.experimental_rerun()

