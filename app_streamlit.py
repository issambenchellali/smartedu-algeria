"""
🇩🇿 SmartEdu Algeria V14.0 - Innovative Algeria Palette
المميزات الجديدة:
1. تطبيق لوحة "الجزائر المبتكرة" بدقة (أخضر عميق #006241، أحمر نابض #E32636).
2. طباعة ضخمة جداً (Super Bold & Large).
3. تصحيح الترتيب: الخروج فوق اللوج (Logout above Logs).
4. تصميم عصري 2026 مع تدرجات لونية وظلال ناعمة.
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import re
import datetime
import streamlit.components.v1 as components

# ==========================================
# 1. إعدادات CSS (Innovative Algeria Palette)
# ==========================================

st.set_page_config(
    page_title="Innovative LMS - Partage",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@800;900&display=swap');
    
    /* تعريف المتغيرات - Innovate Algeria Palette */
    :root {
        --primary-green: #006241;
        --accent-red: #E32636;
        --bg-white: #F8FAFC;
        --text-main: #1E293B;
        --soft-green: #D1FAE5;
    }
    
    /* الخلفية الأساسية (أبيض لؤلؤي) */
    .stApp {
        background-color: var(--bg-white);
        color: var(--text-main);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }

    /* طباعة ضخمة جداً */
    .stApp, .stMarkdown, .stTextInput, .stSelectbox {
        font-size: 1.4rem !important;
    }
    
    h1, h2, h3, h4 {
        color: var(--text-main);
        font-weight: 900;
        line-height: 1.2;
    }
    
    h1 { font-size: 3.5rem; letter-spacing: -1px; }
    h2 { font-size: 2.8rem; }
    h3 { font-size: 2rem; }

    /* البطاقات العصرية (Soft Shadows & Floating) */
    .lms-card {
        background: white;
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0, 98, 65, 0.08); /* ظل أخضر خفيف */
        border: 1px solid rgba(0, 0, 0, 0.02);
        margin-bottom: 30px;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }

    .lms-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0, 98, 65, 0.15);
        border-color: var(--primary-green);
    }

    /* خلفيات ثانوية (أخضر عشبي فاتح) */
    .soft-bg {
        background-color: var(--soft-green);
        border-radius: 16px;
        padding: 15px;
        color: var(--primary-green);
        font-weight: 800;
    }

    /* الأزرار التدريجية (Gradients) */
    .stButton>button {
        font-weight: 900;
        font-size: 1.4rem;
        border-radius: 16px;
        height: 70px;
        border: none;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* الزر الرئيسي (الأخضر العميق المتدرج) */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-green) 0%, #008250 100%);
        color: white;
    }
    
    /* الزر الثانوي (الأحمر النابض) */
    .stButton>button[kind="secondary"] {
        background: linear-gradient(135deg, var(--accent-red) 0%, #ff5f6d 100%);
        color: white;
    }

    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%);
        border-left: 1px solid #e2e8f0;
    }

    /* اللوج (أسفل الشريط الجانبي) */
    .sidebar-logs {
        background: #111827; /* رمادي فحمي للتباين */
        color: var(--soft-green);
        border-radius: 16px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        height: 200px;
        overflow-y: auto;
        direction: ltr;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
        border: 1px solid var(--primary-green);
    }
    
    .log-entry { margin-bottom: 8px; border-bottom: 1px solid #374151; padding-bottom: 4px; }

    /* الفوتر */
    .footer-bar {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: var(--primary-green);
        color: white;
        padding: 20px;
        text-align: center;
        font-weight: 900;
        font-size: 1.1rem;
        z-index: 1000;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. إعداد البيانات
# ==========================================

def log_event(message):
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] [INFO] {message}"
    st.session_state.logs.append(entry)

def initialize_session_state():
    if 'users' not in st.session_state:
        st.session_state.users = [
            {"username": "teacher", "password": "123", "name": "أ. د. كمال", "role": "معلم"},
            {"username": "student", "password": "123", "name": "الطالب سعيد", "role": "طالب"}
        ]
        log_event("تم تحميل النظام")

    if 'lessons' not in st.session_state:
        st.session_state.lessons = [
            {
                "id": 1, 
                "title": "التفاضل والتكامل: فهم المشتقات", 
                "subject": "رياضيات", 
                "instructor": "أ. د. كمال", 
                "video_url": "https://www.youtube.com/watch?v=WUvTyaaNkzM",
                "description": "شرح عميق وشامل لقوانين التفاضل والتكامل مع تطبيقات هندسية.",
                "duration": "45 دقيقة"
            },
            {
                "id": 2, 
                "title": "تاريخ الجزائر: نضال الاستقلال", 
                "subject": "تاريخ", 
                "instructor": "أ. د. كمال", 
                "video_url": "https://www.youtube.com/watch?v=G8Gp9iG7S_A",
                "description": "وثائق تاريخية حصرية حول ثورة نوفمبر.",
                "duration": "60 دقيقة"
            }
        ]
        log_event("تم تحميل المكتبة")

    if 'logs' not in st.session_state:
        st.session_state.logs = []
    if 'progress' not in st.session_state:
        st.session_state.progress = []
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

announcements_data = [
    {"title": "مؤتمر 2026 للابتكار", "desc": "أكبر حدث تقني في المنطقة.", "img": "https://images.unsplash.com/photo-1544531586-fde5298cdd40?w=800"},
    {"title": "قائمة الشرف", "desc": "تهنئ إدارة المدرسة المتفوقين.", "img": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800"},
]

# ==========================================
# 3. دوال مساعدة
# ==========================================

def extract_youtube_id(url):
    try:
        pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        return re.search(pattern, url).group(1)
    except:
        return None

# ==========================================
# 4. الصفحات (Pages)
# ==========================================

def show_login():
    st.markdown("<div class='lms-card' style='max-width: 700px; margin: 120px auto; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #006241;'>مرحباً بعودتك 🇩🇿</h1>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 دخول", "📝 تسجيل"])
    
    with tab_login:
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")
            
            if st.form_submit_button("تسجيل الدخول", use_container_width=True, type="primary"):
                if username == "admin" and password == "123":
                    st.session_state['user'] = {"username": "admin", "name": "المدير العام", "role": "مدير"}
                    st.session_state['logged_in'] = True
                    log_event("دخول: المدير العام")
                    st.success("أهلاً بك أيها المدير")
                    time.sleep(1)
                    st.rerun()
                else:
                    user = next((u for u in st.session_state.users if u['username'] == username and u['password'] == password), None)
                    if user:
                        st.session_state['user'] = user
                        st.session_state['logged_in'] = True
                        log_event(f"دخول: {username}")
                        st.success(f"مرحباً {user['name']}")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("بيانات خاطئة")

    with tab_signup:
        with st.form("signup_form"):
            col1, col2 = st.columns(2)
            new_name = col1.text_input("الاسم الكامل")
            new_role = col2.selectbox("نوع الحساب", ["طالب", "معلم"])
            new_username = col1.text_input("اسم المستخدم")
            new_password = col2.text_input("كلمة المرور", type="password")
            
            if st.form_submit_button("إنشاء الحساب", use_container_width=True, type="primary"):
                if not any(u['username'] == new_username for u in st.session_state.users):
                    st.session_state.users.append({
                        "username": new_username, "password": new_password,
                        "name": new_name, "role": new_role
                    })
                    log_event(f"تسجيل {new_role}")
                    st.success("تم إنشاء الحساب")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("الاسم مستخدم")

    st.markdown("</div>", unsafe_allow_html=True)

def show_admin_dashboard():
    st.markdown("<div class='lms-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #006241;'>📊 لوحة المدير</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("المستخدمين", len(st.session_state.users))
    c2.metric("الدروس", len(st.session_state.lessons))
    c3.metric("حالة النظام", "ممتاز")
    st.markdown("</div>", unsafe_allow_html=True)

def show_teacher_dashboard():
    st.markdown("<div class='lms-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #006241;'>👨‍🏫 منصة المعلم</h2>", unsafe_allow_html=True)
    
    with st.form("add_lesson"):
        col1, col2 = st.columns(2)
        title = col1.text_input("عنوان الدرس")
        subject = col2.selectbox("المادة", ["رياضيات", "علوم الحاسوب", "تاريخ"])
        video_url = st.text_input("رابط الفيديو")
        
        if st.form_submit_button("نشر الدرس", use_container_width=True, type="primary"):
            if title and video_url:
                st.session_state.lessons.append({
                    "id": len(st.session_state.lessons) + 1,
                    "title": title, "subject": subject,
                    "instructor": st.session_state.user['name'],
                    "video_url": video_url
                })
                log_event("إضافة درس")
                st.success("تم النشر")
                st.rerun()
    
    for lesson in st.session_state.lessons:
        if lesson['instructor'] == st.session_state.user['name']:
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"<h3>{lesson['title']}</h3>", unsafe_allow_html=True)
            if col2.button("🗑️ حذف", key=f"del_{lesson['id']}", type="secondary"):
                st.session_state.lessons.remove(lesson)
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def show_student_dashboard():
    st.markdown("<div class='lms-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #006241;'>🎓 بوابة الطالب</h2>", unsafe_allow_html=True)
    
    prog = len(st.session_state.progress) / len(st.session_state.lessons) * 100 if st.session_state.lessons else 0
    
    tab1, tab2 = st.tabs(["📚 المكتبة", "📈 التقدم"])
    
    with tab1:
        if 'selected_lesson' in st.session_state:
            show_lesson_player(st.session_state['selected_lesson'])
        else:
            for lesson in st.session_state.lessons:
                yt_id = extract_youtube_id(lesson['video_url'])
                thumb = f"https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg" if yt_id else "https://placehold.co/800x450/006241/FFFFFF?text=Lesson+Preview"
                
                st.markdown(f"""
                <div class='lms-card' style='padding: 0; overflow: hidden;'>
                    <img src="{thumb}" style="width:100%; height: 250px; object-fit: cover;">
                    <div style="padding: 25px;">
                        <h3>{lesson['title']}</h3>
                        <p>{lesson.get('description', '')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"▶️ مشاهدة", key=f"watch_{lesson['id']}", use_container_width=True, type="primary"):
                    st.session_state['selected_lesson'] = lesson
                    st.rerun()

    with tab2:
        st.markdown(f"<h1 style='text-align: center; color: #006241;'>{int(prog)}%</h1>", unsafe_allow_html=True)
        st.progress(prog / 100)
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_lesson_player(lesson):
    st.markdown(f"<h1>{lesson['title']}</h1>", unsafe_allow_html=True)
    if st.button("⬅️ عودة"):
        del st.session_state['selected_lesson']
        if lesson['id'] not in st.session_state.progress:
            st.session_state.progress.append(lesson['id'])
            log_event(f"مشاهدة: {lesson['title']}")
        st.rerun()
        
    yt_id = extract_youtube_id(lesson['video_url'])
    if yt_id:
        components.iframe(f"https://www.youtube.com/embed/{yt_id}", height=500)
    else:
        st.warning("خطأ في الفيديو")

