"""
🇩🇿 SmartEdu Algeria V8.0 - Ultimate Edition
المميزات:
1. نظام صلاحيات ثلاثي: (مدير - معلم - طالب).
2. المدير: يرى إحصائيات المنصة الكاملة.
3. المعلم: يضيف ويحذف الدروس.
4. الطالب: 5 تبويبات متكاملة (إعلانات، دروس، تقدم، شات، نصائح).
5. تصميم عصري بألوان العلم الجزائري (خلفيات زجاجية).
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import re

# ==========================================
# 1. إعدادات الصفحة والتصميم (Modern UI)
# ==========================================

st.set_page_config(
    page_title="منصة التعليم الجزائرية",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS متقدم يدعم ألوان العلم الجزائري والزجاجية
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');
    
    /* الخلفية المتدرجة الخفيفة (أبيض وأخضر فاتح) */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        color: #1f2937;
    }
    
    /* الخطوط والعناوين */
    h1, h2, h3 {
        color: #004d26; /* أخضر داكن */
        font-weight: 800;
    }
    
    /* البطاقات الزجاجية الحديثة */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(0, 102, 51, 0.1);
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border-color: #006633;
    }

    /* البطاقات في تبويب الإعلانات */
    .announcement-card {
        border-left: 5px solid #D52B1E; /* أحمر العلم */
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    /* الأزرار العصرية */
    .stButton>button {
        font-weight: bold;
        border-radius: 50px; /* أزرار مستديرة */
        padding: 12px 30px;
        transition: all 0.3s;
    }
    
    .stButton>button[kind="primary"] {
        background: linear-gradient(90deg, #006633 0%, #009944 100%);
        color: white;
        border: none;
    }
    
    .stButton>button[kind="secondary"] {
        background: #D52B1E; /* أحمر للحذف */
        color: white;
        border: none;
    }
    
    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: transparent;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px 10px 0 0;
        padding: 15px 25px;
        font-weight: bold;
        color: #6b7280;
        font-size: 1.1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: #006633;
        color: white;
        box-shadow: 0 4px 10px rgba(0, 102, 51, 0.2);
    }

    /* إخفاء الفوتر */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. تهيئة البيانات (Data & State)
# ==========================================

if 'users' not in st.session_state:
    st.session_state.users = [
        {"username": "admin", "password": "123", "name": "مدير المنصة", "role": "مدير"},
        {"username": "teacher", "password": "123", "name": "أ. محمد", "role": "معلم"},
        {"username": "student", "password": "123", "name": "الطالب أحمد", "role": "طالب"}
    ]

if 'lessons' not in st.session_state:
    st.session_state.lessons = [
        {"id": 1, "title": "أساسيات التفاضل", "subject": "رياضيات", "instructor": "أ. محمد", "video_url": "https://www.youtube.com/watch?v=ZcQnJ1vQ2lY"},
        {"id": 2, "title": "تاريخ التحرير", "subject": "تاريخ", "instructor": "أ. محمد", "video_url": "https://www.youtube.com/watch?v=2nSspGq1ZlY"}
    ]

if 'progress' not in st.session_state:
    st.session_state.progress = [] # لتخزين الـ IDs التي شاهدها الطالب

if 'announcements' not in st.session_state:
    # بيانات إعلانات وهمية بروابط صور حقيقية
    st.session_state.announcements = [
        {"title": "بدء مسابقة الروبوت", "desc": "شارك في مسابقة الابتكار العلمي الوطنية.", "img": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600"},
        {"title": "تذكير بالامتحانات", "desc": "اختبارات نهاية الفصل تبدأ الشهر القادم.", "img": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600"},
        {"title": "يوم العلم", "desc": "احتفل معنا بالفعاليات الترفيهية.", "img": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600"}
    ]

if 'tips' not in st.session_state:
    st.session_state.tips = [
        "المراجعة بعد 24 ساعة تحفظ المعلومة بنسبة 70%.",
        "شرب الماء بانتظام يحسن التركيز.",
        "قسّم وقت الدراسة إلى فترات (25 دقيقة عمل - 5 دقائق راحة).",
        "النوم الجيد ليلاً أهم من السهر."
    ]

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ==========================================
# 3. دوال مساعدة (Helpers)
# ==========================================

def extract_youtube_id(url):
    pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# ==========================================
# 4. الصفحات والأدوار (Pages)
# ==========================================

def show_login():
    st.markdown("<div class='glass-card' style='text-align: center; max-width: 500px; margin: 100px auto;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #006633;'>تسجيل الدخول 🇩🇿</h1>", unsafe_allow_html=True)
    st.markdown("<p>منصة التعليم المتطورة</p>", unsafe_allow_html=True)
    st.write("---")
    
    with st.form("login_form"):
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        
        submitted = st.form_submit_button("دخول", use_container_width=True, type="primary")
        
        if submitted:
            user = next((u for u in st.session_state.users if u['username'] == username and u['password'] == password), None)
            if user:
                st.session_state['user'] = user
                st.session_state['logged_in'] = True
                st.success(f"مرحباً {user['name']}")
                time.sleep(1)
                st.rerun()
            else:
                st.error("بيانات خاطئة، جرب:\n- admin / 123\n- teacher / 123\n- student / 123")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_admin_dashboard():
    """لوحة تحكم المدير: إحصائيات شاملة"""
    st.sidebar.title(f"👮 {st.session_state.user['name']}")
    
    st.header("📊 لوحة القيادة التنفيذية")
    
    # الإحصائيات
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("المستخدمين", len(st.session_state.users))
    c2.metric("الدروس", len(st.session_state.lessons))
    c3.metric("الطلاب النشطين", len([u for u in st.session_state.users if u['role'] == 'طالب']))
    c4.metric("المشاهدات", np.random.randint(100, 500)) # رقم وهمي
    
    st.divider()
    
    # جدول المستخدمين
    st.subheader("👥 قاعدة بيانات المستخدمين")
    df_users = pd.DataFrame(st.session_state.users)
    st.dataframe(df_users, use_container_width=True)
    
    st.subheader("📂 جميع الدروس")
    df_lessons = pd.DataFrame(st.session_state.lessons)
    st.dataframe(df_lessons, use_container_width=True)

def show_teacher_dashboard():
    """لوحة المعلم: إضافة وحذف الدروس"""
    st.sidebar.title(f"👨‍🏫 {st.session_state.user['name']}")
    
    # نموذج الإضافة
    with st.form("add_lesson"):
        st.markdown("### ➕ إضافة درس جديد")
        col1, col2 = st.columns(2)
        title = col1.text_input("عنوان الدرس")
        subject = col2.selectbox("المادة", ["رياضيات", "علوم", "تاريخ", "عربي"])
        video_url = st.text_input("رابط الفيديو (YouTube)")
        
        if st.form_submit_button("نشر", use_container_width=True, type="primary"):
            if title and video_url:
                new_lesson = {
                    "id": len(st.session_state.lessons) + 1,
                    "title": title, "subject": subject,
                    "instructor": st.session_state.user['name'],
                    "video_url": video_url
                }
                st.session_state.lessons.append(new_lesson)
                st.success("تمت الإضافة بنجاح")
                st.rerun()
    
    st.divider()
    st.subheader("📜 الدروس التي قمت بإضافتها")
    
    # عرض الدروس مع زر الحذف
    for lesson in st.session_state.lessons:
        if lesson['instructor'] == st.session_state.user['name']:
            with st.container():
                col1, col2 = st.columns([4, 1])
                col1.markdown(f"**{lesson['title']}** ({lesson['subject']})")
                if col2.button("🗑️ حذف", key=f"del_{lesson['id']}", type="secondary"):
                    st.session_state.lessons.remove(lesson)
                    st.rerun()
                st.divider()

def show_student_dashboard():
    """لوحة الطالب: 5 تبويبات متكاملة"""
    st.sidebar.title(f"🎓 {st.session_state.user['name']}")
    
    # حساب التقدم
    total_lessons = len(st.session_state.lessons)
    watched_lessons = len([l for l in st.session_state.lessons if l['id'] in st.session_state.progress])
    progress_percent = int((watched_lessons / total_lessons * 100)) if total_lessons > 0 else 0
    
    # إنشاء التبويبات
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📢 الإعلانات", "📚 دروسي", "📈 تقدمي", "🤖 الذكاء الاصطناعي", "💡 نصائح يومية"])
    
    # 1. تبويب الإعلانات
    with tab1:
        st.header("الأخبار والإعلانات المدرسية")
        for ann in st.session_state.announcements:
            st.markdown(f"""
            <div class="announcement-card">
                <img src="{ann['img']}" style="width:100%; height:200px; object-fit:cover; border-radius:8px; margin-bottom:10px;">
                <h3 style="margin:0;">{ann['title']}</h3>
                <p>{ann['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 2. تبويب دروسي
    with tab2:
        st.header("قائمة الدروس المتاحة")
        
        # عند اختيار درس
        if 'selected_lesson' in st.session_state:
            show_lesson_player(st.session_state['selected_lesson'])
        else:
            for lesson in st.session_state.lessons:
                is_watched = lesson['id'] in st.session_state.progress
                status_icon = "✅" if is_watched else "⬜"
                
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    yt_id = extract_youtube_id(lesson['video_url'])
                    with col1:
                        if yt_id:
                            st.image(f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg", use_column_width=True)
                    
                    with col2:
                        st.markdown(f"### {status_icon} {lesson['title']}")
                        st.caption(f"{lesson['subject']} | {lesson['instructor']}")
                        
                        if not is_watched:
                            if st.button(f"👀 مشاهدة الدرس", key=f"watch_{lesson['id']}", use_container_width=True):
                                st.session_state['selected_lesson'] = lesson
                                st.rerun()
                        else:
                            st.success("تمت المشاهدة مسبقاً")
                    
                    st.markdown("---")
    
    # 3. تبويب تقدمي
    with tab3:
        st.header("نسبة التقدم في المنصة")
        st.markdown(f"<h1 style='text-align: center; color: #006633;'>{progress_percent}%</h1>", unsafe_allow_html=True)
        st.progress(progress_percent / 100)
        
        col1, col2 = st.columns(2)
        col1.metric("الدروس المكتملة", watched_lessons)
        col2.metric("الدروس المتبقية", total_lessons - watched_lessons)
        
        if progress_percent == 100:
            st.balloons()
            st.success("أنت بطل! أتممت جميع الدروس.")

    # 4. تبويب الذكاء الاصطناعي
    with tab4:
        st.header("🤖 المعلم الذكي")
        st.info("اسألني عن أي شيء دراسي!")
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        user_input = st.chat_input("اكتب سؤالك...")
        
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # ردود بسيطة
            response = random.choice(st.session_state.tips)
            if "صعب" in user_input:
                response = "لا تيأس، كرر المشاهدة وستفهم. الصبر مفتاح الفهم."
            elif "شكرا" in user_input:
                response = "عفواً! أنا هنا دائماً."
                
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
            
            st.rerun()
            
    # 5. تبويب النصائح اليومية
    with tab5:
        st.header("💡 نصائح يومية للتفوق")
        today_tip = random.choice(st.session_state.tips)
        
        st.markdown(f"""
        <div class="glass-card" style='text-align: center; border: 2px dashed #006633;'>
            <h2>نصيحة اليوم</h2>
            <h1 style='color: #D52B1E; font-size: 2.5rem;'>"{today_tip}"</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("مزيد من النصائح:")
        for t in st.session_state.tips:
            if t != today_tip:
                st.success(f"• {t}")

def show_lesson_player(lesson):
    """مشغل الفيديو"""
    st.title(f"🎬 {lesson['title']}")
    
    if st.button("⬅️ عودة للقائمة"):
        del st.session_state['selected_lesson']
        # تسجيل الدرس كمشاهد
        if lesson['id'] not in st.session_state.progress:
            st.session_state.progress.append(lesson['id'])
        st.rerun()
    
    yt_id = extract_youtube_id(lesson['video_url'])
    if yt_id:
        st.components.v1.iframe(f"https://www.youtube.com/embed/{yt_id}", height=500)
    else:
        st.warning("تعذر تشغيل الفيديو داخلياً")

# ==========================================
# 5. التشغيل الرئيسي (Main Loop)
# ==========================================

def main():
    if not st.session_state['logged_in']:
        show_login()
    else:
        with st.sidebar:
            st.write(f"**الدور:** {st.session_state.user['role']}")
            st.divider()
            if st.button("🚪 تسجيل الخروج"):
                st.session_state['logged_in'] = False
                if 'selected_lesson' in st.session_state: del st.session_state['selected_lesson']
                st.rerun()
        
        # التوجيه حسب الدور
        role = st.session_state.user['role']
        if role == 'مدير':
            show_admin_dashboard()
        elif role == 'معلم':
            show_teacher_dashboard()
        elif role == 'طالب':
            show_student_dashboard()

if __name__ == "__main__":
    main()
