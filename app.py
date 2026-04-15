import streamlit as st
from openai import OpenAI
import base64
import numpy as np
import pandas as pd

# 1. 页面全局配置
st.set_page_config(page_title="拓扑One智能体", page_icon="♾️", layout="wide")

# ==========================================
# 客户端初始化 (移至前端以便全局调用)
# ==========================================
# DeepSeek 客户端（用于回答数学问题）
client = OpenAI(
    api_key=st.secrets["DEEPSEEK_KEY"], 
    base_url="https://api.deepseek.com"
)

# ==========================================
# 侧边栏：资源导航与 LaTeX 识别工具
# ==========================================
with st.sidebar:
    st.title("♾️ 拓扑One")
    st.markdown("面向数学与统计学专业的深度学习辅助系统")
    st.divider()
    
    # 模块：常见应用导航
    st.subheader("🚀 常见应用导航")
    st.markdown("[📚 CNKI知网 (文献检索)](https://www.cnki.net)")
    st.markdown("[📐 中国数学会 (学术动态)](https://www.cms.org.cn)")
    st.markdown("[🌐 中国大学MOOC (在线课程)](https://www.icourse163.org)")
    st.markdown("[📊 数学建模网 (CUMCM资源)](http://www.mcm.edu.cn)")
    st.markdown("[🏫 学科网 (教学资源)](https://www.zxxk.com)")
    
    st.divider()
    
    # 模块：核心功能
    st.subheader("💡 核心功能")
    st.markdown("- 📦 **课程与教材库**")
    
    # 功能 A：LaTeX识别
    with st.expander("∑ LaTeX公式识别 (点击上传图片)"):
        zhipu_api_key = st.secrets["ZHIPU_KEY"]
        uploaded_image = st.file_uploader("支持截图或拍照上传", type=["png", "jpg", "jpeg"], key="sidebar_latex")
        
        if uploaded_image is not None:
            st.image(uploaded_image, caption="待识别公式预览") 
            if st.button("✨ 开启真实识别"):
                with st.spinner("正在解析图片..."):
                    try:
                        img_data = uploaded_image.getvalue()
                        base64_image = base64.b64encode(img_data).decode('utf-8')
                        vision_client = OpenAI(
                            api_key=zhipu_api_key,
                            base_url="https://open.bigmodel.cn/api/paas/v4/"
                        )
                        response = vision_client.chat.completions.create(
                            model="glm-4v",
                            messages=[{
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "提取图片中的全部数学公式并转换为LaTeX代码。仅输出代码。"},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]
                            }]
                        )
                        st.code(response.choices[0].message.content, language="latex")
                    except:
                        st.error("识别出错，请检查配置。")
    
    st.divider()
    st.caption("让科研更高效，让学习更快乐！")

# ==========================================
# 主页面：三标签页架构
# ==========================================
st.title("♾️ 拓扑One - 智慧数学学伴AI")
st.caption("专为数学专业大学生打造的自适应学业规划与科研辅助系统。")

tab_chat, tab_visual, tab_course = st.tabs(["💬 智能问答", "📈 模型可视化演示", "📚 课程资源检索库"])

