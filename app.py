"""
🇩🇿 SmartEdu Algeria V5.0 - Global Learning Platform
المواصفات:
- واجهة بصرية عالمية المستوى (Enterprise UI)
- محرك توصيات ذكاء اصطناعي (Recommendation Engine)
- تحليلات بيانات متقدمة (Advanced Analytics with Plotly)
- مسار تعلم ذكي (Smart Learning Paths)
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from supabase import create_client, Client
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# 1. CONFIG & CONNECTION
# ==========================================

st.set_page_config(
    page_title="SmartEdu Global",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# الاتصال (تأكد من صحة البيانات في الإصدار السابق)
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "YOUR_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "YOUR_KEY")

try:
    client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    client = None

# ==========================================
# 2. GLOBAL UI STYLING (Glassmorphism & Animations)
# ==========================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&display=swap');
    
    .stApp {
        background-color: #0f172a; /* Dark Modern Background */
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }
    
    /* Sidebar - Dashboard Style */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-left: 1px solid #334155;
    }

    /* Glass Card for Dark Mode */
    .glass-dark {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        color: #f8fafc;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    
    .glass-dark:hover {
        transform: translateY(-2px);
        border-color: #3b82f6;
    }
    
    /* Primary Button - Gradient */
    .stButton>button[kind="primary"] {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1rem;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button[kind="primary"]:hover {
        box-shadow: 0 6px 25px rgba(139, 92, 246, 0.5);
        transform: scale(1.01);
    }
    
    /* Metrics Styles */
    [data-testid="stMetricValue"] {
        color: #f8fafc;
        font-family: 'Tajawal', sans-serif;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8;
    }
    
    /* Skill Progress Bar */
    .skill-bar-bg {
        background: #334155;
        border-radius: 10px;
        height: 10px;
        overflow: hidden;
        margin-top: 5px;
    }
    .skill-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
        border-radius: 10px;
    }

    /* Hide Footer */
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. MOCK DATA GENERATOR (For Rich Experience)
# ==========================================

RICH_LESSONS = [
    {"id": 1, "title": "احتراف التفاضل والتكامل", "subject": "رياضيات", "level": "ثانوي", 
     "difficulty": "متقدم", "duration": "45 دقيقة", "students": 1250, "rating": 4.9,
     "image": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600", 
     "tags": ["حساب", "رسم بياني", "جامعي"], "instructor": "د. علي بن ناصر"},
    
    {"id": 2, "title": "الفيزياء الكمومية للجميع", "subject": "فيزياء", "level": "ثانوي", 
     "difficulty": "خبير", "duration": "60 دقيقة", "students": 890, "rating": 5.0,
     "image": "https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?w=600", 
     "tags": ["ميكانيكا", "نظرية", "فضاء"], "instructor": "أ. ياسين"},
    
    {"id": 3, "title": "فنون الخط العربي", "subject": "لغة عربية", "level": "ابتدائي", 
     "difficulty": "مبتدئ", "duration": "30 دقيقة", "students": 3200, "rating": 4.7,
     "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=600", 
     "tags": ["إبداع", "ثقافة", "رسم"], "instructor": "أ. ليلى"},
    
    {"id": 4, "title": "برمجة تطبيقات الويب", "subject": "علوم الحاسوب", "level": "ثانوي", 
     "difficulty": "متوسط", "duration": "90 دقيقة", "students": 1500, "rating": 4.8,
     "image": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=600", 
     "tags": ["كود", "برمجة", "تكنولوجيا"], "instructor": "م. كريم"},
]

# ==========================================
# 4. ADVANCED LOGIC: AI ENGINE & DATA
# ==========================================

class RecommendationEngine:
    """محرك ذكاء اصطناعي للتوصيات (AI Recommendation Engine)"""
    
    @staticmethod
    def get_for_you(user_profile: Dict, all_lessons: List[Dict]) -> List[Dict]:
        """
        خوارزمية التوصية:
        1. فلترة حسب المستوى.
        2. إعطاء نقاط (Score) بناءً على الاهتمامات، الصعوبة، والشعبية.
        3. الترتيب.
        """
        user_level = user_profile.get('level', '')
        disability = user_profile.get('disability_type', 'عادي')
        
        scored_lessons = []
        
        for lesson in all_lessons:
            score = 0
            
            # 1. معيار المستوى (40%)
            if lesson['level'] == user_level:
                score += 40
            elif (user_level == 'ثانوي' and lesson['level'] == 'متوسط') or \
                 (user_level == 'متوسط' and lesson['level'] == 'ابتدائي'):
                score += 20 # دروس أساسية للمستوى الأعلى

            # 2. معامل الإعاقة (30%) - التكيف
            if disability == 'صم':
                # التفضيل للدروس البصرية (محاكاة عبر الوسوم)
                if 'رسم' in lesson['tags'] or 'ثقافة' in lesson['tags']:
                    score += 30
            elif disability == 'ضعاف سمع':
                # التفضيل للدروس النصية/المكتوبة
                if 'كود' in lesson['tags'] or 'رسم' in lesson['tags']:
                    score += 30
            
            # 3. الشعبية (30%)
            score += min((lesson['students'] / 100), 30)
            
            # 4. معامل التقييم (مكافأة)
            score += (lesson['rating'] * 2)
            
            lesson['ai_score'] = score
            scored_lessons.append(lesson)
            
        # الترتيب تنازلياً
        return sorted(scored_lessons, key=lambda x: x['ai_score'], reverse=True)

class ContextualAI:
    """مساعد ذكي يحاكي الردود بناءً على سياق الدرس"""
    
    @staticmethod
    def chat_response(user_question: str, context_lesson: Dict = None) -> str:
        # محاكاة ذكاء اصطناعي (يمكن ربطه بـ OpenAI هنا)
        
        greetings = ["مرحباً", "السلام", "أهلاً"]
        if any(word in user_question for word in greetings):
            return "أهلاً بك! أنا مساعدك الذكي التعليمي. كيف يمكنني مساعدتك في دراستك اليوم؟ 🇩🇿"
        
        if context_lesson:
            subject = context_lesson['subject']
            if "رياضيات" in subject:
                return f"في موضوع الرياضيات، {'حل المعادلات يتطلب التركيز على الخطوات المنطقية' if 'معادلة' in user_question else 'التكامل هو عملية عكسية للتفاضل، وهو مفيد لحساب المساحات'}."
            elif "فيزياء" in subject:
                return f"في الفيزياء، {'الطاقة لا تفنى ولا تستحدث بل تتحول من شكل لآخر' if 'طاقة' in user_question else 'الجاذبية قوة تجذب الأجسام نحو بعضها البعض'}."
        
        return "سؤال ممتاز! لكي أقدم لك الإجابة الأكثر دقة، هل يمكنك التعمق قليلاً في النقطة التي تشعر بالارتباك فيها؟"

# ==========================================
# 5. UI COMPONENTS
# ==========================================

def render_skill_radar():
    """رسم مخطط مهارات الطالب (Radar Chart)"""
    categories = ['الرياضيات', 'الفيزياء', 'اللغة العربية', 'العلوم', 'التاريخ']
    values = [85, 70, 90, 65, 80] # بيانات وهمية للطالب
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        marker_color='rgba(59, 130, 246, 0.6)',
        line_color='rgba(59, 130, 246, 1)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color='#94a3b8')
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc', family='Tajawal'),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig

def render_course_card(lesson, is_hero=False):
    """رسم بطاقة درس عالمية"""
    width = 100 if is_hero else 100
    height = 400 if is_hero else 200
    
    if is_hero:
        st.markdown(f"""
        <div class="glass-dark" style="background: url('{lesson['image']}'); background-size: cover; background-position: center; min-height: 300px; position: relative; overflow: hidden;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, #0f172a); padding: 30px;">
                <h2 style="margin: 0; font-size: 2.5rem; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">{lesson['title']}</h2>
                <p style="color: #cbd5e1; font-size: 1.2rem;">{lesson['instructor']}</p>
                <div style="margin-top: 15px;">
                    <span style="background: #3b82f6; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold;">{lesson['subject']}</span>
                    <span style="background: #10b981; color: white; padding: 5px 15px; border-radius: 20px; margin-right: 10px; font-weight: bold;">⭐ {lesson['rating']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(lesson['image'], use_column_width=True)
            with col2:
                st.markdown(f"<span style='color: #3b82f6; font-weight: bold;'>{lesson['subject']}</span>", unsafe_allow_html=True)
                st.subheader(lesson['title'])
                st.caption(f"👨‍🏫 {lesson['instructor']} | ⏱️ {lesson['duration']} | 👥 {lesson['students']} طالب")
                
                # Tags
                tags_html = " ".join([f"<span style='background:#334155; color:#cbd5e1; padding:3px 8px; border-radius:5px; font-size:0.8rem; margin-left:5px;'>{tag}</span>" for tag in lesson['tags']])
                st.markdown(tags_html, unsafe_allow_html=True)
                
                # Progress Sim
                st.markdown('<div class="skill-bar-bg"><div class="skill-bar-fill" style="width: 75%;"></div></div>', unsafe_allow_html=True)
                st.caption("أكملت 75% من هذا المسار")

def show_global_dashboard(user):
    """لوحة تحكم الطالب العالمية"""
    
    # 1. Header with Progress
    st.markdown(f"<h1 style='font-weight: 900; margin-bottom: 0;'>مرحباً، {user['full_name']} 👋</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #94a3b8; font-size: 1.1rem; margin-top: 5px;'>لقد وصلت إلى المستوى <strong style='color: #f59e0b;'>المتقدم (Level 8)</strong> | 🔥 15 يوم تواصل</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # 2. Main Recommendation (AI Hero Section)
    recommendations = RecommendationEngine.get_for_you(user, RICH_LESSONS)
    top_pick = recommendations[0]
    
    st.markdown("<h3 style='color: #f8fafc;'>🎯 الدرس المقترح لك اليوم (ذكاء اصطناعي)</h3>", unsafe_allow_html=True)
    render_course_card(top_pick, is_hero=True)
    
    if st.button("ابدأ التعلم الآن", key="hero_start"):
        st.success("تم توجيهك للدرس...")
    
    # 3. Advanced Analytics Row
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("<div class='glass-dark'><h3>📊 تحليل المهارات</h3></div>", unsafe_allow_html=True)
        st.plotly_chart(render_skill_radar(), use_container_width=True)
        
    with col2:
        st.markdown("<div class='glass-dark'><h3>🏆 الإنجازات</h3></div>", unsafe_allow_html=True)
        ach = [
            "🥇 أول الدفعة", "📚 قرأ 10 دروس", "🔥 تواصل أسبوع", "💬 شارك 5 مرات"
        ]
        for a in ach:
            st.markdown(f"<div style='padding: 10px; background: #334155; margin-bottom: 8px; border-radius: 8px; border-right: 3px solid #10b981;'>{a}</div>", unsafe_allow_html=True)
            
    with col3:
        st.markdown("<div class='glass-dark'><h3>📈 الإحصائيات</h3></div>", unsafe_allow_html=True)
        st.metric("ساعات الدراسة", "128h", "+12%")
        st.metric("الدروس المنجزة", "45", "+5")
        st.metric("الدقة العامة", "92%", "+2%")

    st.divider()
    
    # 4. Continue Watching / More Recommendations
    st.markdown("<h3 style='color: #f8fafc;'>✨ مقترحات إضافية لك</h3>", unsafe_allow_html=True)
    
    # Grid Layout
    for rec in recommendations[1:4]:
        render_course_card(rec)
        st.markdown("---")

def show_ai_chatbot(user):
    """واجهة المساعد الذكي المتقدم"""
    st.title("🤖 المساعد التعليمي الذكي (SmartBot)")
    
    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display Chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User Input
    if prompt := st.chat_input("اسألني عن أي درس..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI Response Logic
        # محاكاة التفكير
        with st.chat_message("assistant"):
            with st.spinner("جاري تحليل السؤال..."):
                # استخدام الذكاء الاصطناعي التفاعلي
                response = ContextualAI.chat_response(prompt)
                time.sleep(1) # تأخير اصطناعي للواقعية
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# ==========================================
# 6. MAIN APP LOGIC
# ==========================================

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    # Login Simulation (Keep existing logic)
    if not st.session_state['logged_in']:
        st.title("🇩🇿 SmartEdu Login")
        user_in = st.text_input("User", value="student1")
        pass_in = st.text_input("Pass", type="password", value="student")
        if st.button("Login"):
            if user_in == "admin" and pass_in == "admin":
                st.session_state['user'] = {"full_name": "Admin User", "role": "مدير", "level": "ثانوي", "disability_type": "عادي"}
                st.session_state['logged_in'] = True
            else:
                # Mock Student Login
                st.session_state['user'] = {"full_name": "سارة الجزائرية", "role": "طالب", "level": "ثانوي", "disability_type": "صم"}
                st.session_state['logged_in'] = True
            st.rerun()
    
    else:
        user = st.session_state['user']
        
        # Sidebar Navigation
        with st.sidebar:
            st.markdown(f"<h2 style='text-align: center; color: white;'>🎓 {user['role']}</h2>", unsafe_allow_html=True)
            st.info(f"المستخدم: {user['full_name']}")
            
            nav = st.radio("التنقل", ["🏠 الرئيسية", "🤖 المساعد الذكي", "📂 مكتبة الدروس", "📊 تحليلاتي"])
            
            st.divider()
            if st.button("تسجيل خروج"):
                st.session_state.clear()
                st.rerun()

        # Page Routing
        if nav == "🏠 الرئيسية":
            show_global_dashboard(user)
        elif nav == "🤖 المساعد الذكي":
            show_ai_chatbot(user)
        elif nav == "📂 مكتبة الدروس":
            st.header("المكتبة الكاملة")
            for l in RICH_LESSONS:
                render_course_card(l)
        elif nav == "📊 تحليلاتي":
            st.header("تحليلات متقدمة")
            st.plotly_chart(render_skill_radar(), use_container_width=True)

if __name__ == "__main__":
    main()
