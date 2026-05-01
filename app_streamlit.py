"""
منصة التعليم الذكية
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
# 1. إعدادات CSS
# ==========================================

st.set_page_config(
    page_title="منصة التعليم الذكية",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght:800;900&display=swap');
    
    /* تطبيق لوحة الألوان */
    :root {
        --primary-green: #006241; /* أخضر عميق */
        --accent-red: #E32636;    /* أحمر نابض */
        --bg-white: #F8FAFC;       /* خلفية بيضاء */
        --text-dark: #1E293B;      /* نص داكن */
        --soft-green: #D1FAE5;     /* أخضر عشبي */
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

    /* العناوين الضخمة */
    h1, h2, h3, h4 {
        color: var(--primary-green);
        font-weight: 900;
    }
    h1 { font-size: 4rem; letter-spacing: -1px; line-height: 1.1; }
    h2 { font-size: 3rem; }

    /* تسميات المدخلات */
    label { font-size: 1.6rem; font-weight: 800; color: var(--text-dark); }

    /* البطاقات العصرية */
    .lms-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 25px rgba(0, 98, 65, 0.08);
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
    
    /* الزر الرئيسي */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-green) 0%, #008250 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 98, 65, 0.3);
    }
    
    /* زر الخروج */
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
        background: #1e293b;
        color: #4ade80;
        border-top: 2px solid var(--primary-green);
        border-radius: 12px 12px 0 0;
        padding: 20px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
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
        z-index: 1000;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
    }

    /* Diaporama */
    .login-bg {
        position: fixed;
        top: 0; left: 0;
        width: 100%;
        height: 100%;
        background: url('https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1920&q=80'); /* صورة أخرى */
        background-size: cover;
        background-position: center;
        z-index: -9999; /* خلف everything */
        opacity: 0.2; /* شفافية واضحة */
    }
    
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
        log_event("تم تحميل النظام")

    if 'lessons' not in st.session_state:
        st.session_state.lessons = [
            {
                "id": 1, 
                "title": "التفاضل والتكامل: الأساسيات", 
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
    
    if 'current_view' not in st.session_state:
        st.session_state['current_view'] = 'home'

announcements_data = [
    {"title": "المؤتمر الدولي للتعليم", "desc": "أكبر حدث تقني في المنطقة.", "img": "https://images.unsplash.com/photo-1544531586-fde5298cdd40?w=800"},
    {"title": "قائمة التفوق", "desc": "تهنئ إدارة المدرسة المتفوقين.", "img": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800"}
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
    # 1. تخصيص CSS 
    st.markdown("""
    <style>
    div[data-testid="stApp"] { background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)
    
    # 2. إضافة خلفية الصورة
    st.markdown("<div class='login-bg'></div>", unsafe_allow_html=True)
    
    # 3. حاوية الدخول
    col_center = st.columns([1, 2, 1])
    with col_center[1]:
        st.markdown("<h1 style='color: #006241;'>مرحباً بعودتك</h1>", unsafe_allow_html=True)
        
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
                        log_event(f"تسجيل {new_role}")
                        st.success("تم إنشاء الحساب")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("الاسم مستخدم")
        st.markdown("</div>", unsafe_allow_html=True)

def show_admin_dashboard():
    st.header("📊 لوحة القيادة")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("المستخدمين", len(st.session_state.users))
    c2.metric("الدروس", len(st.session_state.lessons))
    c3.metric("حالة النظام", "مستقر", "🟢")
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
            if col2.button("🗑️ حذف", key=f"del_{lesson['id']}", type="secondary"):
                st.session_state.lessons.remove(lesson)
                st.rerun()

def show_student_dashboard():
    st.header("🎓 بوابة الطالب")
    
    prog = len(st.session_state.progress) / len(st.session_state.lessons) * 100 if st.session_state.lessons else 0
    
    tab1, tab2, tab3, tab4 = st.tabs(["📢 الإعلانات", "📚 المكتبة", "📈 التقدم", "المساعد"])
    
    with tab1:
        for ann in announcements_data:
            st.markdown(f"""
            <div class='lms-card'>
                <img src="{ann['img']}" style="width:100%; height:200px; object-fit:cover; border-radius:12px;">
                <h2>{ann['title']}</h2>
                <p>{ann['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    with tab2:
        if 'selected_lesson' in st.session_state:
            show_lesson_player(st.session_state['selected_lesson'])
        else:
            for lesson in st.session_state.lessons:
                yt_id = extract_youtube_id(lesson['video_url'])
                thumb = f"https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg" if yt_id else "https://placehold.co/800x450/006241/FFFFFF?text=Lesson+Preview"
                
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
        st.warning("خطأ في الفيديو")

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
            st.markdown(f"<h2 style='color: #006241;'>{st.session_state.user['name']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:1.5rem;'>📌 {st.session_state.user['role']}</p>", unsafe_allow_html=True)
            st.divider()
            
            # القائمة التفاعلية (الأزرار)


            st.markdown("### 🏠 الرئيسية")
            
            st.divider()
            
            # 1. زر الخروج (فوق اللوج)
            if st.button("🚪 تسجيل الخروج", use_container_width=True, type="secondary"):
                st.session_state['logged_in'] = False
                if 'selected_lesson' in st.session_state: del st.session_state['selected_lesson']
                log_event("خروج")
                st.rerun()
            
            st.divider()
            
            # 2. اللوج (أسفل الخروج)
            with st.container():
                logs_html = "<div class='sidebar-logs'>"
                logs_html += "<div style='color: white; font-weight: bold; margin-bottom:10px;'>📜 سجل النظام</div>"
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
            if st.session_state['current_view'] == 'home': show_student_dashboard()
            elif st.session_state['current_view'] == 'library': show_student_dashboard()
            elif st.session_state['current_view'] == 'progress': show_student_dashboard()
            elif st.session_state['current_view'] == 'ai': show_student_dashboard()

    # الفوتر
    st.markdown("""
    <div class="footer-bar">
        🇩🇿 <strong>Global LMS</strong> - منصة التعليم الذكية | المدرسة العليا لاساتذة الصم البكم - بني مسوس | من اعداد الطلبة: بن شلالي المعتصم بالله - حلوز اشرف عبد النور | تحت إشراف: د. بن عاشور رضا
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
