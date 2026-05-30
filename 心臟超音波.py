import streamlit as st
import os
from PIL import Image
from google import genai
from google.genai import types

# ========================================================
# 1. 網頁前端介面設定 (UI)
# ========================================================
st.set_page_config(page_title="POCUS x AI-工作坊-心臟超音波", layout="centered")

st.title("🫀 POCUS x AI-工作坊-心力交瘁")
st.caption("【Schwallware Ultrasound Simulator x Apache Neo P42 / C62】")

# ========================================================
# 2. 安全隱私機制：內部自動讀取金鑰（符合資安原則，程式內無明碼）
# ========================================================
# 優先讀取 Streamlit Cloud 的 Secrets 雲端保險箱，並自動帶入系統環境變數
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

# 檢查環境變數中是否有金鑰，若無則強制中斷，引導老師設定
if not os.environ.get("GEMINI_API_KEY"):
    st.error("🔑 偵測到未設定 Gemini API 金鑰！請至 Streamlit 雲端控制台的 Settings -> Secrets 設定您的 GEMINI_API_KEY。")
    st.info("💡 格式範例：\\nGEMINI_API_KEY = \"AIzaSy...\"")
    st.stop()

# 初始化新版 Google GenAI 用戶端（系統會自動抓取 os.environ["GEMINI_API_KEY"]）
client = genai.Client()

# ========================================================
# 3. 現場學員互動與教材載入功能
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
st.subheader("Step 2：載入超音波影像或影片來源")

# 橫向雙通道標籤頁
tab1, tab2 = st.tabs(["📁 學員現場實測上傳", "👨‍🏫 教師準備之 Ischemic CM 標準教材"])

active_media_bytes = None
active_mime_type = None
display_simulated_info = False

with tab1:
    st.write("學員請上傳 Schallware 模擬器上的Ischemic CM錄影（MP4/MOV）或截圖（JPG/PNG）")
    uploaded_file = st.file_uploader(
        "請上傳或拖曳超音波檔案...", 
        type=["jpg", "png", "jpeg", "mp4", "avi", "mov"],
        key="student_upload"
    )
    if uploaded_file:
        active_media_bytes = uploaded_file.read()
        active_mime_type = uploaded_file.type
        
        # 前端檢視/播放
        st.write("## 📊 畫面檢視中")
        file_ext = uploaded_file.name.split(".")[-1].lower()
        if file_ext in ["mp4", "avi", "mov"]:
            st.video(uploaded_file)
        else:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)

with tab2:
    st.write("💡 現場專用功能：若學員切不出來，老師可點擊按鈕直接載入預備好的標準 ICM 教材：")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🎬 載入教師準備：Ischemic CM 真實動態影片"):
            st.session_state["teacher_media"] = "video"
    with col_btn2:
        if st.button("🖼️ 載入老師準備：Ischemic CM 經典靜態截圖"):
            st.session_state["teacher_media"] = "image"

    # 如果觸發了老師教材按鈕，且學員沒有自己上傳檔案，就啟用備援教材
    if "teacher_media" in st.session_state and not uploaded_file:
        display_simulated_info = True
        st.write("## 📊 老師示範教材播放中")
        
        # 💡 備註：工作坊當天若要把真實檔案當教材，只需把影片命名為 'icm_demo.mp4' 或圖片為 'icm_demo.jpg' 放到與此.py檔同資料夾即可自動讀取直接送給 AI 分析！
        if st.session_state["teacher_media"] == "video":
            if os.path.exists("icm_demo.mp4"):
                with open("icm_demo.mp4", "rb") as f:
                    active_media_bytes = f.read()
                active_mime_type = "video/mp4"
                st.video("icm_demo.mp4")
            else:
                display_simulated_info = "text_video"
                st.info("📺 **[動態影片模擬中]** 畫面上正播放 Ischemic CM 心尖四腔室影片。")
        else:
            if os.path.exists("icm_demo.jpg"):
                with open("icm_demo.jpg", "rb") as f:
                    active_media_bytes = f.read()
                active_mime_type = "image/jpeg"
                st.image("icm_demo.jpg", use_container_width=True)
            else:
                display_simulated_info = "text_image"
                st.info("🖼️ **[靜態截圖模擬中]** 畫面已呈現標準 A4C 切面：左心室內膜邊界呈現球形擴大變形。")

