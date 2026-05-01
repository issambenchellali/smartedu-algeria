"""
🇩🇿 SmartEdu Algeria V10.0 - Professional Academic Edition
المميزات الجديدة:
1. واجهة فاتحة واحترافية (Light Clean Theme).
2. خطوط عريضة (Bold) وواضحة جداً.
3. إصلاح عرض الفيديو (Thumbnails احترافية).
4. إعلانات أكاديمية وعالمية المستوى.
5. لوحة تحكم المدير المُحسنة برسوم بيانية.
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import re
import datetime

# ==========================================
# 1. إعدادات CSS والتصميم (Professional Light Theme)
# ==========================================

st.set_page_config(
    page_title="المنصة الأكاديمية - بني مسوس",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700;800;900&display=swap');
    
    /* الخلفية الفاتحة والنظيفة */
    .stApp {
        background: linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        color: #1a202c;
    }

    /* إخفاء العناصر الافتراضية */
    #MainMenu, footer {visibility: hidden;}

    /* البطاقات الاحترافية (Clean White Cards) */
    .pro-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
        color: #1f2937;
        transition: all 0.3s;
    }

    .pro-card:hover {
        box-shadow: 0 10px 30px rgba(0, 102, 51, 0.1);
        border-color: #006633;
    }

    /* العناوين العريضة جداً */
    h1, h2, h3 {
        color: #004d26;
        font-weight: 900;
    }

    /* واجهة الفيديو الاحترافية */
    .video-container {
        position: relative;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        border: 4px solid #ffffff;
    }
    
    .video-container img {
        width: 100%;
        height: auto;
        display: block;
        transition: transform 0.3s;
    }
    
    .video-container:hover img {
        transform: scale(1.02);
    }

    /* الأزرار */
    .stButton>button {
        font-weight: 800;
        font-size: 1.1rem;
        border-radius: 8px;
        height: 55px;
        border: none;
        text-transform: uppercase;
    }
    
    .stButton>button[kind="primary"] {
        background-color: #006633;
        color: white;
        box-shadow: 0 4px 15px rgba(0, 102, 51, 0.3);
    }

    /* مربع اللوج */
    .logs-panel {
        position: fixed;
        bottom: 90px;
        left: 20px;
        width: 320px;
        max-height: 150px;
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #e2e8f0;
        border-right: 4px solid #006633;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        overflow-y: auto;
        z-index: 999;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        direction: ltr;
    }

    /* الشريط السفلي */
    .footer-bar {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: #004d26;
        color: white;
        padding: 12px;
        text-align: center;
        font-weight: 700;
        z-index: 1000;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
    }

    /* تحسين التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        border-bottom: 2px solid #006633;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #666;
        font-weight: 700;
        padding: 10px 25px;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background: #006633;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. إدارة السجلات والبيانات
# ==========================================

def log_event(message, status="INFO"):
# التحقق من وجود المفتاح، وإذا لم يكن موجوداً، قم بتهيئته
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    
    # الآن يمكنك إضافة السجل بأمان
    st.session_state.logs.append(entry)
# تهيئة البيانات الاحترافية
if 'users' not in st.session_state:
    st.session_state.users = [
        {"username": "admin", "password": "123", "name": "مدير المنصة", "role": "مدير"},
        {"username": "teacher", "password": "123", "name": "أ. د. كمال", "role": "معلم"},
        {"username": "student", "password": "123", "name": "الطالب سعيد", "role": "طالب"}
    ]
    log_event("تم تهيئة النظام بنجاح")

if 'lessons' not in st.session_state:
    # عناوين احترافية
    st.session_state.lessons = [
        {
            "id": 1, 
            "title": "التفاضل والتكامل: الأساسيات المتقدمة", 
            "subject": "رياضيات", 
            "instructor": "أ. د. كمال", 
            "video_url": "https://www.youtube.com/watch?v=WUvTyaaNkzM",
            "description": "شرح مفصل لمفاهيم النهايات والمشتقات في التفاضل مع أمثلة تطبيقية على الحياة."
        },
        {
            "id": 2, 
            "title": "تاريخ الجزائر الحديث والمعاصر", 
            "subject": "تاريخ", 
            "instructor": "أ. د. كمال", 
            "video_url": "https://www.youtube.com/watch?v=G8Gp9iG7S_A",
            "description": "نظرة معمقة على الأحداث التاريخية لثورة التحرير والاستقلال."
        },
        {
            "id": 3, 
            "title": "مقدمة في الذكاء الاصطناعي", 
            "subject": "علوم الحاسوب", 
            "instructor": "أ. د. كمال", 
            "video_url": "https://www.youtube.com/watch?v=aircAruvnKk",
            "description": "تعلم كيف تعمل الخوارزميات الحديثة والشبكات العصبية بأسلوب مبسط."
        }
    ]

if 'logs' not in st.session_state:
    st.session_state.logs = []

if 'progress' not in st.session_state:
    st.session_state.progress = []

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# بيانات إعلانات احترافية (World Class)
announcements_data = [
    {
        "title": "المؤتمر الدولي للتعليم الرقمي 2024",
        "desc": "ندعوكم للمشاركة في المؤتمر الدولي الذي سيعقد في الجزائر العاصمة في شهر أكتوبر.",
        "img": "https://images.unsplash.com/photo-1544531586-fde5298cdd40?w=600&q=80"
    },
    {
        "title": "إعلان قائمة التفوق للفصل الدراسي",
        "desc": "تهنئ إدارة المدرسة الطلاب الحاصلين على مرتبة الشرف لهذا الفصل.",
        "img": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=600&q=80"
    },
    {
        "title": "فرص منح دراسية خارجية",
        "desc": "تتوفر منح دراسية كاملة للطلاب المتفوقين للدراسة في الجامعات الفرنسية والألمانية.",
        "img": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=600&q=80"
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
    tab_login, tab_signup = st.tabs(["🔐 تسجيل الدخول", "📝 إنشاء حساب جديد"])
    
    with tab_login:
        st.markdown("<div class='pro-card' style='max-width: 500px; margin: 80px auto; text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: #006633; font-size: 3rem;'>مرحباً بعودتك</h1>", unsafe_allow_html=True)
        st.write("<h3 style='color: #666;'>المنصة الأكاديمية المتكاملة</h3>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")
            
            if st.form_submit_button("دخول للنظام", use_container_width=True, type="primary"):
                user = next((u for u in st.session_state.users if u['username'] == username and u['password'] == password), None)
                if user:
                    st.session_state['user'] = user
                    st.session_state['logged_in'] = True
                    log_event(f"تم تسجيل الدخول: {username}")
                    st.success("تم الدخول بنجاح")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("بيانات خاطئة")
                    log_event("فشل تسجيل دخول", "ERROR")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_signup:
        st.markdown("<div class='pro-card' style='max-width: 500px; margin: 80px auto;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #006633;'>تسجيل طالب جديد</h2>", unsafe_allow_html=True)
        
        with st.form("signup_form"):
            new_name = st.text_input("الاسم الكامل")
            new_username = st.text_input("اسم المستخدم")
            new_password = st.text_input("كلمة المرور", type="password")
            
            if st.form_submit_button("تسجيل الحساب", use_container_width=True, type="primary"):
                if not any(u['username'] == new_username for u in st.session_state.users):
                    st.session_state.users.append({
                        "username": new_username, "password": new_password,
                        "name": new_name, "role": "طالب"
                    })
                    log_event(f"تسجيل طالب جديد: {new_name}")
                    st.success("تم إنشاء الحساب")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("اسم المستخدم موجود")
        st.markdown("</div>", unsafe_allow_html=True)

def show_admin_dashboard():
    st.sidebar.title(f"👮 {st.session_state.user['name']}")
    st.header("📊 لوحة القيادة التحليلية")
    
    # إحصائيات رئيسية
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("إجمالي المستخدمين", len(st.session_state.users), "+5%", delta_color="normal")
    c2.metric("المحتوى التعليمي", len(st.session_state.lessons), "+2", delta_color="normal")
    c3.metric("نسبة النشاط", "87%", "+12%", delta_color="normal")
    c4.metric("حالة النظام", "مستقر", "🟢")
    
    st.divider()
    
    # رسم بياني (Dummy Data for Professional Look)
    col_chart, col_data = st.columns([2, 1])
    
    with col_chart:
        st.subheader("📈 نمو التسجيلات الأسبوعي")
        dates = pd.date_range(end=datetime.date.today(), periods=7)
        growth_data = np.random.randint(5, 20, size=7)
        chart_df = pd.DataFrame({'التاريخ': dates.strftime('%d-%m'), 'التسجيلات': growth_data})
        st.line_chart(chart_df.set_index('التاريخ'), use_container_width=True, color="#006633")
    
    with col_data:
        st.subheader("أحدث النشاطات")
        activities = [
            "تسجيل طالب جديد: سعيد",
            "إضافة درس: الذكاء الاصطناعي",
            "تحديث النظام",
            "أرشيف ملفات PDF"
        ]
        for act in activities:
            st.markdown(f"""
            <div style='background: #f9fafb; padding: 10px; border-radius: 8px; margin-bottom: 8px; font-size: 0.9rem;'>
                🟢 {act}
            </div>
            """, unsafe_allow_html=True)

def show_teacher_dashboard():
    st.sidebar.title(f"👨‍🏫 {st.session_state.user['name']}")
    
    with st.form("add_lesson"):
        st.markdown("### ➕ إضافة درس جديد")
        col1, col2 = st.columns(2)
        title = col1.text_input("عنوان الدرس الاحترافي")
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
                log_event("تم إضافة درس جديد")
                st.success("تم النشر")
                st.rerun()
    
    # قائمة الدروس مع زر الحذف
    for lesson in st.session_state.lessons:
        if lesson['instructor'] == st.session_state.user['name']:
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"**{lesson['title']}**")
            if col2.button("🗑️ حذف", key=f"del_{lesson['id']}"):
                st.session_state.lessons.remove(lesson)
                log_event("حذف درس", "WARNING")
                st.rerun()

def show_student_dashboard():
    st.sidebar.title(f"🎓 {st.session_state.user['name']}")
    
    # حساب التقدم
    prog = len(st.session_state.progress) / len(st.session_state.lessons) * 100 if st.session_state.lessons else 0
    
    # التبويبات
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📢 الإعلانات الأكاديمية", "📚 المكتبة الرقمية", "📈 تقدمك", "🤖 المساعد الذكي", "💡 نصائح التفوق"])
    
    # 1. الإعلانات الاحترافية
    with tab1:
        for ann in announcements_data:
            st.markdown(f"""
            <div class='pro-card' style='padding: 0; overflow: hidden;'>
                <img src="{ann['img']}" style="width:100%; height: 200px; object-fit: cover;">
                <div style="padding: 20px;">
                    <h3 style="color: #006633;">{ann['title']}</h3>
                    <p style="color: #4b5563;">{ann['desc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    # 2. المكتبة الرقمية
    with tab2:
        if 'selected_lesson' in st.session_state:
            show_lesson_player(st.session_state['selected_lesson'])
        else:
            for lesson in st.session_state.lessons:
                yt_id = extract_youtube_id(lesson['video_url'])
                thumb = f"https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg" if yt_id else "https://placehold.co/800x450/006633/FFFFFF?text=Video+No+Preview"
                
                # تصميم البطاقة الاحترافي للدرس
                st.markdown(f"""
                <div class='pro-card'>
                    <div class="video-container">
                        <img src="{thumb}">
                    </div>
                    <h2 style="margin-top: 15px;">{lesson['title']}</h2>
                    <p style="color: #666; font-size: 1.1rem; margin-bottom: 20px;">{lesson.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"👀 مشاهدة الدرس الآن", key=f"watch_{lesson['id']}", use_container_width=True, type="primary"):
                    st.session_state['selected_lesson'] = lesson
                    st.rerun()
                
                st.markdown("---")

    # 3. التقدم
    with tab3:
        st.markdown(f"<h1 style='text-align: center; font-size: 4rem; color: #006633;'>{int(prog)}%</h1>", unsafe_allow_html=True)
        st.progress(prog / 100)
        
        col1, col2 = st.columns(2)
        col1.metric("الدروس المكتملة", len(st.session_state.progress))
        col2.metric("الدروس المتبقية", len(st.session_state.lessons) - len(st.session_state.progress))

    # 4. المساعد
    with tab4:
        st.header("🤖 المساعد الذكي الأكاديمي")
        st.info("أنا هنا للمساعدة في دراستك")
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(f"<div style='font-size: 1.1rem;'>{msg['content']}</div>", unsafe_allow_html=True)
        
        user_input = st.chat_input("اكتب سؤالك...")
        
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            
            response = random.choice([
                "هذا موضوع مهم للغاية، يرجى مراجعة الفيديو مرة أخرى.",
                "سؤال ممتاز! يرتبط هذا المفهوم بقوانين الفيزياء الأساسية.",
                "الاستمرارية هي مفتاح التعلم."
            ])
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)
            st.rerun()
            
    # 5. نصائح
    with tab5:
        tips = ["المراجعة بعد 24 ساعة تثبت المعلومة.", "ابدأ اليوم بدروس الأصعب.", "استخدم الملاحظات البصرية."]
        for t in tips:
            st.markdown(f"<h2 style='color: #006633; font-size: 1.5rem;'>📌 {t}</h2>", unsafe_allow_html=True)

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
        st.components.v1.iframe(f"https://www.youtube.com/embed/{yt_id}", height=500)
    else:
        st.warning("لا يمكن عرض الفيديو داخلياً")

# ==========================================
# 5. التشغيل الرئيسي
# ==========================================

def main():
    # تهيئة مربع اللوج
    log_container = st.empty()
    st.session_state['log_container'] = log_container

    if not st.session_state['logged_in']:
        show_login()
    else:
        with st.sidebar:
            st.write(f"**{st.session_state.user['name']}**")
            st.write(f"الدور: {st.session_state.user['role']}")
            st.divider()
            if st.button("🚪 تسجيل الخروج"):
                st.session_state['logged_in'] = False
                if 'selected_lesson' in st.session_state: del st.session_state['selected_lesson']
                log_event("تسجيل خروج", "WARNING")
                st.rerun()
        
        role = st.session_state.user['role']
        if role == 'مدير':
            show_admin_dashboard()
        elif role == 'معلم':
            show_teacher_dashboard()
        elif role == 'طالب':
            show_student_dashboard()

    # الشريط السفلي
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
