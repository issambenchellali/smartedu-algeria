"""
🇩🇿 SmartEdu Algeria V7.0 - Login & Dynamic Video System
المميزات الجديدة:
1. واجهة تسجيل دخول حقيقية (للمعلم والطالب).
2. المعلم يمكنه إضافة دروس برابط فيديو من يوتيوب أو رابط مباشر.
3. الطالب يشاهد الفيديو باستخدام الرابط الذي أدخله المعلم ديناميكياً.
4. واجهة واضحة وعالية التباين (كما طلبت سابقاً).
"""

import streamlit as st
import pandas as pd
import re
from datetime import datetime

# ==========================================
# 1. إعدادات التصميم (واضح وكبير)
# ==========================================

st.set_page_config(
    page_title="منصة التعلم الذكية",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="collapsed" # إخفاء الشريط الجانبي في صفحة الدخول
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');
    
    body {
        font-family: 'Tajawal', sans-serif;
        background-color: #ffffff;
        color: #1a202c;
    }
    
    .stApp {
        font-size: 18px;
        direction: rtl;
    }
    
    h1, h2, h3 {
        color: #006633;
        font-weight: 800;
    }
    
    /* تنسيق صفحة الدخول */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh;
        background: #f0fdf4;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    /* بطاقات الدروس */
    .lesson-card {
        border: 2px solid #e2e8f0;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        background: #fff;
        transition: all 0.3s;
        cursor: pointer;
    }
    .lesson-card:hover {
        border-color: #006633;
        background: #f7fafc;
    }

    .stButton>button {
        font-size: 18px;
        font-weight: bold;
        height: 50px;
        border-radius: 8px;
    }

    .stButton>button[kind="primary"] {
        background-color: #006633;
        color: white;
    }

    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. تهيئة البيانات والمستخدمين
# ==========================================

if 'users' not in st.session_state:
    st.session_state.users = [
        {"username": "teacher", "password": "123", "name": "الأستاذ محمد", "role": "معلم"},
        {"username": "student", "password": "123", "name": "التلميذ أحمد", "role": "طالب"}
    ]

if 'lessons' not in st.session_state:
    # دروس افتراضية، لكن يمكن للمعلم إضافة غيرها
    st.session_state.lessons = [
        {
            "id": 1,
            "title": "شرح قاعدة باسكال",
            "subject": "فيزياء",
            "video_url": "https://www.youtube.com/watch?v=ZcQnJ1vQ2lY", # رابط يوتيوب كمثال
            "instructor": "الأستاذ محمد",
            "description": "شرح مبسط لضغط السوائل."
        }
    ]

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'user' not in st.session_state:
    st.session_state['user'] = None

# ==========================================
# 3. دوال مساعدة (Helper Functions)
# ==========================================

def extract_youtube_id(url):
    """استخراج معرف الفيديو من رابط يوتيوب لعمل Embed"""
    pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# ==========================================
# 4. واجهات النظام (Pages)
# ==========================================

def show_login():
    """واجهة تسجيل الدخول"""
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #006633;'>تسجيل الدخول 🇩🇿</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>منصة التعليم الذكية</p>", unsafe_allow_html=True)
    st.write("---")
    
    with st.form("login_form"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("اسم المستخدم")
        with col2:
            password = st.text_input("كلمة المرور", type="password")
        
        submitted = st.form_submit_button("دخول", use_container_width=True, type="primary")
        
        if submitted:
            # التحقق من المستخدم
            user_found = None
            for u in st.session_state.users:
                if u['username'] == username and u['password'] == password:
                    user_found = u
                    break
            
            if user_found:
                st.session_state['user'] = user_found
                st.session_state['logged_in'] = True
                st.success(f"تم تسجيل الدخول بنجاح! مرحباً {user_found['name']}")
                time.sleep(1)
                st.rerun()
            else:
                st.error("خطأ: اسم المستخدم أو كلمة المرور غير صحيحة")
                st.info("جرب:\nالمعلم: teacher / 123\nالطالب: student / 123")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_teacher_dashboard():
    """لوحة تحكم المعلم: إضافة دروس برابط فيديو"""
    st.sidebar.title(f"👨‍🏫 {st.session_state.user['name']}")
    
    st.header("📂 إدارة الدروس")
    st.markdown("أضف درساً جديداً عبر لصق رابط الفيديو أدناه.")
    
    # نموذج إضافة درس
    with st.form("add_lesson_form"):
        st.subheader("➕ إضافة درس جديد")
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("عنوان الدرس", placeholder="مثال: شرح المعادلات")
            subject = st.selectbox("المادة", ["رياضيات", "فيزياء", "علوم", "لغة عربية", "تاريخ"])
        
        with col2:
            level = st.selectbox("المستوى", ["ابتدائي", "متوسط", "ثانوي"])
        
        description = st.text_area("وصف الدرس", placeholder="اكتب نبذة مختصرة...")
        
        # حقل رابط الفيديو (هنا الميزة المطلوبة)
        video_url = st.text_input("🔗 رابط الفيديو (YouTube or Direct)", placeholder="https://www.youtube.com/watch?v=...")
        
        if st.form_submit_button("نشر الدرس", use_container_width=True, type="primary"):
            if title and video_url:
                new_lesson = {
                    "id": len(st.session_state.lessons) + 1,
                    "title": title,
                    "subject": subject,
                    "level": level,
                    "video_url": video_url,
                    "instructor": st.session_state.user['name'],
                    "description": description
                }
                st.session_state.lessons.append(new_lesson)
                st.success("تمت إضافة الدرس بنجاح!")
                st.rerun()
            else:
                st.error("يرجى ملء العنوان ورابط الفيديو")
    
    st.divider()
    st.subheader("📜 الدروس التي قمت بإضافتها")
    for lesson in reversed(st.session_state.lessons): # عرض الأحدث أولاً
        if lesson['instructor'] == st.session_state.user['name']:
            st.markdown(f"""
            <div class="lesson-card">
                <h3>{lesson['title']}</h3>
                <p>{lesson['video_url']}</p>
            </div>
            """, unsafe_allow_html=True)

def show_student_dashboard():
    """لوحة تحكم الطالب: عرض الدروس ومشاهدة الفيديو"""
    st.sidebar.title(f"🎓 {st.session_state.user['name']}")
    
    # إذا تم اختيار درس، عرض المشغل
    if 'selected_lesson' in st.session_state:
        show_lesson_player(st.session_state['selected_lesson'])
    else:
        st.header("📚 قائمة الدروس المتاحة")
        
        # فلاتر
        subject_filter = st.selectbox("تصفية حسب المادة", ["الكل"] + ["رياضيات", "فيزياء", "علوم", "لغة عربية", "تاريخ"])
        
        filtered_lessons = st.session_state.lessons
        if subject_filter != "الكل":
            filtered_lessons = [l for l in st.session_state.lessons if l['subject'] == subject_filter]
        
        if not filtered_lessons:
            st.info("لا توجد دروس حالياً في هذه المادة.")
        
        # عرض البطاقات
        for lesson in filtered_lessons:
            with st.container():
                col_vid, col_info = st.columns([1, 2])
                with col_vid:
                    # عرض صورة مصغرة إذا كان يوتيوب
                    yt_id = extract_youtube_id(lesson['video_url'])
                    if yt_id:
                        st.image(f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg", use_column_width=True)
                    else:
                        st.image("https://via.placeholder.com/400x225?text=Video", use_column_width=True)
                
                with col_info:
                    st.markdown(f"<h3>{lesson['title']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>المدرس:</strong> {lesson['instructor']} | <strong>المادة:</strong> {lesson['subject']}</p>", unsafe_allow_html=True)
                    st.write(lesson['description'])
                    
                    # زر المشاهدة
                    if st.button(f"👀 مشاهدة: {lesson['title']}", key=f"watch_{lesson['id']}", use_container_width=True):
                        st.session_state['selected_lesson'] = lesson
                        st.rerun()
                
                st.markdown("---")

def show_lesson_player(lesson):
    """مشغل الفيديو الديناميكي"""
    st.title(f"🎬 {lesson['title']}")
    
    if st.button("⬅️ عودة للقائمة"):
        del st.session_state['selected_lesson']
        st.rerun()
    
    # تحويل الرابط للعرض
    yt_id = extract_youtube_id(lesson['video_url'])
    
    st.markdown(f"**المدرس:** {lesson['instructor']}")
    st.markdown(f"**الرابط المستخدم:** {lesson['video_url']}")
    st.divider()
    
    # منطق العرض
    if yt_id:
        # إذا كان الرابط يوتيوب، استخدم iframe مدمج
        embed_url = f"https://www.youtube.com/embed/{yt_id}"
        st.components.v1.iframe(embed_url, height=500, scrolling=False)
    else:
        # إذا كان رابط آخر (مثلاً mp4)، حاول تشغيله مباشرة
        if lesson['video_url'].endswith('.mp4'):
            st.video(lesson['video_url'])
        else:
            st.warning("هذا الرابط ليس من يوتيوب ولا يمكن مشاهدته داخلياً.")
            st.markdown(f"### [اضغط هنا لمشاهدة الفيديو في نافذة جديدة]({lesson['video_url']})")

# ==========================================
# 5. التوجيه الرئيسي (Routing)
# ==========================================

def main():
    if not st.session_state['logged_in']:
        show_login()
    else:
        # زر الخروج في الشريط الجانبي
        with st.sidebar:
            st.divider()
            if st.button("🚪 تسجيل الخروج"):
                st.session_state['logged_in'] = False
                st.session_state['user'] = None
                if 'selected_lesson' in st.session_state:
                    del st.session_state['selected_lesson']
                st.rerun()
        
        # توجيه حسب الدور
        if st.session_state.user['role'] == 'معلم':
            show_teacher_dashboard()
        else:
            show_student_dashboard()

if __name__ == "__main__":
    main()
