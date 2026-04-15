import streamlit as st
from openai import OpenAI
import base64
import numpy as np
import pandas as pd
import time

# 1. 页面全局配置
st.set_page_config(page_title="拓扑One智能体", page_icon="♾️", layout="wide")

# ==========================================
# 客户端初始化 (移至前端以便全局调用)
# ==========================================
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
    
    st.subheader("💡 核心功能")
    st.markdown("- 📦 **课程与教材库**")
    
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

    st.subheader("🚀 常见应用导航")
    st.markdown("[📚 CNKI知网 (文献检索)](https://www.cnki.net)")
    st.markdown("[📐 中国数学会 (学术动态)](https://www.cms.org.cn)")
    st.markdown("[🌐 中国大学MOOC (在线课程)](https://www.icourse163.org)")
    st.markdown("[📊 数学建模网 (CUMCM资源)](http://www.mcm.edu.cn)")
    st.markdown("[🏫 学科网 (教学资源)](https://www.zxxk.com)")
    
    st.divider()
    st.caption("让科研更高效，让学习更快乐！")

# ==========================================
# 主页面：海报与四标签页架构
# ==========================================
# 🌟 视觉增强：极简版 Apple Bento Box (纯标题，几何居中)
st.markdown("""
<style>
.bento-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, 160px); 
    gap: 16px;
    margin-bottom: 30px;
    margin-top: 20px;
}
.bento-box {
    background: #fbfbfd;
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    justify-content: center; /* 水平绝对居中 */
    align-items: center;     /* 垂直绝对居中 */
    flex-direction: column;
    border: 1px solid #e5e5ea;
    overflow: hidden;
    position: relative;
    text-align: center;
}
.bento-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}
.box-large {
    grid-column: span 2;
    grid-row: span 2;
    background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
}
.box-wide {
    grid-column: span 2;
    background: linear-gradient(135deg, #ffffff 0%, #f0f4f8 100%);
}
.bento-title {
    font-size: 22px; 
    font-weight: 700;
    color: #1d1d1f;
    margin: 0; /* 强制清空外边距以保证绝对居中 */
}
.large-title {
    font-size: 42px; 
    font-weight: 800;
    background: -webkit-linear-gradient(45deg, #0071e3, #42a1f5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0; /* 强制清空外边距以保证绝对居中 */
}
@keyframes spin3D {
    0% { transform: rotateY(0deg); }
    100% { transform: rotateY(360deg); }
}
.rotate-logo {
    display: inline-block;
    animation: spin3D 4s linear infinite;
    transform-style: preserve-3d;
}
</style>

<div class="bento-container">
    <div class="bento-box box-large">
        <div class="large-title"><span class="rotate-logo">♾️</span> 拓扑One</div>
    </div>
    <div class="bento-box box-wide">
        <div class="bento-title">∑ 多模态 LaTeX 极速识别</div>
    </div>
    <div class="bento-box">
        <div class="bento-title">📈 动态模型</div>
    </div>
    <div class="bento-box">
        <div class="bento-title">🏆 CUMCM</div>
    </div>
</div>
""", unsafe_allow_html=True)

tab_chat, tab_visual, tab_course, tab_solver = st.tabs(["💬 智能问答", "📈 模型可视化演示", "📚 课程资源检索库", "📸 AI识图解题"])

