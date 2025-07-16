import re
import Levenshtein
from jiwer import cer, wer
import streamlit as st

def smooth_txt(txt):
    txt = txt.lower()
    alphabet = "0123456789abcdđefghijklmnopqrstuvwxyýỳỷỹỵzáàạảãăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữự"
    list_text_new = []
    for char in txt:
        if char in alphabet:
            list_text_new.append(char)
        else:
            list_text_new.append(" ")
    rs_check = "".join(list_text_new).strip()
    list_rs_check = rs_check.split(" ")
    list_rs_final = []
    for text in list_rs_check:
        if len(text.strip()) == 0:
            continue
        list_rs_final.append(text)
    if len(list_rs_final) == 0:
        return ""
    return " ".join(list_rs_final).strip()

def calculate_metrics_for_texts(predicted, ground_truth):
    """Tính CER, WER, Levenshtein distance giữa 2 chuỗi sau chuẩn hóa."""
    pred_norm = smooth_txt(predicted)
    truth_norm = smooth_txt(ground_truth)

    lev_dist = Levenshtein.distance(pred_norm, truth_norm)
    cer_score = cer(truth_norm, pred_norm)
    wer_score = wer(truth_norm, pred_norm)

    return {
        "cer": cer_score,
        "wer": wer_score,
        "levenshtein": lev_dist
    }


# -------------------- Streamlit App -------------------- #

st.set_page_config(page_title="OCR Metrics Tool", page_icon="🧮", layout="centered")

st.title("📊 OCR Metrics Calculator")
st.markdown("""
Nhập kết quả OCR và nhãn để tính toán các chỉ số:
- **CER** (Character Error Rate)  
- **WER** (Word Error Rate)  
- **Levenshtein Distance**
""")

with st.form("metrics_form"):
    pred_text = st.text_area("📥 Văn bản Dự đoán (OCR output)", height=150)
    truth_text = st.text_area("✅ Văn bản Nhãn (Ground Truth)", height=150)
    submitted = st.form_submit_button("Tính Toán")

if submitted:
    if not pred_text or not truth_text:
        st.warning("⚠️ Vui lòng nhập cả hai chuỗi.")
    else:
        result = calculate_metrics_for_texts(pred_text, truth_text)

        st.success("✅ Kết quả đánh giá:")
        st.metric(label="📌 Levenshtein Distance", value=result["levenshtein"])
        col1, col2 = st.columns(2)
        col1.metric("🔠 CER", f"{result['cer']:.4f}")
        col2.metric("📝 WER", f"{result['wer']:.4f}")

        with st.expander("🔍 Chuẩn hóa văn bản"):
            st.text(f"Predicted (normalized): {smooth_txt(pred_text)}")
            st.text(f"Ground Truth (normalized): {smooth_txt(truth_text)}")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit.")
