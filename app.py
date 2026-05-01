"""
🇩🇿 SmartEdu Algeria V4.0 - Enterprise Connected Edition
المميزات:
- اتصال حقيقي بقاعدة بيانات Supabase
- إدارة ملفات PDF للدروس (رفع وتحميل)
- صلاحيات كاملة: المدير (إدارة المستخدمين)، المعلم (إدارة الدروس)
- تصميم UI/UX عصري (Modern Glassmorphism)
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import io
from supabase import create_client, Client
from typing import List, Dict, Optional

# ==========================================
# 1. CONFIG & SECRETS
# ==========================================

# إعدادات الصفحة
st.set_page_config(
    page_title="SmartEdu Algeria - Connected",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# الاتصال بـ Supabase
# في Streamlit Cloud، ضع هذه القيم في قسم Secrets
# في التطوير المحلي، يمكنك وضعها مباشرة للتجربة
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "YOUR_SUPABASE_URL_HERE")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "YOUR_SUPABASE_KEY_HERE")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    CONNECTION_STATUS = "🟢 متصل بقاعدة البيانات"
except:
    supabase = None
    CONNECTION_STATUS = "🔴 خطأ في الاتصال (تحقق من المفاتيح)"

# ==========================================
# 2. ADVANCED UI STYLING (Glassmorphism)
# ==========================================

st.markdown("""
<style>
    /* Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;500;700;900&display=swap');
    
    /* Global Styles */
    .stApp {
        background-color: #f0f4f8;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.15);
    }
    
    /* Sidebar Styling - Deep Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #0f172a 100%);
        color: white;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: rgba(255, 255, 255, 0.8);
    }

    /* Primary Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.2s;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
    
    /* Danger Buttons (Delete) */
    .stButton > button[kind="secondary"] {
        background: #ef4444;
        color: white;
        border-radius: 12px;
    }

    /* Metrics & KPIs */
    [data-testid="stMetricValue"] {
        font-family: 'Cairo', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
    }
    
    /* Image containers */
    .lesson-img-container {
        width: 100%;
        height: 200px;
        overflow: hidden;
        border-radius: 15px;
        margin-bottom: 15px;
        position: relative;
    }
    
    .lesson-img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s;
    }
    
    .lesson-img-container:hover img {
        transform: scale(1.1);
    }
    
    /* Badges */
    .badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        color: white;
        display: inline-block;
    }
    .badge-math { background: #3b82f6; }
    .badge-science { background: #10b981; }
    .badge-history { background: #f59e0b; }

    /* Hide Default Streamlit Footer */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BACKEND LOGIC (Supabase Integration)
# ==========================================

class DataManager:
    """مدير البيانات للتعامل مع Supabase"""
    
    def __init__(self, client: Client):
        self.client = client
    
    def login(self, username, password):
        """المصادقة البسيطة (للأغراض التجريبية)"""
        try:
            response = self.client.table('users').select("*").eq('username', username).eq('password', password).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            st.error(f"خطأ في قاعدة البيانات: {e}")
            return None

    def get_all_users(self):
        response = self.client.table('users').select("*").execute()
        return response.data if response.data else []

    def add_user(self, user_data):
        try:
            self.client.table('users').insert(user_data).execute()
            return True
        except Exception as e:
            st.error(f"فشل الإضافة: {e}")
            return False

    def delete_user(self, user_id):
        try:
            self.client.table('users').delete().eq('id', user_id).execute()
            return True
        except Exception as e:
            st.error(f"فشل الحذف: {e}")
            return False

    def get_lessons(self, subject_filter=None):
        query = self.client.table('lessons').select("*")
        if subject_filter:
            query = query.eq('subject', subject_filter)
        response = query.order('created_at', desc=True).execute()
        return response.data if response.data else []
    
    def add_lesson(self, lesson_data, pdf_file=None):
        try:
            # 1. رفع ملف PDF إلى Supabase Storage إذا وجد
            pdf_url = None
            if pdf_file:
                # ملاحظة: يجب إنشاء Bucket اسمه 'lessons' في Supabase يدوياً
                try:
                    file_name = f"{pdf_file.name}_{int(time.time())}"
                    self.client.storage.from_('lessons').upload(file_name, pdf_file.read())
                    # الحصول على رابط عام
                    pdf_url = self.client.storage.from_('lessons').get_public_url(file_name)
                except Exception as e:
                    st.warning(f"تعذر رفع الملف، سيتم حفظ الدرس بدون PDF: {e}")
            
            # 2. حفظ بيانات الدرس
            lesson_data['pdf_url'] = pdf_url
            self.client.table('lessons').insert(lesson_data).execute()
            return True
        except Exception as e:
            st.error(f"فشل إضافة الدرس: {e}")
            return False

    def delete_lesson(self, lesson_id):
        try:
            self.client.table('lessons').delete().eq('id', lesson_id).execute()
            return True
        except Exception as e:
            st.error(f"فشل الحذف: {e}")
            return False

# ==========================================
# 4. UI COMPONENTS & PAGES
# ==========================================

def show_login(db: DataManager):
    st.markdown("<h1 style='text-align: center; color: #1e3a8a; margin-bottom: 2rem;'>تسجيل الدخول 🇩🇿</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")
            st.markdown(f"<p style='text-align:center; color: #666;'>{CONNECTION_STATUS}</p>", unsafe_allow_html=True)
            submitted = st.form_submit_button("دخول للنظام", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if submitted:
                user = db.login(username, password)
                if user:
                    st.session_state['user'] = user
                    st.session_state['logged_in'] = True
                    st.success(f"أهلاً بك {user['full_name']}")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة")

def render_lesson_card(lesson, key):
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Image Section
        col1, col2 = st.columns([1, 2])
        with col1:
            img_url = lesson.get('image_url', 'https://via.placeholder.com/300')
            st.markdown(f'<div class="lesson-img-container"><img src="{img_url}"></div>', unsafe_allow_html=True)
        
        with col2:
            # Tags & Badges
            badge_color = "badge-math" if lesson['subject'] == "رياضيات" else "badge-science" if lesson['subject'] == "علوم" else "badge-history"
            st.markdown(f"<span class='badge {badge_color}'>{lesson['subject']}</span> <span class='badge' style='background:#64748b'>{lesson['level']}</span>", unsafe_allow_html=True)
            
            st.subheader(lesson['title'])
            st.caption(lesson.get('description', 'لا يوجد وصف'))
            
            # Action Buttons
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if lesson.get('pdf_url'):
                    # محاكاة تحميل الملف، في الواقع نستخدم الرابط
                    st.markdown(f"""
                    <a href="{lesson['pdf_url']}" target="_blank" style="
                        text-decoration: none; 
                        display: inline-block; 
                        background: #3b82f6; 
                        color: white; 
                        padding: 8px 15px; 
                        border-radius: 8px; 
                        font-size: 0.9rem; 
                        font-weight: bold;">
                        📄 تحميل PDF
                    </a>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("لا يوجد ملف PDF")
            
            with col_btn2:
                st.metric("المشاهدات", lesson['views'])
                
        st.markdown('</div>', unsafe_allow_html=True)

def admin_dashboard(db: DataManager, user):
    st.header("🛡️ لوحة تحكم المدير (Executive Admin)")
    
    # Admin: User Management
    st.subheader("👥 إدارة المستخدمين")
    users = db.get_all_users()
    
    with st.expander("إضافة مستخدم جديد"):
        with st.form("add_user_form"):
            c1, c2 = st.columns(2)
            new_user = {
                'username': c1.text_input("اسم المستخدم"),
                'password': c1.text_input("كلمة المرور", type="password"),
                'full_name': c2.text_input("الاسم الكامل"),
                'role': c2.selectbox("الدور", ["طالب", "معلم", "مدير"]),
                'disability_type': st.selectbox("نوع الإعاقة", DISABILITIES),
                'level': st.selectbox("المستوى", ["ابتدائي", "متوسط", "ثانوي"])
            }
            if st.form_submit_button("إضافة مستخدم"):
                if db.add_user(new_user):
                    st.success("تمت الإضافة بنجاح")
                    st.rerun()
    
    # User List with Delete Action
    if users:
        df = pd.DataFrame(users)
        st.dataframe(df, use_container_width=True)
        
        # Delete Section
        st.subheader("⚠️ حذف مستخدم")
        user_to_delete = st.selectbox("اختر المستخدم للحذف", options=[f"{u['id']} - {u['full_name']}" for u in users])
        if st.button("حذف نهائي", type="primary"):
            uid = int(user_to_delete.split(' - ')[0])
            if db.delete_user(uid):
                st.success("تم الحذف")
                st.rerun()

def teacher_dashboard(db: DataManager, user):
    st.header("👨‍🏫 بوابة المعلم")
    
    tab_manage, tab_view = st.tabs(["إدارة الدروس", "معاينة الطلاب"])
    
    with tab_manage:
        # Teacher: Add Lesson with PDF
        st.subheader("📂 رفع درس جديد")
        with st.form("upload_lesson"):
            title = st.text_input("عنوان الدرس")
            subject = st.selectbox("المادة", SUBJECTS)
            level = st.selectbox("المستوى", LEVELS)
            desc = st.text_area("وصف الدرس")
            uploaded_pdf = st.file_uploader("اختر ملف PDF للدرس", type=['pdf'])
            image_url = st.text_input("رابط الصورة الغلاف (اختياري)")
            
            if st.form_submit_button("نشر الدرس", type="primary"):
                lesson_data = {
                    'title': title, 'subject': subject, 'level': level,
                    'description': desc, 'image_url': image_url, 
                    'rating': 0, 'views': 0, 'created_by': user['id']
                }
                if db.add_lesson(lesson_data, uploaded_pdf):
                    st.success("تم رفع الدرس ونشره بنجاح!")
                    st.rerun()
        
        # Teacher: Delete Lessons
        st.divider()
        st.subheader("🗑️ حذف دروس")
        lessons = db.get_lessons()
        lesson_to_del = st.selectbox("اختر درس للحذف", [f"{l['id']} - {l['title']}" for l in lessons])
        if st.button("حذف الدرس المختار", type="primary"):
            lid = int(lesson_to_del.split(' - ')[0])
            if db.delete_lesson(lid):
                st.success("تم الحذف")
                st.rerun()

    with tab_view:
        st.write("إحصائيات الطلاب (قيد التطوير)...")

# Constants
LEVELS = ["ابتدائي", "متوسط", "ثانوي"]
SUBJECTS = ["رياضيات", "علوم", "فيزياء", "لغة عربية", "تاريخ"]
DISABILITIES = ["عادي", "صم", "ضعاف سمع"]

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if supabase:
        db = DataManager(supabase)
    else:
        st.error("لا يمكن الاتصال بقاعدة البيانات. يرجى التحقق من الإعدادات.")
        return

    # Sidebar Logic
    if st.session_state['logged_in']:
        with st.sidebar:
            user = st.session_state['user']
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100) # Generic logo
            st.markdown(f"### {user['full_name']}")
            st.markdown(f"**الدور:** {user['role']}")
            st.divider()
            
            if st.button("🏠 الرئيسية", use_container_width=True):
                st.rerun()
            
            if st.button("🚪 تسجيل الخروج", use_container_width=True):
                st.session_state.clear()
                st.rerun()

    # Routing
    if not st.session_state['logged_in']:
        show_login(db)
    
    else:
        user = st.session_state['user']
        if user['role'] == 'مدير':
            admin_dashboard(db, user)
        elif user['role'] == 'معلم':
            teacher_dashboard(db, user)
        elif user['role'] == 'طالب':
            st.header(f"مرحباً {user['full_name']} 🎓")
            
            # Student: View Lessons
            subject_filter = st.selectbox("تصفية حسب المادة", ["الكل"] + SUBJECTS)
            lessons = db.get_lessons(subject_filter if subject_filter != "الكل" else None)
            
            if not lessons:
                st.info("لا توجد دروس حالياً.")
            else:
                for lesson in lessons:
                    render_lesson_card(lesson, lesson['id'])

if __name__ == "__main__":
    main()
