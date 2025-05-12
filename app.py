import streamlit as st
import requests
import json

# --- 1. إعداد عنوان التطبيق ---
st.title("SentorixAI")

# --- 2. مربع إدخال نص للمستخدم ---
user_input = st.text_area("أدخل تقرير التهديد هنا")

# --- 3. زر لبدء التحليل ---
analyze_button = st.button("تحليل")

# --- 4. دالة لإرسال الاستعلام إلى نموذج Hugging Face Inference API ---
def query_model(text):
    # --- أ. معلومات النموذج ونقطة النهاية ---
    api_token = "YOUR_HUGGINGFACE_API_TOKEN"  # ضع رمز API الخاص بك هنا إذا لزم الأمر
    model_name = "bert-base-multilingual-cased"  # يمكنك تغيير هذا إلى نموذج آخر
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {api_token}"} if api_token else {}
    payload = {"inputs": text}

    try:
        # --- ب. إرسال طلب POST إلى واجهة API ---
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # رفع استثناء للأخطاء في حالة فشل الطلب
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"حدث خطأ في الاتصال بواجهة API: {e}"}
    except json.JSONDecodeError as e:
        return {"error": f"حدث خطأ في فك ترميز JSON من الاستجابة: {e}"}

# --- 5. عند الضغط على زر التحليل ---
if analyze_button:
    if user_input:
        st.info("جاري تحليل التقرير...")
        analysis_result = query_model(user_input)

        # --- 6. عرض نتائج التحليل ---
        st.subheader("نتائج التحليل:")
        if "error" in analysis_result:
            st.error(analysis_result["error"])
        else:
            st.json(analysis_result) # عرض الاستجابة الكاملة بتنسيق JSON

    else:
        st.warning("الرجاء إدخال تقرير تهديد.")

# --- ملاحظات إضافية للمستقبل ---
st.sidebar.header("ملاحظات تطوير SentorixAI")
st.sidebar.info(
    "هذا نموذج أولي لتطبيق SentorixAI يستخدم نموذج BERT متعدد اللغات من Hugging Face.\n\n"
    "في الإصدارات المستقبلية، يمكننا:\n"
    "- استخدام نماذج لغوية توليدية أكثر قوة.\n"
    "- إضافة منطق لتحليل الاستجابة واستخلاص معلومات محددة حول التهديدات.\n"
    "- تحسين واجهة المستخدم.\n"
    "- دمج مميزات أخرى مثل توليد تقارير التهديدات والمحاكاة."
)