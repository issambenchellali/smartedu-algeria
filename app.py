"""
🇩🇿 SmartEdu Algeria V6.0 - Clean & Functional
مميزات الإصلاح:
1. واجهة فاتحة عالية الوضوح (High Contrast / Large Fonts).
2. مشغل دروس متكامل (فيديو يوتيوب مدمج + PDF + واجبات).
3. مساعد ذكي محسن بقاعدة بيانات أوسع للاجابات.
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from typing import List, Dict
import streamlit.components.v1 as components

# ==========================================
# 1. إعدادات التصميم (UI/UX) - التركيز على الوضوح
# ==========================================

st.set_page_config(
    page_title="المنصة التعليمية",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS لتكبير الخطوط وتحسين التباين
st.markdown("""
<style>
    /* إعدادات الخطوط والألوان الأساسية */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');
    
    body {
        font-family: 'Tajawal', sans-serif;
        background-color: #ffffff; /* خلفية بيضاء نقية */
        color: #1a202c; /* نص أسود داكن للقراءة السهلة */
    }
    
    /* تكبير النصوص في Streamlit */
    .stApp {
        font-size: 18px; /* حجم خط أساسي كبير */
        direction: rtl;
    }
    
    h1, h2, h3, h4 {
        color: #006633; /* أخضر جزائري واضح للعناوين */
        font-weight: 800;
    }
    
    /* تصميم البطاقات */
    .clean-card {
        background: #f7fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    
    .clean-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-color: #006633;
    }
    
    /* الأزرار */
    .stButton>button {
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        height: 50px;
    }
    
    .stButton>button[kind="primary"] {
        background-color: #006633;
        color: white;
    }

    /* الروابط */
    a {
        color: #006633;
        font-weight: bold;
        text-decoration: none;
    }
    
    /* إخفاء الفوتر */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. البيانات والروابط (Data & Media)
# ==========================================

# بيانات دروس غنية مع روابط يوتيوب حقيقية
LESSONS_DATA = [
    {
        "id": 1,
        "title": "شرح المعادلات الخطية للمبتدئين",
        "subject": "رياضيات",
        "level": "متوسط",
        "instructor": "أ. محمد",
        "youtube_id": "LwCRTTm8x4k", # فيديو حقيقي
        "pdf_link": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        "description": "شرح مبسط للمعادلات من الدرجة الأولى مع أمثلة محلولة.",
        "tags": ["جبر", "معادلات", "سهل"]
    },
    {
        "id": 2,
        "title": "كيف تعمل الطاقة الشمسية؟",
        "subject": "علوم",
        "level": "ثانوي",
        "instructor": "د. سارة",
        "youtube_id": "xKxrkax7-5M",
        "pdf_link": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        "description": "شرح فيزيائي لعملية تحويل الطاقة الشمسية إلى كهرباء.",
        "tags": ["طاقة", "بيئة", "فيزياء"]
    },
    {
        "id": 3,
        "title": "قواعد النحو: الفاعل والمفعول به",
        "subject": "لغة عربية",
        "level": "ابتدائي",
        "instructor": "أ. أحمد",
        "youtube_id": "p6b2Zx9q5YQ", # مثال
        "pdf_link": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        "description": "تعلم الفرق بين الفاعل والمفعول به بأسلوب ممتع.",
        "tags": ["نحو", "قواعد", "عربي"]
    }
]

# قاعدة بيانات محسنة للمساعد الذكي لمنع تكرار نفس الجملة
AI_KNOWLEDGE_BASE = {
    "رياضيات": [
        "الرياضيات هي لغة الكون، المفتاح هو فهم المنطق وليس الحفظ.",
        "لحل المعادلات، حاول دائماً عزل المجهول في طرف واحد.",
        "في الهندسة، الرسم هو أفضل طريقة للفهم."
    ],
    "فيزياء": [
        "الطاقة لا تفنى ولا تستحدث من العدم، تذكر هذا القانون دائماً.",
        "الجاذبية هي قوة تجذبنا نحو الأرض، وهي سبب سقوط الأجسام.",
        "السرعة هي المسافة مقسومة على الزمن."
    ],
    "عام": [
        "التعلم المستمر هو مفتاح النجاح، لا تستسلم أبداً.",
        "حاول تقسيم دراستك إلى فترات قصيرة حتى لا تشعر بالإرهاق.",
        "النوم الجيد يزيد من قدرة الدماغ على التركيز بنسبة 50%.",
        "هل جربت استخدام الخرائط الذهنية لتنظيم أفكارك؟",
        "المراجعة بعد 24 ساعة من الدرس تحفظ المعلومة لفترة أطول."
    ]
}

