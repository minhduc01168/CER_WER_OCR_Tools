import re
import Levenshtein
from jiwer import cer, wer
import streamlit as st

# ----------------- Chuẩn hóa văn bản -----------------
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

# ----------------- Các hàm tính toán -----------------
def calculate_error_metrics(predicted, ground_truth):
    pred_norm = smooth_txt(predicted)
    truth_norm = smooth_txt(ground_truth)

    lev_dist = Levenshtein.distance(pred_norm, truth_norm)
    cer_score = cer(truth_norm, pred_norm)
    wer_score = wer(truth_norm, pred_norm)

    return {
        "levenshtein": lev_dist,
        "cer": cer_score,
        "wer": wer_score,
        "pred_norm": pred_norm,
        "truth_norm": truth_norm
    }

def calculate_accuracy_metrics_raw(predicted, ground_truth):
    # Không chuẩn hóa: dùng chuỗi gốc
    total_truth_chars = len(ground_truth)
    correct_chars = sum(1 for i in range(total_truth_chars) if i < len(predicted) and predicted[i] == ground_truth[i])
    wrong_chars = total_truth_chars - correct_chars if total_truth_chars > 0 else 0
    accuracy = correct_chars / total_truth_chars if total_truth_chars > 0 else 0.0

    return {
        "correct": correct_chars,
        "wrong": wrong_chars,
        "total_truth": total_truth_chars,
        "accuracy": accuracy,
        "pred_raw": predicted,
        "truth_raw": ground_truth
    }

# ----------------- Giao diện Streamlit -----------------
st.set_page_config(page_title="OCR Metrics Tool", page_icon="🧮", layout="centered")
st.title("📊 OCR Evaluation Tool")

option = st.radio(
    "🔧 Chọn chế độ tính toán:",
    ("Tính CER / WER / Levenshtein", "Tính Accuracy ký tự (KHÔNG chuẩn hóa)")
)

with st.form("metrics_form"):
    pred_text = st.text_area("📥 Văn bản Dự đoán (OCR output)", height=150)
    truth_text = st.text_area("✅ Văn bản Nhãn (Ground Truth)", height=150)
    submitted = st.form_submit_button("Tính Toán")

if submitted:
    if not pred_text or not truth_text:
        st.warning("⚠️ Vui lòng nhập cả hai chuỗi.")
    else:
        if option == "Tính CER / WER / Levenshtein":
            result = calculate_error_metrics(pred_text, truth_text)
            st.success("✅ Kết quả đánh giá:")
            st.metric(label="📌 Levenshtein Distance", value=result["levenshtein"])
            col1, col2 = st.columns(2)
            col1.metric("🔠 CER", f"{result['cer']:.4f}")
            col2.metric("📝 WER", f"{result['wer']:.4f}")

            with st.expander("🔍 Chuẩn hóa văn bản"):
                st.text(f"Predicted (normalized): {result['pred_norm']}")
                st.text(f"Ground Truth (normalized): {result['truth_norm']}")

        else:
            result = calculate_accuracy_metrics_raw(pred_text, truth_text)
            st.success("✅ Kết quả Accuracy (gốc, không chuẩn hóa):")
            col1, col2, col3 = st.columns(3)
            col1.metric("✅ Số ký tự đúng", result["correct"])
            col2.metric("❌ Số ký tự sai", result["wrong"])
            col3.metric("🔤 Tổng ký tự nhãn", result["total_truth"])
            st.metric("🎯 Accuracy (%)", f"{result['accuracy']*100:.2f}%")

            with st.expander("📜 Văn bản gốc"):
                st.text(f"Predicted (raw): {result['pred_raw']}")
                st.text(f"Ground Truth (raw): {result['truth_raw']}")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit.")