# ------------------------------------------
# 标签页 1：智能问答
# ------------------------------------------
with tab_chat:
    st.markdown("### 💡 快捷提问")
    if "quick_prompt" not in st.session_state:
        st.session_state.quick_prompt = None

    col1, col2 = st.columns(2)
    
    # 左侧列：保留两个固定的快捷问题按钮
    with col1:
        if st.button("🔍 查询大二上学期《拓扑学》推荐教材", use_container_width=True):
            st.session_state.quick_prompt = "请帮我查询数学专业大二上学期《拓扑学》的经典推荐教材，并给出学习该课程的重点建议。"
        if st.button("🧠 从《数学分析》到《实变函数》怎么过渡？", use_container_width=True):
            st.session_state.quick_prompt = "请从核心思想的角度，讲解如何从数学分析平滑过渡到实变函数学习。"
    
    # 右侧列：替换为可以自主输入概念的展开框
    with col2:
        with st.expander("📚 讲解基本概念"):
            concept_query = st.text_input("输入你想了解的概念", placeholder="输入后回车...")
            if concept_query:
                with st.spinner("正在查询专业解析..."):
                    try:
                        sde_response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[
                                {
                                    "role": "system", 
                                    "content": "你是一个名为'拓扑One'的专业数学AI学伴。请直接给出严谨、通俗的解答，绝对不要使用任何诸如'作为一名数学教授'或'我很乐意为你解答'之类的开场白废话。重要格式要求：所有数学公式必须严格使用 Markdown 的 LaTeX 语法，行内公式用单个 $ 包裹（例如 $f(x)$），独立公式用双 $$ 包裹。绝对禁止使用 \\( \\) 或 \\[ \\] 格式输出公式。"
                                },
                                {
                                    "role": "user", 
                                    "content": f"请详细且精炼地讲解这个概念：{concept_query}"
                                }
                            ]
                        )
                        st.info(sde_response.choices[0].message.content)
                    except:
                        st.error("解析失败，请检查 API 配置。")

    st.divider()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "你好！我是你的**拓扑One**导师。无论是拓扑学难点、随机过程公式，还是科研论文排版，我都能为你提供专业的指导。今天想探讨什么？"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("请输入您的数学问题或科研需求...")
    prompt = st.session_state.quick_prompt or user_input

    if prompt:
        st.session_state.quick_prompt = None
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("系统正在进行多维度逻辑推理..."):
                try:
                    # 在主对话中也加入严格格式要求的 System Prompt
                    strict_messages = [
                        {
                            "role": "system",
                            "content": "你是一个名为'拓扑One'的专业数学AI学伴。请直接给出严谨、通俗的解答，不要说废话。数学公式必须严格使用 Markdown 的 LaTeX 语法，行内公式用单个 $ 包裹，独立公式用双 $$ 包裹。绝对禁止使用 \\( \\) 或 \\[ \\] 格式。"
                        }
                    ] + st.session_state.messages
                    
                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=strict_messages,
                        stream=False
                    )
                    ai_answer = response.choices[0].message.content
                    st.markdown(ai_answer)
                    st.session_state.messages.append({"role": "assistant", "content": ai_answer})
                except:
                    st.error("对话失败。请检查 API 配置。")

# ------------------------------------------
# 标签页 2：模型可视化
# ------------------------------------------
with tab_visual:
    st.markdown("### 📊 数学模型动态可视化")
    col_v1, col_v2 = st.columns([1, 2])
    with col_v1:
        st.markdown("#### 参数配置")
        model_type = st.selectbox("请选择随机过程模型", [
            "标准布朗运动 (Standard Brownian Motion)",
            "几何布朗运动 (Geometric Brownian Motion)"
        ])
        n_steps = st.slider("模拟步数", 100, 3000, 1000)
        dt = 1.0 / n_steps

        if model_type == "标准布朗运动 (Standard Brownian Motion)":
            st.latex(r"W_t = \sum_{i=1}^{n} \Delta X_i")
            if st.button("🎲 生成布朗运动路径"):
                with col_v2:
                    steps = np.random.choice([-1, 1], size=n_steps)
                    path = np.cumsum(steps)
                    st.line_chart(pd.DataFrame(path, columns=["位置 (W_t)"]))
                        
        elif model_type == "几何布朗运动 (Geometric Brownian Motion)":
            mu, sigma = st.number_input("漂移率 μ", 0.05), st.number_input("波动率 σ", 0.20)
            st.latex(rf"dS_t = {mu:.2f} S_t dt + {sigma:.2f} S_t dW_t")
            if st.button("📈 生成资产价格路径"):
                with col_v2:
                    t = np.linspace(0, 1, n_steps)
                    W = np.cumsum(np.random.standard_normal(size=n_steps)) * np.sqrt(dt) 
                    S = 100 * np.exp((mu - 0.5 * sigma**2) * t + sigma * W) 
                    st.line_chart(pd.DataFrame(S, columns=["资产价格 (S_t)"]))

# ------------------------------------------
# 标签页 3：数据库检索
# ------------------------------------------
with tab_course:
    st.markdown("### 📚 结构化课程与教材数据库")
    try:
        @st.cache_data
        def load_data():
            return pd.read_csv("课程信息表 (1).csv", encoding="utf-8")
        df = load_data()
        c1, c2 = st.columns(2)
        with c1:
            selected_term = st.selectbox("📅 按学期筛选", ["全部"] + list(df["学年"].unique()))
        with c2:
            query = st.text_input("🔍 搜索课程名称")
        
        filtered = df.copy()
        if selected_term != "全部": filtered = filtered[filtered["学年"] == selected_term]
        if query: filtered = filtered[filtered["课程名称"].str.contains(query, na=False, case=False)]
        
        st.dataframe(filtered, use_container_width=True, hide_index=True, column_config={
            "购买链接": st.column_config.LinkColumn("教材链接"),
            "网课链接（推荐）": st.column_config.LinkColumn("网课资源")
        })
    except:
        st.error("数据文件加载失败，请确保 '课程信息表 (1).csv' 已上传至仓库。")