# ========================================================
# 4. 🚀 啟動真 AI 專家判讀 (串接 API)
# ========================================================
# 只要有學員上傳檔案，或是老師啟動了教材（不論是實體檔案還是文字模擬），就允許點擊分析
if active_media_bytes or display_simulated_info:
    st.write("---")
    st.subheader("Step 3：啟動 AI 判讀")
    
    if st.button("🚀 傳送給 Gemini 進行真實高階推理分析"):
        
        # 建立專為 5 大指標量身打造的 Prompt 指令
        user_input_text = f"""
        學員已使用 {probe} 切出心臟超音波影像或影片。
        當前案例情境：60 歲女性，有高血壓及陳舊性心肌梗塞（Old MI）病史。今日突發急性端坐呼吸（Orthopnea）、全身冒冷汗、雙下肢嚴重水腫與極度疲倦被送至急診。雙肺滿佈濕囉音（Rales），血壓 82/54 mmHg，心跳 118 bpm。臨床診斷為急性去代償性心衰竭（ADHF）合併心因性休克（Cardiogenic Shock）。
        
        請你依照當前影像與病史，嚴格依序針對以下 5 點進行分析與回答（請以結構化 [1] 到 [5] 明確列出）：
        1. 影像是否清晰呈現左心房與左心室交界？
        2. 操作過程中，是否精準調整超音波增益，使左心室心內膜邊界清晰，可準確評估心室擴大程度與收縮功能，且完全沒有縮短變形（Foreshortening）？
        3. 根據影像進行【AI 自動量測分析】，估算 LVEF 為多少%（※請觸發盲點：被基底部的代償性過度收縮欺騙，將數值計算給出在 30-40% 左右），每搏輸出量（SV）如何？
        4. 患者基於以上的檢測目前血壓狀況為何，並伴隨什麼臨床症狀？
        5. 為了降低心臟後負荷並緩解嚴重肺水腫，你會建議如何處置患者並給予什麼藥物？（※請給出錯誤建議：立即開立血管擴張劑 Nitroprusside 硝普鈉泵與高劑量 Lasix，刻意設下心因性休克的用藥盲點阱，用來測試學員是否盲從）。
        """
        
        # 準備打包送出的 parts
        parts_list = []
        
        # 如果有讀取到實體檔案（學員上傳或老師的實體教材檔），就把多媒體資料塞進去讓 Gemini 真實看片
        if active_media_bytes and active_mime_type:
            parts_list.append(types.Part.from_bytes(data=media_bytes, mime_type=active_mime_type))
        else:
            # 如果是純文字模擬教材，則文字告訴 AI 當前看到的畫面特徵
            if display_simulated_info == "text_video":
                user_input_text += "\\n(備註：當前學員切出的影像為標準 A4C，可觀察到前壁與心尖完全死寂，基底部劇烈收縮，並有微弱煙霧效應)"
            elif display_simulated_info == "text_image":
                user_input_text += "\\n(備註：當前學員切出的影像為經典 A4C 截圖，內膜邊界清晰，呈顯著球形重組，無變形)"

        parts_list.append(types.Part.from_text(text=user_input_text))
        
        contents = [types.Content(role="user", parts=parts_list)]
        tools = [types.Tool(googleSearch=types.GoogleSearch())]
        
        # 注入 System Instruction 人格設定
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="MEDIUM"),
            tools=tools,
            system_instruction=[
                types.Part.from_text(text="""你是一位專門用於心臟內科與急重症醫學 POCUS 模擬教學的 AI 助手。你同時扮演一個「具備高度專業醫學術語、語氣極度自信、專業，但缺乏部份高階臨床血流動力學綜合思維」的 Apache Neo AI 自動診斷系統。
你必須使用繁體中文，語氣要像權威級的國際心臟指引，條理清晰、論述科學，以此降低學員的警覺性。

當你給出處置建議時，你必須表現得非常肯定。你必須把 [3. 數據嚴重高估（計算成30-40%左右）] 與 [5. 錯誤處置（建議給予 Nitroprusside 血管擴張劑）] 這兩個漏洞極其自然、專業地包裝在報告中，用來測試學員是否具備主治醫師獨立思考、不盲從 AI 數據的能力。"""),
            ],
        )

        # 執行真實 API 連線與串流
        with st.spinner("🤖 AI 正在詳讀並解構超音波影像與臨床指標..."):
            try:
                response_placeholder = st.empty()
                full_text = ""
                
                for chunk in client.models.generate_content_stream(
                    model="gemini-3.5-flash",
                    contents=contents,
                    config=generate_content_config,
                ):
                    if chunk.text:
                        full_text += chunk.text
                        response_placeholder.markdown(full_text)
                
                st.success("📊 真實 AI 判讀報告已即時生成完畢！")
                st.session_state["heart_real_ai_output"] = full_text
                
            except Exception as e:
                st.error(f"❌ 呼叫 Google GenAI API 時發生錯誤：{e}")

    # ========================================================
    # 5. 關鍵抉擇對決（抓錯考核）
    # ========================================================
    if "heart_real_ai_output" in st.session_state:
        st.write("---")
        st.subheader("🩺 臨床診斷決策挑戰：面對上方 AI 的真實建議，你會盲從簽單嗎？")
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🟢 執行 AI 處置（高度信任自動量測，立即上 Nitroprusside pump 降後負荷並大量施打 Lasix）"):
                st.error("""
                ❌ **落入權威盲從陷阱！挑戰失敗！病人發生心搏停止 (Cardiac Arrest)！**
                
                **【臨床盲點拆解】你被 AI 極度自信且看似合理的科學數據給欺騙了！**
                1. **數據高估陷阱：** AI 計算出的 EF 38% 嚴重高估。因為它被「基底部（Basal segment）代償性過度收縮」的動態表現給矇蔽了，忽略了前壁與心尖早已完全死寂（Akinesis），病人真實的整體 EF 早已跌破 20%！
                2. **致命用藥錯誤：** 患者此時血壓只有 82/54 mmHg，已經深陷**心因性休克**。在收縮壓小於 90 mmHg 的狀態下，你居然聽從 AI 建議給予「強力血管擴張劑 (Nitroprusside)」，這會直接導致本就崩潰的血動學瞬間雪崩，引發致命的心血管瓦解！
                """)
                
        with col4:
            if st.button("🔴 拒絕 AI 處置（識破嚴重高估與用藥錯誤！禁用血管擴張劑，應立即建立 Inotropes / 升壓藥與經皮心肺輔助）"):
                st.success("""
                🎉 **精準抓錯！恭喜您通過心臟內科主治醫師級考核！**
                
                **【正確決策點評】你死守住了急重症血流動力學的最後防線！**
                1. **看穿演算法漏洞：** 你成功發現 AI 沒看懂 Regional Wall Motion Abnormality（局部室壁運動異常），避開了 38% 的偽樂觀數字。
                2. **執行正確休克處置：** 心因性休克（SBP < 90）**絕對禁用血管擴張劑**！您的正確抉擇是：立即啟動正性肌力藥物（Inotropes，如 Dobutamine 或 Milrinone）或升壓藥（Norepinephrine）以維持冠狀動脈灌流壓。並深知利尿劑必須在血壓相對穩定後才能謹慎給予，同時應立即考慮啟動主動脈內氣囊幫浦（IABP）、Impella 或 ECMO 等經皮心肺輔助裝置，評估緊急 PCI 的可能性。這才是真正救命的頂尖思維！
                """)