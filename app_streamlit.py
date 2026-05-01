"""
🇩🇿 SmartEdu Algeria V12.0 - Global LMS Standard
المميزات الجديدة:
1. اللوج في أسفل الشريط الجانبي (Sidebar Logs).
2. خطوط عريضة جداً (Bold) وكبيرة للوضوح القصوى.
3. اختيار الدور عند التسجيل (طالب/معلم).
4. حساب المدير (admin/123) مدمج ومحمي (Hardcoded).
5. تصميم بصري قوي (Icons, Diaporama, Global Style).
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
# 1. إعدادات CSS والتصميم (Global LMS Style)
# ==========================================

st.set_page_config(
    page_title="Global LMS - بني مسوس",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@800;900&display=swap');
    
    /* إعدادات أساسية */
    .stApp {
        background: #f8fafc;
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }

    /* إخفاء العناصر الافتراضية */
    #MainMenu, footer {visibility: hidden;}

    /* طباعة واضحة جداً (Bold & Large) */
    h1, h2, h3, h4 {
        color: #0f172a;
        font-weight: 900;
        line-height: 1.3;
    }
    
    h1 { font-size: 3rem; letter-spacing: -1px; }
    h2 { font-size: 2.2rem; }
    
    /* تسميات المدخلات */
    label { font-weight: 800; font-size: 1.1rem; color: #334155; }

    /* البطاقات العالمية (LMS Cards) */
    .lms-card {
        background: white;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 25px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .lms-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: #006633;
    }

    /* تأثير الديابو (Diaporama) للصور */
    .diaporama-img {
        width: 100%;
        height: 250px;
        object-fit: cover;
        border-radius: 12px;
        transition: transform 0.5s ease;
    }
    
    .lms-card:hover .diaporama-img {
        transform: scale(1.05);
    }

    /* الأزرار */
    .stButton>button {
        font-weight: 900;
        font-size: 1.2rem;
        border-radius: 12px;
        height: 60px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.2s;
    }
    
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #006633 0%, #004d26 100%);
        color: white;
        border: none;
    }

    /* الشريط الجانبي واللوج */
    [data-testid="stSidebar"] {
        background: white;
        border-left: 1px solid #e2e8f0;
        display: flex;
        flex-direction: column;
    }
    
    /* حاوية اللوج في أسفل الشريط الجانبي */
    .sidebar-logs-container {
        margin-top: auto; /* دفع الحاوية للأسفل */
        background: #1e293b;
        color: #94a3b8;
        border-top: 2px solid #006633;
        padding: 15px;
        border-radius: 12px 12px 0 0;
        font-family: 'Courier New', monospace;
        font-size: 0.75rem;
        height: 180px;
        overflow-y: auto;
        direction: ltr;
    }
    
    .log-entry { margin-bottom: 5px; border-bottom: 1px solid #334155; padding-bottom: 2px; }
    .log-time { color: #22d3ee; font-weight: bold; }

    /* الشريط السفلي */
    .footer-bar {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: #004d26;
        color: white;
        padding: 15px;
        text-align: center;
        font-weight: 800;
        font-size: 0.9rem;
        z-index: 1000;
        box-shadow: 0 -4px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. دوال النظام والتهيئة (Logic & Init)
# ==========================================

def log_event(message):
    """دالة تسجيل الأحداث"""
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] [INFO] {message}"
    st.session_state.logs.append(entry)

def initialize_session_state():
    """تهيئة كاملة للجلسة"""
    if 'users' not in st.session_state:
        st.session_state.users = [
            {"username": "teacher", "password": "123", "name": "أ. د. كمال", "role": "معلم"},
            {"username": "student", "password": "123", "name": "الطالب سعيد", "role": "طالب"}
        ]
        log_event("تم تحميل قاعدة المستخدمين")

    if 'lessons' not in st.session_state:
        st.session_state.lessons = [
            {
                "id": 1, 
                "title": "التفاضل والتكامل: فهم المشتقات", 
                "subject": "رياضيات", 
                "instructor": "أ. د. كمال", 
                "video_url": "https://www.youtube.com/watch?v=WUvTyaaNkzM",
                "description": "دورة شاملة في التفاضل تغطي المفاهيم الأساسية والتطبيقات المتقدمة.",
                "duration": "45 دقيقة"
            },
            {
                "id": 2, 
                "title": "تاريخ الجزائر الحديث: الثورة التحريرية", 
                "subject": "تاريخ", 
                "instructor": "أ. د. كمال", 
                "video_url": "https://www.youtube.com/watch?v=G8Gp9iG7S_A",
                "description": "سرد تاريخي مفصل لأحداث ثورة التحرير والنضال الوطني.",
                "duration": "60 دقيقة"
            },
            {
                "id": 3, 
                "title": "الذكاء الاصطناعي ومستقبل البشرية", 
                "subject": "علوم الحاسوب", 
                "instructor": "أ. د. كمال", 
                "video_url": "https://www.youtube.com/watch?v=aircAruvnKk",
                "description": "استكشاف كيف تتعلم الآلات وتأثير ذلك على مختلف المجالات.",
                "duration": "90 دقيقة"
            }
        ]
        log_event("تم تحميل المكتبة الرقمية")

    if 'logs' not in st.session_state:
        st.session_state.logs = []

    if 'progress' not in st.session_state:
        st.session_state.progress = []

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

announcements_data = [
    {
        "title": "المؤتمر الدولي للتعليم الذكي 2025",
        "desc": "ينظم المركز الجامعي مؤتمراً دولياً حول تكنولوجيا التعليم في عصر الذكاء الاصطناعي.",
        "img": "https://images.unsplash.com/photo-1544531586-fde5298cdd40?w=800&q=80"
    },
    {
        "title": "بدء التسجيل في الماستر 2",
        "desc": "يُعلن مدير المدرسة العليا عن فتح باب التسجيل لسنة الماستر الثانية لطلبة التخرج.",
        "img": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800&q=80"
    },
    {
        "title": "يوم التميز العلمي",
        "desc": "تكريم الطلاب المتفوقين والباحثين في حفل علمي كبير بحضور الأساتذة والكوادر.",
        "img": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800&q=80"
    }
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
    st.markdown("<div class='lms-card' style='max-width: 600px; margin: 100px auto; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #006633;'>مرحباً بعودتك 🇩🇿</h1>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 تسجيل الدخول", "📝 إنشاء حساب جديد"])
    
    with tab_login:
        with st.form("login_form"):
            st.markdown("<h3 style='margin-top: 30px;'>الدخول إلى النظام</h3>", unsafe_allow_html=True)
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")
            
            if st.form_submit_button("تسجيل الدخول", use_container_width=True, type="primary"):
                # 1. فحص المدير العام (Hardcoded Admin) أولاً
                if username == "admin" and password == "123":
                    st.session_state['user'] = {"username": "admin", "name": "المدير العام", "role": "مدير"}
                    st.session_state['logged_in'] = True
                    log_event("تسجيل دخول: المدير العام")
                    st.success("تم الدخول بنجاح بصلاحيات المدير العام")
                    time.sleep(1)
                    st.rerun()
                
                # 2. فحص المستخدمين العاديين
                else:
                    user = next((u for u in st.session_state.users if u['username'] == username and u['password'] == password), None)
                    if user:
                        st.session_state['user'] = user
                        st.session_state['logged_in'] = True
                        log_event(f"تسجيل دخول: {username}")
                        st.success(f"مرحباً {user['name']}")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("بيانات الدخول غير صحيحة")

    with tab_signup:
        with st.form("signup_form"):
            st.markdown("<h3 style='margin-top: 30px;'>حساب جديد</h3>", unsafe_allow_html=True)
            
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
                    log_event(f"تسجيل حساب جديد ({new_role}): {new_name}")
                    st.success("تم إنشاء الحساب بنجاح! يرجى تسجيل الدخول.")
                else:
                    st.error("اسم المستخدم موجود مسبقاً")

    st.markdown("</div>", unsafe_allow_html=True)

def show_admin_dashboard():
    st.header("📊 لوحة القيادة الإدارية")
    
    # إحصائيات (KPIs)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("إجمالي المستخدمين", len(st.session_state.users), "👥", delta_color="normal")
    c2.metric("الدروس النشطة", len(st.session_state.lessons), "📚", delta_color="normal")
    c3.metric("حالة النظام", "مستقر", "🟢", delta_color="normal")
    c4.metric("سعة التخزين", "85%", "💾", delta_color="normal")
    
    st.divider()
    
    # قسم الرسوم البيانية
    col_chart, col_info = st.columns([2, 1])
    with col_chart:
        st.subheader("📈 تحليل النشاط الشهري")
        chart_data = pd.DataFrame({
            'الشهر': ['يناير', 'فبراير', 'مارس', 'أبريل'],
            'الزوار': [120, 150, 180, 220]
        })
        st.line_chart(chart_data.set_index('الشهر'), use_container_width=True, color="#006633")
    
    with col_info:
        st.subheader("⚙️ إعدادات النظام")
        st.info("إعدادات الأمان:")
        st.write("- تفعيل المصادقة الثنائية")
        st.write("- نسخ احتياطي يومي")
        st.write("- تحديث النسخة V12.0")

def show_teacher_dashboard():
    st.header("👨‍🏫 منصة المعلم")
    
    with st.form("add_lesson"):
        st.markdown("### ➕ إضافة محتوى تعليمي جديد")
        col1, col2 = st.columns(2)
        title = col1.text_input("عنوان الدرس")
        subject = col2.selectbox("المادة", ["رياضيات", "علوم الحاسوب", "تاريخ", "فيزياء"])
        video_url = st.text_input("رابط الفيديو (YouTube)")
        desc = st.text_area("وصف مختصر")
        
        if st.form_submit_button("نشر الدرس", use_container_width=True, type="primary"):
            if title and video_url:
                st.session_state.lessons.append({
                    "id": len(st.session_state.lessons) + 1,
                    "title": title, "subject": subject,
                    "instructor": st.session_state.user['name'],
                    "video_url": video_url,
                    "description": desc,
                    "duration": "غير محدد"
                })
                log_event("نشر درس جديد")
                st.success("تم النشر بنجاح")
                st.rerun()

    st.divider()
    st.subheader("📂 الدروس الخاصة بك")
    for lesson in st.session_state.lessons:
        if lesson['instructor'] == st.session_state.user['name']:
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"**{lesson['title']}** - {lesson['subject']}")
            if col2.button("🗑️ حذف", key=f"del_{lesson['id']}", type="secondary"):
                st.session_state.lessons.remove(lesson)
                log_event("حذف درس")
                st.rerun()

def show_student_dashboard():
    st.header("🎓 المنطقة التعليمية للطالب")
    
    prog = len(st.session_state.progress) / len(st.session_state.lessons) * 100 if st.session_state.lessons else 0
    
    tab1, tab2, tab3, tab4 = st.tabs(["📢 الإعلانات", "📚 المكتبة الرقمية", "📈 مسار التفوق", "🤖 المساعد الذكي"])
    
    with tab1:
        for ann in announcements_data:
            st.markdown(f"""
            <div class='lms-card'>
                <img src="{ann['img']}" class="diaporama-img" style="height: 200px; margin-bottom: 20px;">
                <h2 style="color: #006633; font-size: 1.8rem;">{ann['title']}</h2>
                <p style="font-size: 1.1rem; color: #475569;">{ann['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    with tab2:
        if 'selected_lesson' in st.session_state:
            show_lesson_player(st.session_state['selected_lesson'])
        else:
            for lesson in st.session_state.lessons:
                yt_id = extract_youtube_id(lesson['video_url'])
                thumb = f"https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg" if yt_id else "https://placehold.co/800x450/006633/FFFFFF?text=Lesson+Preview"
                
                st.markdown(f"""
                <div class='lms-card'>
                    <img src="{thumb}" class="diaporama-img">
                    <h2 style="margin-top: 15px;">{lesson['title']}</h2>
                    <div style="display: flex; gap: 10px; margin: 10px 0;">
                        <span style="background: #e2e8f0; padding: 5px 10px; border-radius: 5px; font-weight: bold;">{lesson['subject']}</span>
                        <span style="background: #dcfce7; color: #166534; padding: 5px 10px; border-radius: 5px; font-weight: bold;">{lesson.get('duration', 'N/A')}</span>
                    </div>
                    <p>{lesson.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"▶️ بدء الدرس: {lesson['title']}", key=f"watch_{lesson['id']}", use_container_width=True, type="primary"):
                    st.session_state['selected_lesson'] = lesson
                    st.rerun()

    with tab3:
        st.markdown(f"<h1 style='text-align: center; color: #006633;'>{int(prog)}%</h1>", unsafe_allow_html=True)
        st.progress(prog / 100)
        
        col1, col2 = st.columns(2)
        col1.metric("الدروس المكتملة", len(st.session_state.progress), "✅")
        col2.metric("الدروس المتبقية", len(st.session_state.lessons) - len(st.session_state.progress), "⏳")

    with tab4:
        st.header("🤖 المساعد الأكاديمي الذكي")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(f"<div style='font-size: 1.1rem;'>{msg['content']}</div>", unsafe_allow_html=True)
        
        user_input = st.chat_input("اسألني عن دروسك...")
        
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            
            response = random.choice(["هذا سؤال ذكي جداً!", "للفهم الأفضل، راجع الفيديو مرة أخرى.", "أنا هنا لمساعدتك دائماً."])
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)
            st.rerun()

def show_lesson_player(lesson):
    st.title(lesson['title'])
    
    if st.button("⬅️ عودة للمكتبة"):
        del st.session_state['selected_lesson']
        if lesson['id'] not in st.session_state.progress:
            st.session_state.progress.append(lesson['id'])
            log_event(f"مشاهدة درس: {lesson['title']}")
        st.rerun()
        
    yt_id = extract_youtube_id(lesson['video_url'])
    if yt_id:
        components.iframe(f"https://www.youtube.com/embed/{yt_id}", height=500)
    else:
        st.warning("لا يمكن عرض الفيديو")

# ==========================================
# 5. التشغيل الرئيسي (Main Loop)
# ==========================================

def main():
    # تهيئة البيانات
    initialize_session_state()
    
    if not st.session_state['logged_in']:
        show_login()
    else:
        # تصميم الشريط الجانبي مع اللوج في الأسفل
        with st.sidebar:
            # قسم المستخدم
            st.markdown(f"<h2 style='color: #006633;'>{st.session_state.user['name']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 1.1rem; font-weight: bold;'>📌 {st.session_state.user['role']}</p>", unsafe_allow_html=True)
            st.divider()
            
            # التنقل
            st.write("**القائمة الرئيسية:**")
            menu = st.radio("", ["🏠 الرئيسية", "📂 المكتبة", "📈 التقدم", "🤖 المساعد"], label_visibility="collapsed")
            st.divider()
            
            # مساحة لتدفع اللوج للأسفل
            st.markdown("<div style='flex-grow: 1; min-height: 20px;'></div>", unsafe_allow_html=True)
            
            # اللوج (مثبت في الأسفل)
            with st.container():
                logs_html = "<div class='sidebar-logs-container'>"
                logs_html += "<div style='font-weight: bold; color: white; margin-bottom: 5px;'>📜 سجل النظام (Logs)</div>"
                for log in reversed(st.session_state.logs[-8:]):
                    logs_html += f"<div class='log-entry'>{log}</div>"
                logs_html += "</div>"
                st.markdown(logs_html, unsafe_allow_html=True)
            
            # زر الخروج
            if st.button("🚪 تسجيل الخروج", use_container_width=True):
                st.session_state['logged_in'] = False
                if 'selected_lesson' in st.session_state: del st.session_state['selected_lesson']
                log_event("تسجيل خروج")
                st.rerun()
        
        # منطق العرض الرئيسي
        role = st.session_state.user['role']
        if role == 'مدير':
            show_admin_dashboard()
        elif role == 'معلم':
            show_teacher_dashboard()
        elif role == 'طالب':
            # توجيه التبويبات (محاكاة بسيطة للتنقل داخل لوحة الطالب)
            if menu == "🏠 الرئيسية": # الإعلانات
                st.subheader("📢 آخر الأخبار والإعلانات")
                for ann in announcements_data:
                    st.markdown(f"""
                    <div class='lms-card'>
                        <img src="{ann['img']}" class="diaporama-img">
                        <h2>{ann['title']}</h2>
                        <p>{ann['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            elif menu == "📂 المكتبة":
                # عرض الدروس
                if 'selected_lesson' in st.session_state:
                    show_lesson_player(st.session_state['selected_lesson'])
                else:
                    for lesson in st.session_state.lessons:
                        st.markdown(f"<div class='lms-card'>", unsafe_allow_html=True)
                        yt_id = extract_youtube_id(lesson['video_url'])
                        thumb = f"https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg" if yt_id else "https://placehold.co/800x450/006633/FFFFFF?text=Lesson+Preview"
                        st.image(thumb, use_column_width=True)
                        st.markdown(f"<h2>{lesson['title']}</h2>", unsafe_allow_html=True)
                        if st.button(f"▶️ مشاهدة", key=f"watch_side_{lesson['id']}", use_container_width=True, type="primary"):
                            st.session_state['selected_lesson'] = lesson
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
            elif menu == "📈 التقدم":
                prog = len(st.session_state.progress) / len(st.session_state.lessons) * 100 if st.session_state.lessons else 0
                st.markdown(f"<h1 style='text-align: center;'>{int(prog)}%</h1>", unsafe_allow_html=True)
                st.progress(prog / 100)
            elif menu == "🤖 المساعد":
                st.header("مساعدك الذكي")
                st.chat_input("اكتب هنا...")

    # الفوتر
    st.markdown(f"""
    <div class="footer-bar">
        🇩🇿 <strong>Global LMS - منصة التعليم الذكية</strong> | من إنجاز طلبة المدرسة العليا لأساتذة الصم البكم بني مسوس | الماستر 01 الدفعة الرابعة 2025/2026 | إشراف: د. بن عاشور رضا
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