# ==========================================
# 5. التشغيل الرئيسي (Main Loop)
# ==========================================

def main():
    initialize_session_state()
    
    if not st.session_state['logged_in']:
        show_login()
    else:
        # الشريط الجانبي
        with st.sidebar:
            # 1. معلومات المستخدم
            st.markdown(f"<h2 style='color: #006241;'>{st.session_state.user['name']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 1.5rem;'>📌 {st.session_state.user['role']}</p>", unsafe_allow_html=True)
            st.divider()
            
            # 2. القائمة
            st.markdown("### 🏠 القائمة")
            st.write("- الرئيسية")
            st.write("- المكتبة")
            st.write("- الإعدادات")
            st.divider()
            
            # 3. زر الخروج (فوق اللوج)
            if st.button("🚪 تسجيل الخروج", use_container_width=True, type="secondary"):
                st.session_state['logged_in'] = False
                if 'selected_lesson' in st.session_state: del st.session_state['selected_lesson']
                log_event("خروج")
                st.rerun()
            
            st.divider()
            
            # 4. اللوج (أسفل الخروج)
            with st.container():
                logs_html = "<div class='sidebar-logs'>"
                logs_html += "<div style='color: white; font-weight: bold; margin-bottom: 10px;'>📜 سجل النظام</div>"
                for log in reversed(st.session_state.logs[-5:]):
                    logs_html += f"<div class='log-entry'>{log}</div>"
                logs_html += "</div>"
                st.markdown(logs_html, unsafe_allow_html=True)
        
        # منطق العرض
        role = st.session_state.user['role']
        if role == 'مدير':
            show_admin_dashboard()
        elif role == 'معلم':
            show_teacher_dashboard()
        elif role == 'طالب':
            show_student_dashboard()

    # الفوتر
    st.markdown("""
    <div class="footer-bar">
        🇩🇿 <strong>Innovative LMS</strong> - منصة التعليم الذكية | بني مسوس | الماستر 01 | إشراف: د. بن عاشور رضا
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
