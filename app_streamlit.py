"""
🇩🇿 SmartEdu Algeria V9.0 - Final Aesthetic Edition
المميزات الجديدة:
1. نظام تسجيل حساب للطلاب (Sign Up).
2. لوحة Logs سفلية تظهر أخطاء النظام وحالة الاتصال.
3. واجهة فيديو بأسلوب "Diapo" (شرائح) عصري.
4. خلفية خضراء "علم جزائري" مع تأثير تظليل الحواف (Dark Vignette).
5. شريط اعتمادات أكاديمي أسفل الصفحة.
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import re
import datetime

# ==========================================
# 1. إعدادات CSS والتصميم (Dark Algerian Theme)
# ==========================================

st.set_page_config(
    page_title="المنصة التعليمية - بني مسوس",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');
    
    /* الخلفية: خضراء داكنة تتفتح في الوسط (علم جزائري + Vignette) */
    .stApp {
        background: radial-gradient(circle at center, #005c2b 0%, #001a0d 100%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        color: #f0fdf4;
    }

    /* إخفاء العناصر الافتراضية */
    #MainMenu, footer {visibility: hidden;}

    /* البطاقات الزجاجية (Glassmorphism) للوضع الداكن */
    .glass-dark {
        background: rgba(20, 40, 20, 0.7);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
        color: white;
        transition: transform 0.3s;
    }

    .glass-dark:hover {
        transform: translateY(-2px);
        border-color: #00ff88;
    }

    /* واجهة فيديو "ديابو" */
    .video-diapo {
        position: relative;
        width: 100%;
        aspect-ratio: 16/9;
        background: #000;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: all 0.4s ease;
    }

    .video-diapo img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.4s;
    }

    .video-diapo:hover img {
        transform: scale(1.05);
    }

    /* زر التشغيل المضمن */
    .play-overlay {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.4);
        display: flex;
        justify-content: center;
        align-items: center;
        opacity: 0;
        transition: opacity 0.3s;
    }

    .video-diapo:hover .play-overlay {
        opacity: 1;
    }

    .play-btn {
        width: 60px;
        height: 60px;
        background: rgba(0, 255, 136, 0.8);
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 0 20px #00ff88;
    }

    .play-btn::after {
        content: '';
        width: 0; 
        height: 0; 
        border-top: 10px solid transparent;
        border-bottom: 10px solid transparent;
        border-left: 18px solid #000;
        margin-left: 4px;
    }

    /* الأزرار العصرية */
    .stButton>button {
        font-weight: bold;
        border-radius: 30px;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton>button[kind="primary"] {
        background: linear-gradient(90deg, #00ff88, #00cc6a);
        color: #001a0d;
        font-size: 1.1rem;
        height: 50px;
    }

    /* مربع اللوج (Logs) السفلي */
    .logs-panel {
        position: fixed;
        bottom: 70px; /* فوق الفوتر */
        left: 20px;
        width: 300px;
        max-height: 150px;
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid #333;
        border-radius: 10px;
        padding: 10px;
        font-size: 12px;
        font-family: 'Courier New', monospace;
        color: #00ff88;
        overflow-y: auto;
        z-index: 999;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        direction: ltr;
    }

    /* الشريط السفلي */
    .footer-bar {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: rgba(0, 20, 10, 0.95);
        border-top: 2px solid #005c2b;
        padding: 10px;
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        z-index: 1000;
    }

    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #aaa;
    }
    .stTabs [aria-selected="true"] {
        background: #005c2b;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. إدارة السجلات (Logs Manager)
# ==========================================

def log_event(message, status="INFO"):
    """دالة لتسجيل الأحداث وعرضها في اللوج"""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] [{status}] {message}"
    st.session_state.logs.append(entry)
    
    # تحديث واجهة اللوج
    log_container = st.session_state.get('log_container')
    if log_container:
        with log_container.container():
            # عرض آخر 10 رسائل فقط للحفاظ على الأداء
            for msg in reversed(st.session_state.logs[-10:]):
                color = "#ff4444" if "ERROR" in msg else "#00ff88"
                st.markdown(f"<div style='color:{color}; margin-bottom:5px; font-size:12px;'>{msg}</div>", unsafe_allow_html=True)

# ==========================================
# 3. تهيئة البيانات والجلسة (Data & State)
# ==========================================

# تهيئة السجلات
if 'logs' not in st.session_state:
    st.session_state.logs = []

# مستخدمون افتراضيون
if 'users' not in st.session_state:
    st.session_state.users = [
        {"username": "admin", "password": "123", "name": "مدير المنصة", "role": "مدير"},
        {"username": "teacher", "password": "123", "name": "أ. محمد", "role": "معلم"},
        {"username": "student", "password": "123", "name": "الطالب أحمد", "role": "طالب"}
    ]
    log_event("تم تحميل قاعدة بيانات المستخدمين الافتراضية")

# دروس
if 'lessons' not in st.session_state:
    st.session_state.lessons = [
        {"id": 1, "title": "شرح المعادلات", "subject": "رياضيات", "instructor": "أ. محمد", "video_url": "https://www.youtube.com/watch?v=ZcQnJ1vQ2lY"},
        {"id": 2, "title": "تاريخ الجزائر", "subject": "تاريخ", "instructor": "أ. محمد", "video_url": "https://www.youtube.com/watch?v=2nSspGq1ZlY"}
    ]

if 'progress' not in st.session_state:
    st.session_state.progress = []

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ==========================================
# 4. دوال مساعدة (Helpers)
# ==========================================

def extract_youtube_id(url):
    try:
        pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        return re.search(pattern, url).group(1)
    except:
        return None

# ==========================================
# 5. واجهات النظام (Pages)
# ==========================================

def show_login():
    """واجهة الدخول والتسجيل مع التصميم الجديد"""
    
    # تبويب الدخول والتسجيل
    tab_login, tab_signup = st.tabs(["🔐 تسجيل الدخول", "📝 إنشاء حساب جديد"])
    
    with tab_login:
        st.markdown("<div class='glass-dark' style='max-width: 500px; margin: 50px auto; text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: #00ff88;'>مرحباً بعودتك 🇩🇿</h1>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")
            
            if st.form_submit_button("دخول", use_container_width=True, type="primary"):
                user = next((u for u in st.session_state.users if u['username'] == username and u['password'] == password), None)
                if user:
                    st.session_state['user'] = user
                    st.session_state['logged_in'] = True
                    log_event(f"تم تسجيل الدخول للمستخدم: {username}")
                    st.success("تم الدخول بنجاح")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("بيانات غير صحيحة")
                    log_event("فشل تسجيل الدخول: خطأ في البيانات", "ERROR")
        
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_signup:
        st.markdown("<div class='glass-dark' style='max-width: 500px; margin: 50px auto;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #00ff88;'>حساب طالب جديد</h2>", unsafe_allow_html=True)
        
        with st.form("signup_form"):
            new_name = st.text_input("الاسم الكامل")
            new_username = st.text_input("اسم المستخدم")
            new_password = st.text_input("كلمة المرور", type="password")
            
            if st.form_submit_button("تسجيل", use_container_width=True, type="primary"):
                # التحقق من عدم وجود المستخدم مسبقاً
                exists = any(u['username'] == new_username for u in st.session_state.users)
                if exists:
                    st.error("اسم المستخدم مستخدم بالفعل")
                    log_event(f"محاولة تسجيل مستخدم مكرر: {new_username}", "ERROR")
                elif new_name and new_username and new_password:
                    # إضافة المستخدم الجديد
                    st.session_state.users.append({
                        "username": new_username,
                        "password": new_password,
                        "name": new_name,
                        "role": "طالب"
                    })
                    log_event(f"تم تسجيل طالب جديد: {new_name}")
                    st.success("تم إنشاء الحساب بنجاح! يمكنك الدخول الآن.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("يرجى ملء جميع الحقول")
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_teacher_dashboard():
    st.sidebar.title(f"👨‍🏫 {st.session_state.user['name']}")
    
    st.header("إدارة الدروس")
    
    with st.form("add_lesson"):
        st.subheader("➕ إضافة درس")
        c1, c2 = st.columns(2)
        title = c1.text_input("العنوان")
        subject = c2.selectbox("المادة", ["رياضيات", "علوم", "تاريخ"])
        video_url = st.text_input("رابط الفيديو")
        
        if st.form_submit_button("نشر", use_container_width=True):
            if title and video_url:
                st.session_state.lessons.append({
                    "id": len(st.session_state.lessons) + 1,
                    "title": title, "subject": subject,
                    "instructor": st.session_state.user['name'],
                    "video_url": video_url
                })
                st.success("تمت الإضافة")
                log_event(f"أضاف الأستاذ {st.session_state.user['name']} درس جديد: {title}")
                st.rerun()

    # قائمة الدروس مع زر الحذف
    for lesson in st.session_state.lessons:
        if lesson['instructor'] == st.session_state.user['name']:
            with st.container():
                c1, c2 = st.columns([4, 1])
                c1.markdown(f"**{lesson['title']}**")
                if c2.button("🗑️", key=f"del_{lesson['id']}"):
                    st.session_state.lessons.remove(lesson)
                    log_event("تم حذف درس من قبل المعلم", "WARNING")
                    st.rerun()

def show_student_dashboard():
    st.sidebar.title(f"🎓 {st.session_state.user['name']}")
    
    # 5 تبويبات
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📢 الإعلانات", "📚 الدروس", "📈 التقدم", "🤖 المساعد", "💡 نصائح"])
    
    # 1. الإعلانات
    with tab1:
        for i in range(3):
            st.markdown(f"""
            <div class='glass-dark'>
                <h3>حدث تعليمي {i+1}</h3>
                <p>هذا إعلان وهمي لعرض الميزات الجمالية للتصميم...</p>
            </div>
            """, unsafe_allow_html=True)
            
    # 2. الدروس (بأسلوب Diapo)
    with tab2:
        if 'selected_lesson' in st.session_state:
            show_lesson_player(st.session_state['selected_lesson'])
        else:
            for lesson in st.session_state.lessons:
                yt_id = extract_youtube_id(lesson['video_url'])
                thumb = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg" if yt_id else "https://via.placeholder.com/600x340?text=Video"
                
                # تصميم الديابو (Diapo Style)
                st.markdown(f"""
                <div class="video-diapo" style="cursor: pointer;" onclick="document.getElementById('btn_{lesson['id']}').click()">
                    <img src="{thumb}" alt="{lesson['title']}">
                    <div class="play-overlay">
                        <div class="play-btn"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # وصف الدرس
                col1, col2 = st.columns([3, 1])
                col1.markdown(f"<h3>{lesson['title']}</h3>", unsafe_allow_html=True)
                
                # زر مخفي لتفعيل النقر
                if col2.button("مشاهدة", key=f"btn_{lesson['id']}", use_container_width=True):
                    st.session_state['selected_lesson'] = lesson
                    st.rerun()
                
                st.markdown("---")

    # 3. التقدم
    with tab3:
        prog = len(st.session_state.progress) / len(st.session_state.lessons) * 100 if st.session_state.lessons else 0
        st.markdown(f"<h1 style='text-align:center; color: #00ff88;'>{int(prog)}%</h1>", unsafe_allow_html=True)
        st.progress(prog / 100)

    # 4. المساعد
    with tab4:
        st.info("اسألني عن دروسك!")
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        user_input = st.chat_input("اكتب...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            
            response = "هذا رد تجريبي من المساعد الذكي."
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)
            st.rerun()
            
    # 5. نصائح
    with tab5:
        st.success("الصبر مفتاح الفهم")