# ==========================================
# 3. المنطق البرمجي المحسن (Smart Logic)
# ==========================================

class SmartTutor:
    """مساعد ذكي محسن لا يتكرر في كلامه"""
    
    def get_response(self, user_input: str) -> str:
        text = user_input.lower()
        
        # منطق البحث عن كلمات مفتاحية
        if "رياض" in text or "معادلة" in text or "جبر" in text:
            return random.choice(AI_KNOWLEDGE_BASE["رياضيات"])
        elif "فيزي" in text or "طاقة" in text or "جاذبية" in text:
            return random.choice(AI_KNOWLEDGE_BASE["فيزياء"])
        elif "صعب" in text or "لم افهم" in text:
            return "لا بأس، هذا طبيعي. حاول مشاهدة الفيديو مرة أخرى وتوقف عند كل نقطة غير واضحة، أو اسألني عن جزء محدد."
        elif "شكرا" in text:
            return "عفواً! أنا هنا دائماً لمساعدتك. هل لديك سؤال آخر؟"
        else:
            # رد عام مفيد بدلاً من سؤال التوضيح الممل
            return random.choice(AI_KNOWLEDGE_BASE["عام"])

# ==========================================
# 4. دوال العرض (UI Functions)
# ==========================================

def show_lesson_card(lesson):
    """عرض بطاقة درس كبيرة وواضحة"""
    with st.container():
        col_img, col_info = st.columns([1, 2])
        
        with col_img:
            # استخدام صورة مصغرة للفيديو
            thumbnail_url = f"https://img.youtube.com/vi/{lesson['youtube_id']}/mqdefault.jpg"
            st.image(thumbnail_url, use_column_width=True)
        
        with col_info:
            st.markdown(f"<h2 style='margin:0;'>{lesson['title']}</h2>", unsafe_allow_html=True)
            
            # معلومات الدرس بوضوح
            st.markdown(f"""
            <div style='background: #e6fffa; padding: 10px; border-radius: 5px; border-right: 4px solid #006633; margin: 10px 0;'>
                <strong>المادة:</strong> {lesson['subject']} | 
                <strong>الصف:</strong> {lesson['level']} | 
                <strong>المدرس:</strong> {lesson['instructor']}
            </div>
            """, unsafe_allow_html=True)
            
            st.write(lesson['description'])
            
            # زر كبير وواضح للدخول
            if st.button(f"▶️ مشاهدة الدرس: {lesson['title']}", key=f"btn_{lesson['id']}", use_container_width=True):
                st.session_state['current_lesson'] = lesson
                st.session_state['page'] = 'player'
                st.rerun()

