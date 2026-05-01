"""
🇩🇿 SmartEdu Algeria V13.0 (Restored & Modified)
المميزات المستعادة:
1. تصميم متجاوب (Responsive) لجميع الشاشات.
2. ديابو (Diaporama) في صفحة الدخول.
3. حذف البطاقات الفارغة.

التعديلات المطلوبة:
1. تسجيل الخروج فوق اللوج (Logs).
2. نصوص ضخمة جداً (Large & Bold).
3. ألوان "Innovative Algeria" (أخضر عميق، أحمر نابض).
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
# 1. إعدادات CSS (Innovative Algeria Palette + Big Text)
# ==========================================

st.set_page_config(
    page_title="Global LMS - V13",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700;900&display=swap');
    
    /* تطبيق لوحة الألوان الجديدة */
    :root {
        --primary-green: #006241; /* أخضر عميق */
        --accent-red: #E32636;    /* أحمر نابض */
        --bg-white: #F8FAFC;       /* خلفية بيضاء صافية */
        --text-dark: #1E293B;      /* نص داكن للقراءة */
        --soft-green: #D1FAE5;     /* أخضر عشبي فاتح */
    }

    .stApp {
        background-color: var(--bg-white);
        color: var(--text-dark);
        font-family: 'Tajawal', sans-serif;
        font-size: 1.5rem; /* نص ضخم جداً */
        font-weight: 700;      /* عريض افتراضي */
        direction: rtl;
    }

    /* إخفاء العناصر */
    #MainMenu, footer {visibility: hidden;}

    /* العناوين الضخمة جداً */
    h1, h2, h3, h4 {
        color: var(--primary-green);
        font-weight: 900; /* أقصى درجة العرض */
    }
    
    h1 { font-size: 4rem; letter-spacing: -1px; line-height: 1.1; }
    h2 { font-size: 3rem; }
    h3 { font-size: 2.2rem; }

    /* تسميات المدخلات */
    label {
        font-size: 1.6rem;
        font-weight: 900;
        color: var(--text-dark);
    }

    /* البطاقات (Modern Soft Cards) */
    .lms-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 25px rgba(0, 98, 65, 0.08); /* ظل خفيف أخضر */
        border: 1px solid #e2e8f0;
        margin-bottom: 25px;
        transition: all 0.3s;
    }

    .lms-card:hover {
        border-color: var(--primary-green);
        box-shadow: 0 15px 35px rgba(0, 98, 65, 0.15);
    }

    /* الأزرار */
    .stButton>button {
        font-weight: 900;
        font-size: 1.4rem;
        border-radius: 16px;
        height: 70px;
        border: none;
        text-transform: uppercase;
    }
    
    /* الزر الرئيسي (أخضر عميق) */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-green) 0%, #008250 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 98, 65, 0.3);
    }
    
    /* زر الخروج/الثانوي (أحمر نابض) */
    .stButton>button[kind="secondary"] {
        background: linear-gradient(135deg, var(--accent-red) 0%, #ff5f6d 100%);
        color: white;
    }

    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        background: white;
        border-left: 1px solid #e2e8f0;
    }

    /* اللوج في الأسفل */
    .sidebar-logs {
        background: #1e293b; /* خلفية داكنة للتباين */
        color: #4ade80; /* نص أخضر زمردي */
        border-top: 2px solid var(--primary-green);
        border-radius: 12px 12px 0 0;
        padding: 20px;
        font-family: 'Courier New', monospace;
        font-size: 1rem;
        height: 180px;
        overflow-y: auto;
        direction: ltr;
    }
    
    .log-entry { margin-bottom: 8px; border-bottom: 1px solid #334155; padding-bottom: 2px; }

    /* الفوتر */
    .footer-bar {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: var(--primary-green);
        color: white;
        padding: 15px;
        text-align: center;
        font-weight: 800;
        font-size: 1.2rem;
        z-index: 1000;
    }

    /* Diaporama للدخول */
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
        opacity: 0.15; /* شفافية خفيفة للنص */
        animation: zoomEffect 20s infinite alternate;
    }
    
    @keyframes zoomEffect {
        0% { transform: scale(1); }
        100% { transform: scale(1.1); }
    }
    
    /* تخصيص الموبايل */
    @media (max-width: 768px) {
        h1 { font-size: 2.5rem; }
        .sidebar-logs { display: none; }
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
                "description": "شرح مفصل ومتقدم لمفاهيم النهايات والمشتقات.",
                "duration": "45 دقيقة"
            },
            {
                "id": 2, 
                "title": "تاريخ الجزائر الحديث والمعاصر", 
                "subject": "تاريخ", 
                "instructor": "أ. د. كمال", 
                "video_url": "https://www.youtube.com/watch?v=G8Gp9iG7S_A",
                "description": "نظرة معمقة على تاريخ الثورة.",
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
    {"title": "المؤتمر الدولي للتعليم الرقمي", "desc": "شارك معنا في المؤتمر الدولي.", "img": "https://images.unsplash.com/photo-1544531586-fde5298cdd40?w=800"},
    {"title": "قائمة التفوق", "desc": "تهنئ إدارة المدرسة الطلاب المتفوقين.", "img": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800"}
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
# 4. الصفحات
# ==========================================

def show_login():
    # خلفية الديابو
    st.markdown("<div class='login-diapo'></div>", unsafe_allow_html=True)
    
    # حاوية الدخول (بدون بطاقة فارغة فوقها)
    col_center = st.columns([1, 2, 1])
    with col_center[1]:
        st.markdown("<h1 style='text-align: center; color: #006241;'>مرحباً بعودتك 🇩🇿</h1>", unsafe_allow_html=True)
        
        tab_login, tab_signup = st.tabs(["🔐 تسجيل الدخول", "📝 إنشاء حساب"])
        
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
                        log_event(f"تسجيل {new_role}: {new_name}")
                        st.success("تم إنشاء الحساب")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("الاسم مستخدم")

def show_admin_dashboard():
    st.header("📊 لوحة القيادة")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("المستخدمين", len(st.session_state.users))
    c2.metric("الدروس", len(st.session_state.lessons))
    c3.metric("حالة النظام", "مستقر")
    c4.metric("الزوار", "1,240")
    
    st.divider()
    st.dataframe(st.session_state.users)

def show_teacher_dashboard():
    st.header("👨‍🏫 منصة المعلم")
    
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
            col1.markdown(f"**{lesson['title']}**")
            if col2.button("🗑️", key=f"del_{lesson['id']}", type="secondary"):
                st.session_state.lessons.remove(lesson)
                st.rerun()

def show_student_dashboard():
    st.header("🎓 بوابة الطالب")
    
    prog = len(st.session_state.progress) / len(st.session_state.lessons) * 100 if st.session_state.lessons else 0
    
    tab1, tab2, tab3, tab4 = st.tabs(["📢 الإعلانات", "📚 المكتبة", "📈 التقدم", "🤖 المساعد"])
    
    with tab1:
        for ann in announcements_data:
            st.markdown(f"""
            <div class='lms-card' style='padding:0; overflow:hidden;'>
                <img src="{ann['img']}" style="width:100%; height:200px; object-fit:cover;">
                <div style="padding:20px;">
                    <h2>{ann['title']}</h2>
                    <p>{ann['desc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    with tab2:
        if 'selected_lesson' in st.session_state:
            show_lesson_player(st.session_state['selected_lesson'])
        else:
            for lesson in st.session_state.lessons:
                yt_id = extract_youtube_id(lesson['video_url'])
                thumb = f"https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg" if yt_id else "https://placehold.co/800x450/006241/FFFFFF?text=Lesson+Preview"
                
                # عرض مباشر بدون بطاقة فارغة
                st.markdown(f"""
                <div class='lms-card' style='padding:0;'>
                    <img src="{thumb}" style="width:100%; border-radius:12px; margin-bottom:20px;">
                    <h2 style="margin-top:0;">{lesson['title']}</h2>
                    <p>{lesson.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"▶️ مشاهدة: {lesson['title']}", key=f"watch_{lesson['id']}", use_container_width=True, type="primary"):
                    st.session_state['selected_lesson'] = lesson
                    st.rerun()

    with tab3:
        st.markdown(f"<h1 style='text-align: center; color: #006241;'>{int(prog)}%</h1>", unsafe_allow_html=True)
        st.progress(prog / 100)

    with tab4:
        st.chat_input("اكتب سؤالك...")

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
        with st.sidebar:
            st.markdown(f"<h2 style='color: #006241;'>{st.session_state.user['name']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:1.5rem;'>📌 {st.session_state.user['role']}</p>", unsafe_allow_html=True)
            st.divider()
            
            # القائمة
            st.write("**القائمة:**")
            st.write("- الرئيسية")
            st.write("- المكتبة")
            st.write("- التقدم")
            st.divider()
            
            # 1. زر الخروج (موجود فوق اللوج)
            if st.button("🚪 تسجيل الخروج", use_container_width=True, type="secondary"):
                st.session_state['logged_in'] = False
                if 'selected_lesson' in st.session_state: del st.session_state['selected_lesson']
                log_event("خروج")
                st.rerun()
            
            st.divider()
            
            # 2. اللوج (في الأسفل)
            with st.container():
                logs_html = "<div class='sidebar-logs'>"
                logs_html += "<div style='font-weight: bold; color: white; margin-bottom:10px;'>📜 سجل النظام (Logs)</div>"
                for log in reversed(st.session_state.logs[-8:]):
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
            # تبسيط عرض الطالب في الجانب فقط
            if 'selected_lesson' in st.session_state:
                show_lesson_player(st.session_state['selected_lesson'])
            else:
                st.write("اختر درساً من المكتبة")
                for lesson in st.session_state.lessons:
                    yt_id = extract_youtube_id(lesson['video_url'])
                    thumb = f"https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg"
                    st.image(thumb, use_column_width=True)
                    if st.button(f"▶️ {lesson['title']}", key=f"side_{lesson['id']}", use_container_width=True, type="primary"):
                        st.session_state['selected_lesson'] = lesson
                        st.rerun()
                    st.divider()

    # الفوتر
    st.markdown(f"""
    <div class="footer-bar">
        🇩🇿 <strong>Global LMS</strong> - منصة التعليم الذكية | بني مسوس | الماستر 01 | إشراف: د. بن عاشور رضا
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
