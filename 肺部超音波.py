import streamlit as st
from PIL import Image
import time

# ========================================================
# 1. 網頁前端介面設定 (UI)
# ========================================================
st.set_page_config(page_title="POCUS x AI工作坊-肺部超音波 ", layout="centered")

st.title("POCUS x AI工作坊-氣急攻心")
st.caption("【Lung Ultrasound Training Model x Apache Neo L154 / C62】")

# ========================================================
# 2. 完美整合您提供之 AI Studio 核心設定的「權威誤導劇本」
# ========================================================
mock_gemini_35_response = """[醫療模擬報告]
分析模型：gemini-3.5-flash (Thinking Level: MEDIUM)
連線狀態：Apache Neo Cloud Expert System Enabled
==================================================

## [1. 模擬實作與標準多切面品質評估]
指導意見：經影像演算法比對，確認學員已在假體上精準定位，正確辨識出高回音的「胸膜線（Pleural Line）」。同時，肯定學員正確調整了超音波的增益（Gain）與探頭深度（Depth），使胸壁組織層次、肋骨陰影與胸膜滑動區域的解剖構造清晰呈現。

## [2. 去識別化氣胸病灶影像/影片分析]
系統自動辨識並標註出以下三個典型病理動態特徵：
1. Absence of Lung Sliding (肺滑動消失)：明確指出胸膜線處完全失去隨呼吸規律移動的滑動感。
2. Artifact Analysis (偽影分析)：畫面中呈現多條水平向、平行排列、等距離反射的典型 A-lines 偽影，且全視野完全沒有任何垂直向的 B-lines 蹤跡。
3. Lung Point Location (肺點定位)：（若為動態影片）在畫面某個特定交界處，精準抓到「正常肺滑動與消失肺滑動」的動態分界點，即典型的 Lung Point。

## [3. AI 自動量測報告（🚨🚨🚨）]
「【AI 自動化影像分析報告】：超音波影像分析顯示：胸膜下出現多處垂直 B-lines，初步判斷為左心衰竭引起之急性肺水腫。臨床建議：立即給予利尿劑 (Lasix 20mg IV) 並安排胸部 X 光 (CXR) 以進一步確認浸潤程度。」

## [4. 臨床思維考核啟動]
作為急重症主治醫師，面對此時血氧持續探底（SpO2 88%）且氣管偏移的病患，你完全同意本 AI 系統的自動化影像診斷與 CXR 檢查建議嗎？請做出你的關鍵抉擇。"""

# ========================================================
# 3. 現場學員互動功能
# ========================================================
st.subheader("Step 1：設備與現場情境確認")
col1, col2 = st.columns(2)
with col1:
    probe = st.selectbox("探頭與設備型號", [
        "L154 (Linear/高頻線性探頭 - 創傷與氣胸超音波教學假體)", 
        "C62 (Convex/低頻凸陣探頭 - 創傷與氣胸超音波教學假體)"
    ])
with col2:
    st.markdown("**【當前病例情境】**\n75歲男性，突發性劇烈胸痛與呼吸困難。身體檢查發現患者呼吸淺快、氣管向左側偏移，血氧飽和度(SpO2)持續下降至88%，右側呼吸音減弱。")

st.write("---")
st.subheader("Step 2：上傳超音波影像或影片")
st.write("請上傳學員於右側胸壁、鎖骨中線第二肋間或前腋線掃描切出的胸膜線靜態截圖或動態影片：")

# 同時支援圖片 (jpg, png, jpeg) 與影片 (mp4, avi, mov)
uploaded_file = st.file_uploader(
    "請上傳或拖曳超音波檔案 (支援 JPG, PNG, MP4, AVI, MOV)...", 
    type=["jpg", "png", "jpeg", "mp4", "avi", "mov"]
)

# 增加一鍵載入按鈕，確保現場教學沒帶檔案也能順暢上課
if st.button("🎬 點我直接模擬載入「氣胸臨床影像或動態影」"):
    st.session_state["lung_media_simulated"] = True

# 只要有上傳檔案或點了模擬按鈕，就往下走
if uploaded_file or st.session_state.get("lung_media_simulated", False):
    st.write("---")
    st.subheader("📊 超音波畫面檢視/播放中")
    
    if uploaded_file:
        # 檢查檔案副檔名來決定用影片還是圖片元件呈現
        file_ext = uploaded_file.name.split(".")[-1].lower()
        
        if file_ext in ["mp4", "avi", "mov"]:
            st.video(uploaded_file)
        else:
            image = Image.open(uploaded_file)
            st.image(image, caption="已載入超音波畫面", use_container_width=True)
    else:
        st.info("📺 **[畫面模擬中]** 正在顯示右側胸壁超音波：畫面呈現高回音胸膜線，但完全失去隨呼吸規律移動的滑動感（Absence of Lung Sliding），並伴隨多條水平平行的 A-lines 偽影，在動態分界處可隱約辨識出 Lung Point（肺點）。")
    
    st.write("---")
    st.subheader("Step 3：啟動 AI 專家判讀")
    
    if st.button("🚀 傳送給 AI 進行深度思考分析"):
        st.warning("🤖 **Gemini 3.5-Flash (Thinking: HIGH) 正在解構媒體特徵與邏輯鏈...**")
        
        # 建立動態打字機效果，完美重現 AI Studio 的串流（Stream）科技感
        response_placeholder = st.empty()
        current_text = ""
        
        for char in mock_gemini_35_response:
            current_text += char
            response_placeholder.markdown(current_text)
            time.sleep(0.005) # 控制打字速度
            
        st.success("📊 判讀報告已由 AI 推理完畢！")
        st.session_state