# ------------------------------------------
# 标签页 1：智能问答
# ------------------------------------------
with tab_chat:
    st.markdown("### 💡 快捷提问")
    if "quick_prompt" not in st.session_state:
        st.session_state.quick_prompt = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 查询高等代数课程推荐教材", use_container_width=True):
            st.session_state.quick_prompt = "请帮我查询数学专业高等代数的经典推荐教材，并给出学习该课程的重点建议。"
        if st.button("🧠 从《数学分析》到《实变函数》怎么过渡？", use_container_width=True):
            st.session_state.quick_prompt = "请从核心思想的角度，讲解如何从数学分析平滑过渡到实变函数学习。"
    
    with col2:
        if st.button("🏆 全国大学生数学建模竞赛(CUMCM)备考路线", use_container_width=True):
            st.session_state.quick_prompt = "请为数学专业的学生制定一份为期三个月的全国大学生数学建模竞赛（CUMCM）备考计划。要求：1. 分月细化任务（基础、进阶、模拟）；2. 列出核心算法模型；3. 公式使用 $ 渲染。"
        
        with st.expander("📚 讲解基本概念"):
            concept_query = st.text_input("输入你想了解的概念（如：伊藤引理）", placeholder="输入后回车...")
            if concept_query:
                with st.spinner("正在查询专业解析..."):
                    try:
                        sde_response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[
                                {
                                    "role": "system", 
                                    "content": "你是一个名为'拓扑One'的专业数学AI学伴。请直接给出严谨、通俗的解答，绝对不要说废话。数学公式必须严格使用 Markdown 的 LaTeX 语法，行内公式用单个 $ 包裹，独立公式用双 $$ 包裹。绝对禁止使用 \\( \\) 或 \\[ \\] 格式。"
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
                    strict_messages = [
                        {
                            "role": "system",
                            "content": "你是一个名为'拓扑One'的专业数学AI学伴。请直接给出严谨解答，不要说废话。数学公式必须严格使用 $ 包裹行内公式，$$ 包裹独立公式。绝对禁止使用 \\( 或 \\[。"
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

# ------------------------------------------
# 标签页 4：拍照搜题 (多模型联合接力解题)
# ------------------------------------------
with tab_solver:
    st.markdown("### 📸 拓扑One 核心矿山：多模型联合解题系统")
    
    if "solver_mode" not in st.session_state:
        st.session_state.solver_mode = None

    if st.session_state.solver_mode is None:
        st.info("👇 请先选择你要解答的题目大类，然后上传题目截图或拍照。")
        
        with st.container(border=True):
            st.markdown("#### 📐 微积分")
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("∫ 不定积分", use_container_width=True): st.session_state.solver_mode = "不定积分"
            if c2.button("∬ 二重积分", use_container_width=True): st.session_state.solver_mode = "二重积分"
            if c3.button("∂ 微分方程", use_container_width=True): st.session_state.solver_mode = "微分方程"
            if c4.button("lim 极限计算", use_container_width=True): st.session_state.solver_mode = "极限计算"

        with st.container(border=True):
            st.markdown("#### 🧮 线性代数")
            c5, c6, c7, c8 = st.columns(4)
            if c5.button("[A]ᵀ 矩阵转置", use_container_width=True): st.session_state.solver_mode = "矩阵转置"
            if c6.button("|A| 行列式", use_container_width=True): st.session_state.solver_mode = "行列式计算"
            if c7.button("R(A) 矩阵的秩", use_container_width=True): st.session_state.solver_mode = "矩阵的秩"
            if c8.button("λ 特征值与向量", use_container_width=True): st.session_state.solver_mode = "特征值与特征向量"

    else:
        col_back, _ = st.columns([1, 4])
        if col_back.button("⬅️ 返回更换题型"):
            st.session_state.solver_mode = None
            st.rerun()
            
        st.markdown(f"#### 当前选定题型：**{st.session_state.solver_mode}**")
        st.caption("采用 VLM视觉感知 + LLM深度推理 双引擎。请选择题目图片上传。")
        
        solve_image = st.file_uploader("支持截图或拍照上传", type=["png", "jpg", "jpeg"], key="solver_upload")
            
        if solve_image is not None:
            if st.button("✨ 提交并启动联合解码解答", type="primary", use_container_width=True):
                
                status_placeholder = st.empty()
                
                try:
                    img_data = solve_image.getvalue()
                    base64_image = base64.b64encode(img_data).decode('utf-8')
                    zhipu_api_key = st.secrets["ZHIPU_KEY"]
                    vision_client = OpenAI(
                        api_key=zhipu_api_key,
                        base_url="https://open.bigmodel.cn/api/paas/v4/"
                    )
                    
                    status_placeholder.info("👁️ 正在调用视觉模型 (GLM-4V) 提取图像中的数学特征...")
                    
                    ocr_prompt = "请仅仅提取图片中的数学题目公式，将其转换为标准的一行 LaTeX 代码。绝对不要尝试解答这道题，不要任何说明文字，只要代码本身。"
                    ocr_response = vision_client.chat.completions.create(
                        model="glm-4v",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": ocr_prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }]
                    )
                    
                    equation_latex = ocr_response.choices[0].message.content.replace("```latex", "").replace("```", "").replace("<answer>", "").replace("</answer>", "").strip()
                    
                    status_placeholder.success(f"✅ 提取成功！识别方程为: $ {equation_latex} $ \n\n🧠 正在交由 DeepSeek 数学逻辑引擎进行深度推导...")
                    
                    solve_prompt = f"""你是一名资深的大学数学教授，精通【{st.session_state.solver_mode}】。
                    请解答以下数学题（它是从图片中提取出的 LaTeX 公式）：
                    $$ {equation_latex} $$
                    
                    请务必遵守以下规范：
                    1. 严格使用以下模板结构，并且包含中文文字说明：
                    **【题目分析】**
                    (一句话指出核心考点)
                    **【详细推导步骤】**
                    (一步一步写出计算过程。每一步必须有中文解说。公式两边必须用 $ 包裹，例如：$y=x^2$。独立成行的长公式用 $$ 包裹。)
                    **【最终答案】**
                    (写出最终结果，用 $$ 包裹)
                    
                    2. 绝对禁止输出 <answer> 或 </answer> 这种 XML 标签。
                    """
                    
                    solve_response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[{"role": "user", "content": solve_prompt}]
                    )
                    
                    clean_ans = solve_response.choices[0].message.content.replace("<answer>", "").replace("</answer>", "").strip()
                    
                    status_placeholder.empty()
                    st.success("解答完成！以下是数学逻辑引擎的推导步骤：")
                    st.markdown(clean_ans)
                    
                except Exception as e:
                    status_placeholder.error(f"解析过程中发生错误，请检查 API 配置或网络。")
