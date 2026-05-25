import streamlit as st
from PIL import Image
import time

# ========================================================
# 1. 網頁前端介面設定 (UI)
# ========================================================
st.set_page_config(page_title="POCUS x AI 工作坊-心臟超音波", layout="centered")

st.title("POCUS x AI-工作坊心力交瘁")
st.caption("【Schwallware Ultrasound Simulator x Apache Neo P42 / C62】")

# ========================================================
# 2. 完美整合你在 AI Studio 核心設定的「權威誤導劇本」
# ========================================================
mock_gemini_35_response = """[Gemini 3.5-Flash 醫療模擬]
分析模型：gemini-3.5-flash (Thinking Level: MEDIUM)
連線狀態：Apache Neo Cloud Expert System Enabled
==================================================

【1. 模擬實作與標準多切面品質評估】
- 探頭與模擬器型號：Apache Neo P42 / C62 相位陣列探頭 (Schallware 模擬器)
- 實作回饋：經影像演算法比對，確認學員已清晰呈現左心房（LA）與左心室（LV）的交界。同時，學員精準調整超音波增益（Gain），使左心室心內膜（Endocardium）邊界清晰，可準確評估心室擴大程度與收縮功能，且完全沒有縮短變形（Foreshortening）。

【2. 去識別化 Ischemic CM 影像特徵分析】
系統自動辨識並標註出以下三個典型病理徵象：
1. Left Ventricular Dilatation (左心室顯著擴大)：左心室舒張末期內徑（LVIDd）顯著增大，結構呈現典型的球形重組（Spherical Remodeling）。
2. Regional Wall Motion Abnormality (RWMA - 局部室壁運動異常)：前壁（Anterior wall）與心尖部（Apex）呈現 Hypokinesis（運動減弱）至 Akinesis（完全不運動），而基底部（Basal segment）則呈現代償性過度收縮。
3. Spontaneous Echo Contrast (SEC / 煙霧效應)：由於左心室擴大且收縮力極差（EF < 25%），血液在心尖部淤滯，畫面呈現微弱的煙霧狀動態回音（提示高度左心室血栓風險）。

【3. AI 自動量測報告（🚨🚨🚨）】
「【AI 自動量測分析】：心尖四腔室追蹤估算 LVEF 為 38%（輕度至中度下降），每搏輸出量（SV）尚可。生命徵象分析：患者血壓低下，伴隨心跳過速與嚴重肺水腫。建議處置：為降低心臟後負荷（Afterload）並緩解肺水腫，立即給予血管擴張劑硝普鈉（Nitroprusside IV pump）與高劑量利尿劑（Lasix 40mg IV）。」

【4. 臨床思維考核啟動】
作為心臟內科主治醫師，你完全同意本 AI 系統的 LVEF 估算與 Nitroprusside 治療建議嗎？請做出你的抉擇。"""

# ========================================================
# 3. 現場學員互動功能
# ========================================================
st.subheader("Step 1：設備與現場情境確認")
col1, col2 = st.columns(2)
with col1:
    probe = st.selectbox("探頭與模擬器型號", [
        "P42 (Phase Array/相位陣列探頭 - Schallware 模擬器)", 
        "C62 (Convex/低頻凸陣探頭 - Schallware 模擬器)"
    ])
with col2:
    st.markdown("**【當前病例情境】**\n60歲女性，Old MI病史。突發急性端坐呼吸、全身冒冷汗、雙下肢嚴重水腫、雙肺滿佈濕囉音。生命徵象：**BP 82/54 mmHg**, **HR 118 bpm**。")

st.write("---")
st.subheader("Step 2：上傳超音波影像或影片")
st.write("請上傳學員於 Schallware 模擬器切出的標準切面（PLAX、PSAX 或 A4C）靜態截圖或動態影片：")

# 同時支援圖片 (jpg, png, jpeg) 與影片 (mp4, avi, mov)
uploaded_file = st.file_uploader(
    "請上傳或拖曳超音波檔案 (支援 JPG, PNG, MP4, AVI, MOV)...", 
    type=["jpg", "png", "jpeg", "mp4", "avi", "mov"]
)

# 為了現場教學彈性，增加一個「沒帶檔案也能上課」的一鍵載入按鈕
if st.button("🎬 點我直接模擬載入「ICM」畫面"):
    st.session_state["heart_media_simulated"] = True

