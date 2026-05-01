"""
🇩🇿 SmartEdu Algeria V3.0 - Ultimate Edition
المميزات الجديدة:
- واجهة تعليمية فائقة الجودة (Modern UI/UX)
- لوحة قيادة احترافية KPI للمدراء والمعلمين
- معرض صور مرئي (Visual Gallery) للصم والبكم
- نظام تقييم واقتراحات ذكي
- بيانات تجريبية غنية (Rich Mock Data)
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict

# ==========================================
# 1. CONFIGURATION & SETUP
# ==========================================

st.set_page_config(
    page_title="المنصة التعليمية الذكية - الجزائر",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI
st.markdown("""
<style>
    /* Fonts & Base */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;800&display=swap');
    
    body {
        font-family: 'Tajawal', sans-serif;
        background-color: #f4f6f9;
    }
    
    .stApp {
        direction: rtl;
        text-align: right;
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #006633 0%, #004d26 100%);
    }
    
    .css-1d391kg a {
        color: white !important;
        font-weight: bold;
        font-size: 1.1rem;
    }

    /* KPI Cards (Executive Style) */
    .kpi-container {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        flex: 1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-right: 4px solid #006633;
        transition: transform 0.3s;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    
    .kpi-title {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 10px;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #333;
    }
    
    .kpi-trend {
        font-size: 0.8rem;
        color: #00cc66; /* Green for growth */
    }

    /* Lesson Cards with Images */
    .lesson-card {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        margin-bottom: 20px;
    }
    
    .lesson-card:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    
    .lesson-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
    }
    
    .lesson-content {
        padding: 20px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }
    
    .rating-stars {
        color: #FFC107;
        font-size: 1.2rem;
    }

    /* Gallery Grid */
    .gallery-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 15px;
    }
    
    .gallery-item {
        position: relative;
        border-radius: 10px;
        overflow: hidden;
        cursor: pointer;
        height: 200px;
    }
    
    .gallery-item img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.4s;
    }
    
    .gallery-item:hover img {
        transform: scale(1.1);
    }
    
    .overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(0,0,0,0.6);
        color: white;
        padding: 10px;
        font-size: 0.9rem;
    }

    /* Buttons */
    .btn-gradient {
        background: linear-gradient(45deg, #006633, #00cc66);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0, 102, 51, 0.3);
    }
    
    /* Utilities */
    .text-primary { color: #006633; }
    .badge { padding: 5px 10px; border-radius: 12px; font-size: 0.8rem; color: white; }
    .bg-math { background-color: #2196F3; }
    .bg-science { background-color: #4CAF50; }
    .bg-history { background-color: #FF9800; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MOCK DATA & DATABASE LAYER
# ==========================================

class AdvancedDatabase:
    """قاعدة بيانات غنية بالصور والمحتوى"""
    
    def __init__(self):
        self.users = [
            {"id": 1, "username": "admin", "password": "1", "role": "مدير", "name": "مدير النظام", "avatar": "👨‍💼"},
            {"id": 2, "username": "teacher", "password": "1", "role": "معلم", "name": "أستاذ محمد", "avatar": "👨‍🏫"},
            {"id": 3, "username": "student", "password": "1", "role": "طالب", "name": "طالب مجتهد", "disability": "صم", "level": "ثانوي", "avatar": "🧑‍🎓"},
        ]
        
        # دروس مع صور وعناوين جذابة
        self.lessons = [
            {
                "id": 1, "title": "أساسيات التفاضل والتكامل", "subject": "رياضيات", "level": "ثانوي",
                "image": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=500",
                "rating": 4.8, "views": 1200, "difficulty": "متقدم", "tags": ["رسم بياني", "معادلات"],
                "description": "تعلم كيفية حساب المشتقات والتكاملات بأسلوب بصري مبسط."
            },
            {
                "id": 2, "title": "الطاقة الشمسية والاستدامة", "subject": "علوم", "level": "متوسط",
                "image": "https://images.unsplash.com/photo-1509391366360-2e959784a276?w=500",
                "rating": 4.5, "views": 850, "difficulty": "متوسط", "tags": ["بيئة", "طاقة"],
                "description": "اكتشف كيف تعمل الألواح الشمسية وأهميتها للبيئة."
            },
            {
                "id": 3, "title": "ثورة نوفمبر المجيدة", "subject": "تاريخ", "level": "ثانوي",
                "image": "https://images.unsplash.com/photo-1569074187119-c87815b476da?w=500",
                "rating": 5.0, "views": 2100, "difficulty": "سهل", "tags": ["وطنية", "مقاومة"],
                "description": "رحلة بصرية عبر تاريخ ثورة التحرير الجزائرية."
            },
            {
                "id": 4, "title": "الجملة الفعلية في اللغة العربية", "subject": "لغة عربية", "level": "ابتدائي",
                "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500",
                "rating": 4.2, "views": 600, "difficulty": "سهل", "tags": ["نحو", "قواعد"],
                "description": "شرح مبسط مع أمثلة مرئية للجملة الفعلية."
            },
            {
                "id": 5, "title": "علم الفلك النجوم", "subject": "علوم", "level": "ثانوي",
                "image": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=500",
                "rating": 4.9, "views": 1500, "difficulty": "متقدم", "tags": ["فضاء", "كواكب"],
                "description": "رحلة عبر الكون لفهم النظام الشمسي والمجرات."
            }
        ]
        
        self.gallery_images = [
            "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=300",
            "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=300",
            "https://images.unsplash.com/photo-1505664194779-8beaceb93744?w=300",
            "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=300",
            "https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=300",
            "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=300"
        ]
        
        self.analytics = {
            "total_users": 1542,
            "active_today": 230,
            "lessons_completed": 8900,
            "avg_score": 78.5,
            "growth": "+12%"
        }

    def get_user(self, username, password):
        for u in self.users:
            if u['username'] == username and u['password'] == password:
                return u
        return None

    def get_all_lessons(self):
        return self.lessons

    def get_gallery(self):
        return self.gallery_images

# ==========================================
# 3. UI COMPONENTS & HELPERS
# ==========================================

def render_kpi_card(title, value, trend, icon, color="#006633"):
    """رسم بطاقة KPI احترافية"""
    st.markdown(f"""
    <div class="kpi-card" style="border-right-color: {color}">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-trend">{trend} <span style="font-size:1.2rem">📈</span></div>
            </div>
            <div style="font-size: 3rem; opacity: 0.8;">{icon}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_lesson_card(lesson, key):
    """رسم بطاقة درس متقدمة مع صورة"""
    bg_color = "bg-math" if lesson['subject'] == "رياضيات" else "bg-science" if lesson['subject'] == "علوم" else "bg-history"
    
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(lesson['image'], use_column_width=True)
        
        with col2:
            st.markdown(f"""
            <span class="badge {bg_color}">{lesson['subject']}</span>
            <span class="badge" style="background:gray; margin-right:5px;">{lesson['level']}</span>
            """, unsafe_allow_html=True)
            
            st.subheader(lesson['title'])
            st.markdown(f"<div class='rating-stars'>{'⭐' * int(lesson['rating'])} ({lesson['rating']}/5)</div>", unsafe_allow_html=True)
            st.caption(lesson['description'])
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("👀 مشاهدة", key=f"watch_{key}", use_container_width=True):
                    st.session_state['current_lesson'] = lesson
                    st.session_state['page'] = 'lesson_detail'
                    st.rerun()
            
            with col_btn2:
                st.metric("المشاهدات", lesson['views'])
            
            with col_btn3:
                rating = st.slider("قيم الدرس", 1, 5, key=f"rate_{key}", label_visibility="collapsed")

        st.markdown("---")

# ==========================================
# 4. DASHBOARDS
# ==========================================

def show_login(db):
    st.markdown("<h1 style='text-align: center; color: #006633;'>تسجيل الدخول للمنصة التعليمية</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>نظام تعليمي متكامل يدعم الصم والبكم والطلاب العاديين</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login"):
            st.info("حسابات تجريبية:\n- مدير: admin / 1\n- معلم: teacher / 1\n- طالب: student / 1")
            user_input = st.text_input("اسم المستخدم")
            pass_input = st.text_input("كلمة المرور", type="password")
            submitted = st.form_submit_button("دخول", use_container_width=True)
            
            if submitted:
                user = db.get_user(user_input, pass_input)
                if user:
                    st.session_state['user'] = user
                    st.session_state['logged_in'] = True
                    st.success(f"مرحباً بك {user['name']}")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("خطأ في البيانات")

def admin_dashboard(db):
    st.header("🛡️ لوحة القيادة التنفيذية (Executive Dashboard)")
    
    # Row 1: KPIs
    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: render_kpi_card("إجمالي الطلاب", db.analytics['total_users'], db.analytics['growth'], "👥", "#2196F3")
    with col2: render_kpi_card("النشاط اليومي", db.analytics['active_today'], "+5%", "⚡", "#FF9800")
    with col3: render_kpi_card("الدروس المنجزة", db.analytics['lessons_completed'], "+22%", "📚", "#4CAF50")
    with col4: render_kpi_card("متوسط الدرجات", f"{db.analytics['avg_score']}%", "+1.2%", "🏆", "#9C27B0")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Row 2: Charts
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.subheader("📊 أداء الطلاب حسب المواد")
        # Mock Chart Data
        chart_data = pd.DataFrame({
            'المادة': ['رياضيات', 'علوم', 'تاريخ', 'عربي', 'انجليزي'],
            'الأداء': [85, 78, 92, 88, 70]
        })
        st.bar_chart(chart_data.set_index('المادة'), color="#006633")
    
    with col_chart2:
        st.subheader("📈 نمو التسجيلات (آخر 6 أشهر)")
        growth_data = pd.DataFrame({
            'الشهر': ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو'],
            'عدد الطلاب': [100, 120, 150, 200, 230, 260]
        })
        st.line_chart(growth_data.set_index('الشهر'))
    
    # Row 3: Teacher Performance Table
    st.subheader("👩‍🏫 تقييم المعلمين")
    teacher_data = pd.DataFrame({
        "المعلم": ["أ. محمد", "أ. سارة", "أ. أحمد"],
        "المادة": ["رياضيات", "علوم", "لغة عربية"],
        "تقييم الطلاب": [4.8, 4.5, 4.9],
        "عدد الدروس": [12, 15, 10]
    })
    st.dataframe(teacher_data, use_container_width=True)

def teacher_dashboard(db):
    st.header("👨‍🏫 بوابة المعلم")
    
    tab_teach, tab_students = st.tabs(["📝 إدارة المحتوى", "👥 متابعة الطلاب"])
    
    with tab_teach:
        col_left, col_right = st.columns([1, 2])
        with col_left:
            st.info("إضافة درس جديد")
            title = st.text_input("عنوان الدرس")
            subject = st.selectbox("المادة", ["رياضيات", "علوم", "تاريخ"])
            level = st.selectbox("المستوى", ["ابتدائي", "متوسط", "ثانوي"])
            if st.button("نشر الدرس", use_container_width=True):
                st.success("تم نشر الدرس بنجاح!")
        
        with col_right:
            st.subheader("📂 مكتبة الدروس الحالية")
            for l in db.lessons:
                st.markdown(f"- **{l['title']}** ({l['subject']}) - ⭐ {l['rating']}")
    
    with tab_students:
        st.subheader("تقارير أداء الطلاب")
        # Mock Student List
        students = [
            {"name": "علي بن محمد", "progress": 80, "last_active": "منذ ساعة"},
            {"name": "فاطمة الزهراء", "progress": 45, "last_active": "أمس"},
            {"name": "ياسين براهيمي", "progress": 95, "last_active": "الآن"},
        ]
        
        for s in students:
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                c1.write(f"🧑‍🎓 **{s['name']}**")
                c2.progress(s['progress'])
                c3.caption(s['last_active'])
                st.divider()

def student_dashboard(db, user):
    # Hero Section
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #006633 0%, #004d26 100%); padding: 30px; border-radius: 20px; color: white; text-align: center; margin-bottom: 30px;">
        <h1 style="margin: 0;">مرحباً بك في رحلتك التعليمية 🇩🇿</h1>
        <p style="opacity: 0.9;">{user['name']} | المستوى: {user['level']} | نوع الحساب: {user['disability']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Tabs
    tab_learn, tab_gallery, tab_progress = st.tabs(["🎓 الدروس والمقترحات", "🖼️ المعرض المرئي", "📊 تقدمي"])
    
    with tab_learn:
        st.subheader("🌟 دروس مختارة لك")
        lessons = db.get_all_lessons()
        
        # Search & Filter
        col_search, col_filter = st.columns([3, 1])
        with col_search: search = st.text_input("🔍 ابحث عن درس...", placeholder="مثال: تاريخ الجزائر")
        with col_filter: subject_filter = st.selectbox("المادة", ["الكل"] + ["رياضيات", "علوم", "تاريخ", "لغة عربية"])
        
        # Rendering Cards
        count = 0
        for lesson in lessons:
            if search and search.lower() not in lesson['title'].lower(): continue
            if subject_filter != "الكل" and lesson['subject'] != subject_filter: continue
            
            render_lesson_card(lesson, count)
            count += 1
    
    with tab_gallery:
        st.subheader("🖼️ معرض الصور التعليمية (Visual Gallery)")
        st.caption("مكتبة صور توضيحية للطلاب الصم والبكم لتسهيل الفهم")
        
        images = db.get_gallery()
        cols = st.columns(3)
        for i, img_url in enumerate(images):
            with cols[i % 3]:
                st.image(img_url, use_column_width=True, caption=f"صورة توضيحية {i+1}")
    
    with tab_progress:
        st.subheader("📊 تقرير أدائي")
        
        # Charts for Student
        c1, c2 = st.columns(2)
        with c1:
            st.metric("الدروس المكتملة", "12", "+2")
            st.metric("ساعات الدراسة", "45 ساعة", "+5 ساعات")
        
        with c2:
            st.metric("معدل التقييم", "4.7/5", "+0.2")
            st.metric("نقاط الخبرة", "850 XP", "+50 XP")
            
        st.divider()
        st.write("تفاصيل التفاعل:")
        activity_data = pd.DataFrame({
            'النشاط': 'الدروس المقروءة', 'العدد': [12]
        })
        st.bar_chart(activity_data)

# ==========================================
# 5. LESSON DETAIL VIEW (MODAL STYLE)
# ==========================================

def show_lesson_detail(lesson):
    st.markdown(f"""
    <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
        <div style="background: white; width: 80%; max-width: 800px; padding: 30px; border-radius: 20px; max-height: 90vh; overflow-y: auto; position: relative;">
            <button onclick="document.querySelector('button[title=\'Close\']').click()" style="position: absolute; top: 15px; right: 15px; background: red; color: white; border: none; border-radius: 50%; width: 30px; height: 30px; cursor: pointer;">✕</button>
            <h1 style="color: #006633;">{lesson['title']}</h1>
            <img src="{lesson['image']}" style="width: 100%; border-radius: 15px; margin: 20px 0;">
            
            <h3>📝 وصف الدرس</h3>
            <p>{lesson['description']}</p>
            
            <h3>🏷️ الوسوم</h3>
            {', '.join(lesson['tags'])}
            
            <div style="margin-top: 30px; padding: 20px; background: #f0f8ff; border-radius: 10px; border: 1px dashed #006633;">
                <h4>💬 منطق الذكاء الاصطناعي:</h4>
                <p>بناءً على تفاعل السابق، نوصي بمشاهدة الفيديو أولاً ثم حل التمارين البصرية.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Native Streamlit button to exit the "modal" state
    if st.button("🔙 عودة للقائمة", key="exit_detail"):
        st.session_state['page'] = 'student_dashboard'
        st.session_state.pop('current_lesson', None)
        st.rerun()

# ==========================================
# 6. MAIN APP LOOP
# ==========================================

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['page'] = 'login'

    db = AdvancedDatabase()
    
    # Sidebar Logic
    if st.session_state['logged_in']:
        with st.sidebar:
            user = st.session_state['user']
            st.markdown(f"<h2 style='text-align: center; color: white;'>🎓 {user['name']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; color: white; opacity: 0.8;'>{user['role']}</p>", unsafe_allow_html=True)
            st.divider()
            
            if st.button("🏠 الرئيسية"):
                st.session_state['page'] = 'student_dashboard' if user['role'] == 'طالب' else 'admin_dashboard'
                st.rerun()
            
            if st.button("🚪 خروج"):
                st.session_state.clear()
                st.rerun()
    
    # Routing
    if not st.session_state['logged_in']:
        show_login(db)
    
    elif st.session_state['page'] == 'lesson_detail' and 'current_lesson' in st.session_state:
        show_lesson_detail(st.session_state['current_lesson'])
    
    else:
        user = st.session_state['user']
        if user['role'] == 'طالب':
            student_dashboard(db, user)
        elif user['role'] == 'معلم':
            teacher_dashboard(db)
        elif user['role'] == 'مدير':
            admin_dashboard(db)

if __name__ == "__main__":
    main()