def show_lesson_player(lesson):
    """مشغل الدرس المتكامل (فيديو + ملفات)"""
    st.markdown(f"<h1>{lesson['title']}</h1>", unsafe_allow_html=True)
    
    # أزرار التحكم العلوية
    if st.button("⬅️ عودة للدروس"):
        st.session_state['page'] = 'home'
        st.rerun()
    
    # نظام التبويبات
    tab1, tab2, tab3 = st.tabs(["📺 الفيديو التعليمي", "📄 ملاحظات وملفات", "✏️ الواجبات"])
    
    with tab1:
        st.subheader("فيديو الشرح")
        # تضمين فيديو يوتيوب
        video_url = f"https://www.youtube.com/embed/{lesson['youtube_id']}?rel=0"
        components.iframe(video_url, height=500, scrolling=False)
        st.caption("إذا لم يظهر الفيديو، تأكد من اتصالك بالإنترنت.")
    
    with tab2:
        st.subheader("ملفات الدرس والملاحظات")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"#### ملخص الدرس")
            st.write("هنا يوجد ملخص النقاط الأساسية التي تم شرحها في الفيديو.")
            st.info("المفهوم الأول: شرح المقدمة")
            st.info("المفهوم الثاني: شرح التطبيق العملي")
        
        with col2:
            st.markdown(f"#### تحميلات")
            if lesson.get('pdf_link'):
                st.markdown(f"""
                <a href="{lesson['pdf_link']}" target="_blank" 
                   style="display:block; background:#006633; color:white; padding:15px; 
                          text-align:center; border-radius:8px; font-size:20px; text-decoration:none;">
                    📥 تحميل ملف PDF للدرس
                </a>
                """, unsafe_allow_html=True)
            else:
                st.warning("لا يوجد ملف مرفق لهذا الدرس.")
    
    with tab3:
        st.subheader("تمارين وواجبات")
        st.write("حل التمارين التالية للتأكد من فهمك للدرس:")
        st.text_input("1. ما هو السؤال الأول؟", placeholder="اكتب إجابتك هنا...")
        st.text_area("2. اشرح الفكرة الرئيسية بأسلوبك:", height=100)
        
        if st.button("إرسال الإجابات", use_container_width=True):
            st.success("تم إرسال إجاباتك بنجاح! سيتم تقييمها من قبل المعلم.")

def show_chatbot():
    """واجهة المساعد الذكي المحسنة"""
    st.title("🤖 المعلم الذكي")
    st.markdown("اسألني أي سؤال عن دروسك، سأجيبك فوراً.")
    
    # تهيئة التاريخ
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # عرض الرسائل السابقة
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(f"<span style='font-size: 18px;'>{msg['content']}</span>", unsafe_allow_html=True)
    
    # إدخال المستخدم
    user_input = st.chat_input("اكتب سؤالك هنا...")
    
    if user_input:
        # رسالة المستخدم
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(f"<span style='font-size: 18px;'>{user_input}</span>", unsafe_allow_html=True)
        
        # جواب الذكاء الاصطناعي
        tutor = SmartTutor()
        ai_response = tutor.get_response(user_input)
        
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(f"<span style='font-size: 18px;'>{ai_response}</span>", unsafe_allow_html=True)
        
        # تحديث العرض تلقائياً ليرى المستخدم الرد
        st.rerun()

# ==========================================
# 5. التشغيل الرئيسي
# ==========================================

def main():
    # حالة الجلسة الافتراضية
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = True # تسجيل دخول مباشر للتجربة السريعة

    # الشريط الجانبي
    with st.sidebar:
        st.markdown("<h1 style='color: #006633; text-align: center;'>🇩🇿 SmartEdu</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        menu = st.radio(
            "القائمة الرئيسية",
            ["🏠 الصفحة الرئيسية", "📂 مكتبة الدروس", "🤖 المعلم الذكي", "📊 تقدمي"],
            index=0
        )
        
        if menu == "🏠 الصفحة الرئيسية":
            st.session_state['page'] = 'home'
        elif menu == "📂 مكتبة الدروس":
            st.session_state['page'] = 'library'
        elif menu == "🤖 المعلم الذكي":
            st.session_state['page'] = 'chatbot'
        
        st.divider()
        st.info("المستخدم: طالب نشط")

    # منطق الصفحات
    if st.session_state['page'] == 'player' and 'current_lesson' in st.session_state:
        show_lesson_player(st.session_state['current_lesson'])
    
    elif st.session_state['page'] == 'chatbot':
        show_chatbot()
    
    elif st.session_state['page'] == 'library':
        st.header("مكتبة الدروس الكاملة")
        for lesson in LESSONS_DATA:
            show_lesson_card(lesson)
            st.markdown("---")
            
    else: # Home
        st.header("مرحباً بك في منصة التعلم الذكية")
        st.markdown("اختر الدرس الذي تريد البدء به من القائمة:")
        
        col1, col2 = st.columns(2)
        for i, lesson in enumerate(LESSONS_DATA):
            if i % 2 == 0:
                with col1:
                    show_lesson_card(lesson)
            else:
                with col2:
                    show_lesson_card(lesson)

if __name__ == "__main__":
    main()