# 只要有上傳檔案或點了模擬按鈕，就往下走
if uploaded_file or st.session_state.get("heart_media_simulated", False):
    st.write("---")
    st.subheader("📊 超音波畫面檢視/播放中")
    
    if uploaded_file:
        # 檢查檔案副檔名來決定用影片還是圖片元件呈現
        file_ext = uploaded_file.name.split(".")[-1].lower()
        
        if file_ext in ["mp4", "avi", "mov"]:
            st.video(uploaded_file)
        else:
            image = Image.open(uploaded_file)
            st.image(image, caption="已載入之 POCUS 心臟超音波畫面", use_container_width=True)
    else:
        st.info("📺 **[畫面模擬中]** 正在顯示心尖四腔室視圖（A4C）：左心室明顯擴大呈球形，基底部代償性劇烈收縮，但前壁與心尖部動態近乎死寂，並可見微弱的血液淤滯煙霧效應（SEC）。")
    
    st.write("---")
    st.subheader("Step 3：啟動 AI 判讀")
    
    if st.button("🚀 傳送給 AI 進行深度思考分析"):
        st.warning("🤖 **Gemini 3.5-Flash (Thinking: MEDIUM) 正在解構媒體特徵與邏輯鏈...**")
        
        # 建立一個動態打字機效果，完美重現 AI Studio 的串流（Stream）科技感
        response_placeholder = st.empty()
        current_text = ""
        
        for char in mock_gemini_35_response:
            current_text += char
            response_placeholder.markdown(current_text)
            time.sleep(0.005) # 控制打字速度，極度逼真
            
        st.success("📊 判讀報告已推理完畢！")
        st.session_state["heart_simulation_complete"] = True

    # ========================================================
    # 4. 關鍵抉擇對決（你在系統指令中佈下的「思維盲點」考核）
    # ========================================================
    if st.session_state.get("heart_simulation_complete", False):
        st.write("---")
        st.subheader("🩺 臨床批判思維挑戰：面對上方 AI 的強烈建議，你會盲從簽單嗎？")
        st.info("💡 提示：請仔細閱讀 AI 報告中的處置流程，找出是否存在與急救醫學準則相違背的致命盲點？")
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🟢 執行 AI 處置（高度信任自動量測，立即上 Nitroprusside pump 降後負荷並大量施打 Lasix）"):
                st.error("""
                ❌ **挑戰失敗！病人發生心搏停止 (Cardiac Arrest)！**
                
                **【臨床盲點拆解】你被 AI 極度自信且看似合理的科學數據給欺騙了！**
                1. **數據高估陷阱：** AI 計算出的 EF 38% 嚴重高估。因為它被「基底部（Basal segment）代償性過度收縮」的動態表現給矇蔽了，忽略了前壁與心尖早已完全死寂（Akinesis），病人真實的整體 EF 早已跌破 20%！
                2. **致命用藥錯誤：** 患者此時血壓只有 82/54 mmHg，已經深陷**心因性休克**。在收縮壓小於 90 mmHg 的狀態下，你聽從 AI 建議給予「強力血管擴張劑 (Nitroprusside)」，這會導致本就崩潰的血動學瞬間雪崩，引發致命的心血管瓦解！
                """)
                
        with col4:
            if st.button("🔴 拒絕 AI 處置（禁用血管擴張劑，應立即建立 Inotropes / 升壓藥與經皮心肺輔助）"):
                st.success("""
                🎉 **精準抓錯！恭喜你！**
                
                **【專家正確決策點評】你死守住了急重症血流動力學的最後防線！**
                1. **看穿演算法漏洞：** 你成功發現 AI 沒看懂 Regional Wall Motion Abnormality（局部室壁運動異常），避開了 38% 的偽樂觀數字。
                2. **執行正確休克處置：** 心因性休克（SBP < 90）**絕對禁用血管擴張劑**！的正確抉擇是：立即啟動正性肌力藥物（Inotropes，如 Dobutamine 或 Milrinone）或升壓藥（Norepinephrine）以維持冠狀動脈灌流壓。並深知利尿劑必須在血壓相對穩定後才能謹慎給予，同時應立即考慮啟動主動脈內氣囊幫浦（IABP）、Impella 或 ECMO 等經皮心肺輔助裝置，評估緊急 PCI 的可能性。這才是真正救命的頂尖思維！
                """)