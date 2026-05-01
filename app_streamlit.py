"""
🇩🇿 SmartEdu Algeria V13.0 - Responsive Dark LMS
المميزات الجديدة:
1. تصميم متجاوب 100% (Mobile Friendly).
2. خلفية داكنة مريحة (Dark Theme).
3. إزالة البطاقات الفارغة وإضافة Diaporama للدخول.
4. خطوط ضخمة وواضحة للغاية.
5. إيكونات (Icons) في كل مكان.
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
# 1. إعدادات CSS (Dark Responsive Theme)
# ==========================================

st.set_page_config(
    page_title="Global LMS - Dark Mode",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700;900&display=swap');
    
    /* الخلفية الداكنة الاحترافية */
    .stApp {
        background-color: #0f172a; /* Dark Slate */
        color: #f1f5f9;
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        font-size: 1.2rem; /* نص ضخم افتراضي */
    }

    /* إخفاء العناصر الافتراضية */
    #MainMenu, footer {visibility: hidden;}

    /* العناوين ضخمة جداً */
    h1, h2, h3, h4 {
        color: #38bdf8; /* لون سماوي فاتح للتباين */
        font-weight: 900;
    }
    h1 { font-size: 3rem; }
    h2 { font-size: 2.5rem; }

    /* تسميات المدخلات كبيرة وواضحة */
    label {
        font-size: 1.4rem;
        font-weight: 700;
        color: #cbd5e1;
    }

    /* البطاقات الداكنة */
    .dark-card {
        background: #1e293b;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #334155;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        transition: all 0.3s;
    }

    .dark-card:hover {
        border-color: #38bdf8;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
    }

    /* الأزرار الكبيرة */
    .stButton>button {
        font-weight: 900;
        font-size: 1.3rem;
        border-radius: 12px;
        height: 65px;
        border: none;
        text-transform: uppercase;
    }
    
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4);
    }

    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        background: #1e293b;
        border-left: 1px solid #334155;
    }

    /* اللوج في أسفل الشريط الجانبي */
    .sidebar-logs {
        margin-top: auto;
        background: #0f172a;
        border-top: 2px solid #38bdf8;
        padding: 15px;
        border-radius: 12px 12px 0 0;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        height: 150px;
        overflow-y: auto;
        direction: ltr;
        color: #4ade80;
    }

    /* الشريط السفلي */
    .footer-bar {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: #020617;
        color: #94a3b8;
        padding: 15px;
        text-align: center;
        font-weight: 700;
        z-index: 1000;
        border-top: 1px solid #334155;
    }

    /* Diaporama للدخول (خلفية متحركة) */
    .login-diapo {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        z-index: -1;
        background: url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1920&q=80');
        background-size: cover;
        background-position: center;
        opacity: 0.3;
        animation: zoomEffect 20s infinite alternate;
    }
    
    @keyframes zoomEffect {
        0% { transform: scale(1); }
        100% { transform: scale(1.1); }
    }

    /* تحسينات الموبايل */
    @media (max-width: 768px) {
        .stButton>button { height: 50px; font-size: 1.1rem; }
        h1 { font-size: 2rem; }
        .sidebar-logs { display: none; } /* إخفاء اللوج في الموبايل لتوفير المساحة */
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. إعداد البيانات والنظام
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
        log_event("تم تحميل قاعدة البيانات")

    if 'lessons' not in st.session_state:
        st.session_state.lessons = [
            {
                "id": 1, 
                "title": "التفاضل والتكامل: الأساسيات المتقدمة", 
                "subject": "رياضيات", 
                "instructor": "أ. د. كمال", 
                "video_url": "https://www.youtube.com/watch?v=WUvTyaaNkzM",
                "description": "شرح مفصل ومتقدم لمفاهيم التفاضل والتكامل مع أمثلة عملية.",
                "duration": "45 دقيقة"
            },
            {
                "id": 2, 
                "title": "تاريخ الجزائر: الثورة التحريرية", 
                "subject": "تاريخ", 
                "instructor": "أ. د. كمال", 
                "video_url": "https://www.youtube.com/watch?v=G8Gp9iG7S_A",
                "description": "سرد تاريخي شامل لأحداث الثورة الجزائرية المجيدة.",
                "duration": "60 دقيقة"
            },
            {
                "id": 3, 
                "title": "الذكاء الاصطناعي ومستقبل التكنولوجيا", 
                "subject": "علوم الحاسوب", 
                "instructor": "أ. د. كمال", 
                "video_url": "https://www.youtube.com/watch?v=aircAruvnKk",
                "description": "استكشاف عالم الذكاء الاصطناعي والآلة التعلمة بأسلوب مبسط.",
                "duration": "90 دقيقة"
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
    {"title": "المؤتمر الدولي للتعليم الرقمي", "desc": "شارك معنا في أكبر حدث تعليمي تقني.", "img": "https://images.unsplash.com/photo-1544531586-fde5298cdd40?w=800"},
    {"title": "نتائج التفوق الفصلي", "desc": "تهنئ إدارة المدرسة الطلاب المتفوقين لهذا الفصل.", "img": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800"},
    {"title": "توظيف أساتذة جدد", "desc": "تم الإعلان عن فتح باب التوظيف للسنة القادمة.", "img": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"}
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
    # خلفية الديابو (بدون بطاقة فوقها)
    st.markdown("<div class='login-diapo'></div>", unsafe_allow_html=True)
    
    # حاوية الدخول
    col_center = st.columns([1, 2, 1])
    with col_center[1]:
        # العناوين الكبيرة
        st.markdown("<h1 style='text-align: center; color: #38bdf8; margin-bottom: 10px;'>مرحباً بعودتك 🇩🇿</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: white; margin-top: 0;'>المنصة الأكاديمية العالمية</h2>", unsafe_allow_html=True)
        
        tab_login, tab_signup = st.tabs(["🔐 تسجيل الدخول", "📝 إنشاء حساب جديد"])
        
        with tab_login:
            with st.form("login_form"):
                st.markdown("### 👤 بيانات الدخول")
                username = st.text_input("اسم المستخدم", label_visibility="visible")
                password = st.text_input("كلمة المرور", type="password", label_visibility="visible")
                
                if st.form_submit_button("تسجيل الدخول للنظام", use_container_width=True, type="primary"):
                    # فحص المدير
                    if username == "admin" and password == "123":
                        st.session_state['user'] = {"username": "admin", "name": "المدير العام", "role": "مدير"}
                        st.session_state['logged_in'] = True
                        log_event("دخول: المدير العام")
                        st.success("أهلاً بك أيها المدير")
                        time.sleep(1)
                        st.rerun()
                    # فحص المستخدمين
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
                            st.error("خطأ في البيانات")

        with tab_signup:
            with st.form("signup_form"):
                st.markdown("### 🆕 حساب جديد")
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
                        log_event(f"تسجيل {new_role}: {new_name}")
                        st.success("تم إنشاء الحساب بنجاح")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("اسم المستخدم موجود")

def show_admin_dashboard():
    st.markdown("### 📊 لوحة القيادة التنفيذية")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("المستخدمين", len(st.session_state.users), "👥")
    c2.metric("الدروس", len(st.session_state.lessons), "📚")
    c3.metric("حالة النظام", "مستقر", "🟢")
    c4.metric("الزوار", "1,240", "👁️")
    
    st.divider()
    
    col_chart, col_info = st.columns([2, 1])
    with col_chart:
        st.markdown("### 📈 نمو النشاط")
        chart_data = pd.DataFrame({'الشهر': ['يناير', 'فبراير', 'مارس'], 'النشاط': [100, 150, 200]})
        st.line_chart(chart_data.set_index('الشمار'), use_container_width=True, color="#38bdf8")
    
    with col_info:
        st.markdown("### 📋 سجل العمليات")
        for log in st.session_state.logs[-5:]:
            st.text(f"• {log}")

def show_teacher_dashboard():
    st.markdown("### 👨‍🏫 منصة المعلم")
    
    with st.form("add_lesson"):
        st.markdown("#### ➕ إضافة درس")
        col1, col2 = st.columns(2)
        title = col1.text_input("عنوان الدرس")
        subject = col2.selectbox("المادة", ["رياضيات", "علوم الحاسوب", "تاريخ", "فيزياء"])
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
    
    st.divider()
    for lesson in st.session_state.lessons:
        if lesson['instructor'] == st.session_state.user['name']:
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"**{lesson['title']}**")
            if col2.button("🗑️", key=f"del_{lesson['id']}", type="secondary"):
                st.session_state.lessons.remove(lesson)
                st.rerun()

def show_student_dashboard():
    st.markdown("### 🎓 بوابة الطالب")
    
    prog = len(st.session_state.progress) / len(st.session_state.lessons) * 100 if st.session_state.lessons else 0
    
    tab1, tab2, tab3, tab4 = st.tabs(["📢 الإعلانات", "📚 المكتبة", "📈 تقدمك", "🤖 المساعد"])
    
    # 1. الإعلانات
    with tab1:
        for ann in announcements_data:
            st.markdown(f"""
            <div class='dark-card'>
                <img src="{ann['img']}" style="width:100%; height:200px; object-fit:cover; border-radius:10px;">
                <h2>{ann['title']}</h2>
                <p>{ann['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    # 2. المكتبة (بدون بطاقات فارغة فوق الصور)
    with tab2:
        if 'selected_lesson' in st.session_state:
            show_lesson_player(st.session_state['selected_lesson'])
        else:
            for lesson in st.session_state.lessons:
                yt_id = extract_youtube_id(lesson['video_url'])
                thumb = f"https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg" if yt_id else "https://placehold.co/800x450/1e293b/38bdf8?text=No+Preview"
                
                # عرض مباشر للصورة بدون مغلف فارغ
                st.markdown(f"""
                <div class='dark-card'>
                    <img src="{thumb}" style="width:100%; border-radius:12px; margin-bottom:15px;">
                    <h2 style="margin-top:0;">{lesson['title']}</h2>
                    <p>{lesson.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"▶️ مشاهدة: {lesson['title']}", key=f"watch_{lesson['id']}", use_container_width=True, type="primary"):
                    st.session_state['selected_lesson'] = lesson
                    st.rerun()

    # 3. التقدم
    with tab3:
        st.markdown(f"<h1 style='text-align: center;'>{int(prog)}%</h1>", unsafe_allow_html=True)
        st.progress(prog / 100)

    # 4. المساعد
    with tab4:
        st.chat_input("اسألني...")

def show_lesson_player(lesson):
    st.title(lesson['title'])
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
        st.warning("لا يمكن عرض الفيديو")

# ==========================================
# 5. التشغيل الرئيسي
# ==========================================

def main():
    initialize_session_state()
    
    if not st.session_state['logged_in']:
        show_login()
    else:
        # الشريط الجانبي
        with st.sidebar:
            st.markdown(f"<h2 style='color: #38bdf8;'>{st.session_state.user['name']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:1.3rem;'>{st.session_state.user['role']}</p>", unsafe_allow_html=True)
            st.divider()
            
            # القائمة (تتبسط لكل الأدوار)
            st.markdown("### 🏠 الرئيسية")
            st.divider()
            
            # اللوج في الأسفل
            st.markdown("<div style='flex-grow: 1; min-height: 20px;'></div>", unsafe_allow_html=True)
            with st.container():
                st.markdown("<div class='sidebar-logs'>", unsafe_allow_html=True)
                for log in reversed(st.session_state.logs[-5:]):
                    st.text(log)
                st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("🚪 خروج", use_container_width=True):
                st.session_state['logged_in'] = False
                if 'selected_lesson' in st.session_state: del st.session_state['selected_lesson']
                log_event("خروج")
                st.rerun()
        
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
        🇩🇿 <strong>Global LMS</strong> - منصة التعليم الذكية | بني مسوس | الماستر 01 | إشراف: د. بن عاشور رضا
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
