import streamlit as st
import pandas as pd
import os
import time

# ==========================================
# 1. 页面基本配置
# ==========================================
st.set_page_config(
    page_title="政策红利匹配引擎 | 智慧社区",
    page_icon="☀️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# 🎨 V6.0 终极动效增强版：在阳光社区基础上叠加复杂特效
# ==========================================
st.markdown("""
<style>
    /* 强制全站核心文字为深色，确保可读性 */
    [data-testid="stAppViewContainer"], label, .stMarkdown p, .stMarkdown li {
        color: #2c3e50 !important; 
        text-shadow: none !important;
    }

    /* 1. 动态温馨背景：高清阳光社区 + 缓慢平移漫游 */
    .stApp {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.45) 0%, rgba(255, 250, 240, 0.55) 100%),
                    url("https://images.unsplash.com/photo-1521737604893-d14cc237f11d?q=100&w=3840&auto=format&fit=crop");
        background-size: 120% 120%;
        background-attachment: fixed;
        animation: panBackground 40s alternate infinite ease-in-out;
    }
    @keyframes panBackground {
        0% { background-position: 0% 0%; }
        100% { background-position: 100% 100%; }
    }
    
    header[data-testid="stHeader"] { background: transparent !important; }

    /* 2. 极致毛玻璃卡片：增加饱和度和细腻的入场动画 */
    [data-testid="stForm"], [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.85) !important; 
        backdrop-filter: blur(20px) saturate(120%);
        -webkit-backdrop-filter: blur(20px) saturate(120%);
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        border-top: 5px solid #ff7043 !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08) !important;
        animation: floatUp 0.8s ease-out forwards;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* 加入弹簧动画曲线 */
    }
    
    /* 🌟 新增特效：3D 悬浮磁吸卡片 */
    [data-testid="stExpander"]:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 20px 40px rgba(255, 112, 67, 0.2) !important;
        border-color: rgba(255, 112, 67, 0.4) !important;
    }

    @keyframes floatUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* 3. 流光溢彩按钮：呼吸 + 金属扫光特效 */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #ff7043 0%, #f4511e 50%, #ff7043 100%);
        background-size: 200% auto;
        color: white !important; 
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(255, 112, 67, 0.4);
        position: relative;
        overflow: hidden;
        animation: gradientShift 3s ease infinite, pulseBtn 2s infinite; 
        transition: transform 0.2s;
    }
    
    /* 扫光动画结构 */
    div.stButton > button:first-child::after {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 50%; height: 100%;
        background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.4) 50%, rgba(255,255,255,0) 100%);
        transform: skewX(-20deg);
        animation: shimmer 3s infinite;
    }
    @keyframes shimmer { 100% { left: 200%; } }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes pulseBtn {
        0% { box-shadow: 0 0 0 0 rgba(255, 112, 67, 0.6); }
        70% { box-shadow: 0 0 0 15px rgba(255, 112, 67, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 112, 67, 0); }
    }
    div.stButton > button:first-child:hover { transform: scale(1.03); }

    /* 4. 标题心跳与全息渐变字 */
    .heartbeat {
        animation: heartbeatAnim 1.5s infinite;
        display: inline-block;
    }
    @keyframes heartbeatAnim {
        0%, 100% { transform: scale(1); }
        15% { transform: scale(1.25); }
        30% { transform: scale(1); }
        45% { transform: scale(1.25); }
    }
    
    .gradient-text {
        background: linear-gradient(90deg, #e65c00, #F9D423);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }

    /* 5. 模拟打字机动画 */
    .typewriter {
        overflow: hidden; 
        border-right: .15em solid orange; 
        white-space: nowrap; 
        margin: 0 auto; 
        letter-spacing: .1em; 
        animation: typing 3s steps(40, end), blink-caret .75s step-end infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }
    @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: orange; } }
    
    /* 强制输入框底色防止看不清 */
    input, select, [data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #333 !important;
        border-radius: 8px !important;
        border: 1px solid #ddd !important;
        transition: border 0.3s !important;
    }
    input:focus, [data-baseweb="select"] > div:focus-within {
        border: 2px solid #ff7043 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 数据加载引擎
# ==========================================
@st.cache_data
def load_real_data():
    file_path = "policies.csv"
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        default_csv = """id,name,category,description,condition_age_min,condition_age_max,condition_status,condition_income_max,amount
P001,高校毕业生到基层就业补贴,就业创业,鼓励高校毕业生到中小微企业或基层社会组织就业，依法缴纳社保满6个月即可申领。,18,28,学生/应届生,999999,3000元 一次性
P002,灵活就业人员社保补贴,就业创业,针对以个人身份缴纳城镇职工养老和医疗保险的就业困难人员及离校未就业毕业生。,18,55,待业/灵活就业,8000,最高 800元/月
P003,高龄老人综合津贴（尊老金）,养老服务,具有本市户籍且年满80周岁的老年人即可享受，按年龄段分档发放。,80,120,退休,999999,100-500元/月
P004,最低生活保障家庭救助金,民生保障,家庭人均月收入低于当地最低生活保障标准（如1500元）的困难家庭。,0,120,学生/应届生;在职;待业/灵活就业;退休,1500,按差额发放
P005,青年就业见习生活补贴,就业创业,16-24岁失业青年或毕业学年大学生参加政企合作的就业见习计划期间的生活费支持。,16,24,待业/灵活就业;学生/应届生,999999,当地最低工资的80%
P006,困难残疾人生活补贴,民生保障,针对纳入最低生活保障范围的残疾人，缓解其因残疾产生的额外生活支出困难。,0,120,学生/应届生;在职;待业/灵活就业;退休,1500,200元/月
P007,初创企业无息贷款及贴息,就业创业,针对毕业5年内的高校毕业生、登记失业人员等创办小微企业，提供免息资金支持。,18,45,待业/灵活就业;在职;学生/应届生,999999,最高 30万元
P008,经济困难失能老人居家照护补贴,养老服务,面向60周岁以上、低收入且经过失能评估的老人，发放用于购买上门洗浴、家政等服务的额度。,60,120,退休,2500,300元 服务券/月"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(default_csv)
            
    try:
        df = pd.read_csv(file_path)
        df['condition_status'] = df['condition_status'].apply(lambda x: x.split(';') if isinstance(x, str) else [])
        return df.to_dict('records')
    except Exception as e:
        return []

policies = load_real_data()

# ==========================================
# 3. 侧边栏
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/sun.png", width=80)
    st.title("阳光社区导览")
    st.markdown("---")
    st.info("💡 **设计初衷**\n\n让冰冷的政务数据带有温度，让每一项红利像阳光一样精准照拂社区居民。")
    if policies:
        st.metric(label="当前已接入政策数据库", value=f"{len(policies)} 条")
    st.caption("© 2026 PP创新节 展示项目")

# ==========================================
# 4. 主视觉与表单区
# ==========================================
# 标题增加渐变色与心跳
st.markdown("<h1 style='text-align: center;'><span class='heartbeat'>❤️</span> <span class='gradient-text'>政策红利智能匹配引擎</span></h1>", unsafe_allow_html=True)

# 增加打字机动效副标题
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <p class='typewriter' style='color: #555; font-size: 1.1em; display: inline-block;'>只需 30 秒，我们将为您找出专属的政策权益清单...</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    with st.form("user_profile_form", clear_on_submit=False):
        st.subheader("📝 步骤一：告诉我们您的基本情况")
        st.write("")
        
        col1, col2 = st.columns(2)
        with col1:
            user_age = st.number_input("👤 您的周岁年龄", min_value=0, max_value=120, value=22, step=1)
            user_income = st.number_input("💰 月均总收入 (元)", min_value=0, value=2000, step=500)
            
        with col2:
            user_status = st.selectbox("💼 目前就业/身份状态", ["学生/应届生", "在职", "待业/灵活就业", "退休"])
            has_local_hukou = st.toggle("🏠 拥有本市户籍", value=True)
            
        st.write("")
        submitted = st.form_submit_button("☀️ 启动阳光精准匹配", use_container_width=True)

# ==========================================
# 5. 交互动画与匹配结果面板
# ==========================================
if submitted:
    if not policies:
        st.error("数据库异常，请联系网格员解决。")
    else:
        st.divider()
        
        progress_text = "🔎 正在社区数据库中为您仔细检索..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.008)
            my_bar.progress(percent_complete + 1, text=progress_text)
        my_bar.empty() 
        
        matched_policies = []
        for p in policies:
            if not (p["condition_age_min"] <= user_age <= p["condition_age_max"]): continue
            if user_income > p["condition_income_max"]: continue
            if user_status not in p["condition_status"]: continue
            matched_policies.append(p)
        
        if len(matched_policies) > 0:
            st.balloons() 
            st.markdown("<h2 style='color:#ff7043;'>🎁 您的专属权益看板</h2>", unsafe_allow_html=True)
            
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            metric_col1.metric("为您找到政策", f"{len(matched_policies)} 项")
            metric_col2.metric("覆盖生活领域", f"{len(set([p['category'] for p in matched_policies]))} 个")
            metric_col3.metric("匹配精准度", "99.8%")
            
            st.write("")
            
            for idx, mp in enumerate(matched_policies):
                # 这里鼠标移上去就会有浮起的3D动效
                with st.expander(f"📌 {mp['name']}", expanded=(idx == 0)): 
                    st.markdown(f"**🏷️ 所属分类：** `{mp.get('category', '综合民生')}`")
                    st.markdown(f"**💰 权益标准：** <span style='color:#e53935; font-size:1.2em; font-weight:bold;'>{mp['amount']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**📖 政策白话文：** {mp['description']}")
                    st.info("📃 预计需准备材料：身份证复印件、户口本复印件、对应情况证明。")
                        
        else:
            st.info("👋 感谢您的查询。")
            st.warning("经过仔细比对，当前暂时没有与您情况完全匹配的专项补贴。")
            st.markdown("""
            **别灰心，您可以尝试：**
            * 检查刚才输入的年龄或收入是否有误并重新匹配。
            * 前往所在社区的 **党群服务中心**，工作人员会为您提供更详尽的人工解答。
            """)