def show_lesson_player(lesson):
    st.title(lesson['title'])
    if st.button("عودة"):
        del st.session_state['selected_lesson']
        # تسجيل التقدم
        if lesson['id'] not in st.session_state.progress:
            st.session_state.progress.append(lesson['id'])
            log_event(f"شاهد الطالب درس: {lesson['title']}")
        st.rerun()
        
    yt_id = extract_youtube_id(lesson['video_url'])
    if yt_id:
        st.components.v1.iframe(f"https://www.youtube.com/embed/{yt_id}", height=500)

# ==========================================
# 6. التشغيل الرئيسي (Main Loop)
# ==========================================

def main():
    # 1. عرض اللوج (Logs Panel) إذا لم يكن المسجل دخوله، يمكن إظهاره دائماً إذا رغبت
    # سنستخدم st.empty لتحديث اللوج
    log_container = st.empty()
    st.session_state['log_container'] = log_container
    
    if not st.session_state['logged_in']:
        show_login()
    else:
        # المحتوى الرئيسي
        with st.sidebar:
            st.write(f"**{st.session_state.user['name']}** ({st.session_state.user['role']})")
            st.divider()
            if st.button("خروج"):
                st.session_state['logged_in'] = False
                if 'selected_lesson' in st.session_state: del st.session_state['selected_lesson']
                log_event("تسجيل خروج المستخدم", "WARNING")
                st.rerun()
        
        role = st.session_state.user['role']
        if role == 'مدير':
            st.header("لوحة المدير")
            st.dataframe(st.session_state.users)
        elif role == 'معلم':
            show_teacher_dashboard()
        elif role == 'طالب':
            show_student_dashboard()

    # 2. الشريط السفلي (Footer)
    st.markdown(f"""
    <div class="footer-bar">
        <p>
        🇩🇿 <strong>المنصة التعليمية الذكية</strong> - من إنجاز طلبة المدرسة العليا لأساتذة الصم البكم بني مسوس 
        <br>
        الماستر 01 الدفعة الرابعة السنة الدراسية 2025/2026 تحت إشراف الأستاذ د. بن عاشور رضا - مشروع أكاديمي تعلمي قابل للتطوير
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
