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
    
    # --- 第 1 部分：核心功能 ---
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

    # --- 第 2 部分：常见应用导航 ---
    st.subheader("🚀 常见应用导航")
    st.markdown("[📚 CNKI知网 (文献检索)](https://www.cnki.net)")
    st.markdown("[📐 中国数学会 (学术动态)](https://www.cms.org.cn)")
    st.markdown("[🌐 中国大学MOOC (在线课程)](https://www.icourse163.org)")
    st.markdown("[📊 数学建模网 (CUMCM资源)](http://www.mcm.edu.cn)")
    st.markdown("[🏫 学科网 (教学资源)](https://www.zxxk.com)")
    
    st.divider()
    st.caption("让科研更高效，让学习更快乐！")

# ==========================================
# 主页面：三标签页架构 & 苹果便当盒海报
# ==========================================
st.title("♾️ 拓扑One - 智慧数学学伴AI")
st.caption("专为数学专业大学生打造的自适应学业规划与科研辅助系统。")

# 🌟 视觉增强：Apple Bento Box (苹果便当盒) 核心功能海报
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
    justify-content: space-between;
    flex-direction: column;
    border: 1px solid #e5e5ea;
    overflow: hidden;
    position: relative;
}
.bento-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}
.box-large {
    grid-column: span 2;
    grid-row: span 2;
    background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
    justify-content: center;
    align-items: center;
    text-align: center;
}
.box-wide {
    grid-column: span 2;
    background: linear-gradient(135deg, #ffffff 0%, #f0f4f8 100%);
}
.bento-title {
    font-size: 18px;
    font-weight: 700;
    color: #1d1d1f;
    margin-bottom: 8px;
}
.bento-desc {
    font-size: 13px;
    color: #86868b;
    line-height: 1.4;
}
.large-title {
    font-size: 36px;
    font-weight: 800;
    background: -webkit-linear-gradient(45deg, #0071e3, #42a1f5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}
.bg-icon {
    position: absolute;
    right: -10px;
    bottom: -20px;
    font-size: 80px;
    opacity: 0.1;
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
        <div class="bento-desc" style="font-size: 16px;">专为数学专业打造的<br>自适应科研与学习引擎</div>
    </div>
    <div class="bento-box box-wide">
        <div class="bento-title">∑ 多模态 LaTeX 极速识别</div>
        <div class="bento-desc">搭载视觉大模型，复杂数学公式拍照秒转标准代码，告别排版焦虑。</div>
        <div class="bg-icon">📸</div>
    </div>
    <div class="bento-box">
        <div class="bento-title">📈 动态模型</div>
        <div class="bento-desc">SDE、布朗运动<br>参数级实时渲染</div>
        <div class="bg-icon">🎲</div>
    </div>
    <div class="bento-box">
        <div class="bento-title">🏆 CUMCM</div>
        <div class="bento-desc">数模竞赛国奖<br>专属备考路线</div>
        <div class="bg-icon">🏅</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 💡 注意：恢复了第四个标签页！
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
# 标签页 4：拍照搜题 (无弹窗纯上传版)
# ------------------------------------------
with tab_solver:
    st.markdown("### 📸 拓扑One 核心矿山：分发识题系统")
    
    # 状态管理：记录用户当前选择了哪个数学工具
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
        # 进入文件上传模式（手机端点击会自动弹起“拍照/图库”选项）
        col_back, _ = st.columns([1, 4])
        if col_back.button("⬅️ 返回更换题型"):
            st.session_state.solver_mode = None
            st.rerun()
            
        st.markdown(f"#### 当前选定题型：**{st.session_state.solver_mode}**")
        st.caption("请选择题目图片上传。如使用手机访问，点击下方区域可直接拍照。")
        
        solve_image = st.file_uploader("支持截图或拍照上传", type=["png", "jpg", "jpeg"], key="solver_upload")
            
        if solve_image is not None:
            if st.button("✨ 提交并开始智能解答", type="primary", use_container_width=True):
                with st.spinner(f"正在调动视觉大模型解析【{st.session_state.solver_mode}】题目，请稍候..."):
                    try:
                        img_data = solve_image.getvalue()
                        base64_image = base64.b64encode(img_data).decode('utf-8')
                        zhipu_api_key = st.secrets["ZHIPU_KEY"]
                        vision_client = OpenAI(
                            api_key=zhipu_api_key,
                            base_url="https://open.bigmodel.cn/api/paas/v4/"
                        )
                        # 添加了防幻觉的提示词
                        prompt_text = f"你是一个精通【{st.session_state.solver_mode}】的大学数学教授。请识别图片中的数学题目。如果题目计算极其复杂，请侧重于给出清晰的解题思路、步骤框架和核心公式，避免直接心算导致的错误。所有的数学公式必须使用标准的 Markdown LaTeX 语法，行内公式用单个 $ 包裹，独立公式用双 $$ 包裹。绝不能带有任何乱码。"
                        
                        response = vision_client.chat.completions.create(
                            model="glm-4v",
                            messages=[{
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt_text},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]
                            }]
                        )
                        st.success("解答完成！以下是详细步骤：")
                        st.markdown(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"解析失败，请检查配置。")
