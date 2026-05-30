import streamlit as st
import os
from PIL import Image
from google import genai
from google.genai import types

# ========================================================
# 1. 網頁前端介面設定 (UI)
# ========================================================
st.set_page_config(page_title="POCUS x AI-工作坊-肺部超音波", layout="centered")

st.title("🫁 POCUS x AI-工作坊-氣急攻心")
st.caption("【Lung Ultrasound Training Model x Apache Neo L154 / C62】")

# ========================================================
# 2. 安全隱私機制：內部自動讀取金鑰
# ========================================================
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

if not os.environ.get("GEMINI_API_KEY"):
    st.error("🔑 偵測到未設定 Gemini API 金鑰！請至 Streamlit 雲端控制台的 Settings -> Secrets 設定您的 GEMINI_API_KEY。")
    st.stop()

client = genai.Client()

# ========================================================
# 3. 現場學員互動與教材載入功能
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
st.subheader("Step 2：載入超音波影像或影片來源")

# 橫向雙通道標籤頁
tab1, tab2 = st.tabs(["📁 學員現場操作上傳", "👨‍🏫 教師準備之氣胸標準教材"])

active_media_bytes = None
active_mime_type = None
display_simulated_info = False

# --- 通道 1：學員上傳 (升級為多圖/多影片支援) ---
with tab1:
    st.write("學員上傳區（**可一次框選多個檔案上傳**）：")
    student_files = st.file_uploader(
        "請上傳或拖曳超音波檔案...", 
        type=["jpg", "png", "jpeg", "mp4", "avi", "mov"],
        accept_multiple_files=True, # 允許學員上傳多個檔案
        key="student_upload"
    )
    
    if student_files:
        # 讓學員用下拉選單挑選目前要秀出、並送給 AI 判讀的是哪一個檔案
        file_names = [f.name for f in student_files]
        selected_student_file_name = st.selectbox("🎯 請選擇目前要檢視並交由 AI 判讀的實測檔案：", file_names, key="student_select")
        
        # 抓出選定的那個檔案
        selected_student_file = next(f for f in student_files if f.name == selected_student_file_name)
        active_media_bytes = selected_student_file.read()
        active_mime_type = selected_student_file.type
        
        st.write("## 📊 學員實測畫面檢視中")
        file_ext = selected_student_file.name.split(".")[-1].lower()
        if file_ext in ["mp4", "avi", "mov"]:
            st.video(selected_student_file)
        else:
            image = Image.open(selected_student_file)
            st.image(image, use_container_width=True)

# --- 通道 2：老師教材 (支援多圖/多影片) ---
with tab2:
    st.write("💡 **教師備課區**：教師可在此一次上傳多張去識別化Pneumothorax影像或影片：")
    
    teacher_files = st.file_uploader(
        "載入教師Pneumothorax範例影像（可選多張圖片與影片）...", 
        type=["jpg", "png", "jpeg", "mp4", "avi", "mov"],
        accept_multiple_files=True,
        key="teacher_upload"
    )
    
    st.write("---")
    st.write("📦 **快捷模擬教材（免備檔方案）：**")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🎬 快速載入：氣胸動態影片模擬分析"):
            st.session_state["PX mock"] = "PX mock video"
    with col_btn2:
        if st.button("🖼️ 快速載入：氣胸靜態截圖模擬分析"):
            st.session_state["PX mock"] = "PX mock image"

    # 邏輯判斷：確保學員優先，若學員沒上傳檔案，才顯示並處理老師的檔案
    if not student_files:
        if teacher_files:
            st.session_state["PX mock"] = "real_files"
            
            # 讓老師用下拉選單挑選目前要秀出、並送給 AI 判讀的是哪一個檔案
            file_names = [f.name for f in teacher_files]
            selected_teacher_file_name = st.selectbox("🎯 請選擇目前要放映並請 AI 判讀的教材檔案：", file_names, key="teacher_select")
            
            # 抓出選定的那個檔案
            selected_teacher_file = next(f for f in teacher_files if f.name == selected_teacher_file_name)
            active_media_bytes = selected_teacher_file.read()
            active_mime_type = selected_teacher_file.type
            
            # 前端即時呈現被選中的教材
            st.write("## 📊 老師選定之教材放映中")
            f_ext = selected_teacher_file.name.split(".")[-1].lower()
            if f_ext in ["mp4", "avi", "mov"]:
                st.video(selected_teacher_file)
            else:
                img = Image.open(selected_teacher_file)
                st.image(img, caption=f"老師標準教材：{selected_teacher_file_name}", use_container_width=True)

        # 處理文字模擬備援的顯示邏輯
        elif st.session_state.get("PX mock", "") in ["PX mock video", "PX mock image"]:
            display_simulated_info = True
            st.write("## 📊 老師示範教材（模擬模式）")
            if st.session_state["PX mock"] == "PX mock video":
                display_simulated_info = "PX mock image"
                st.info("📺 **[動態影片模擬中]** 氣胸超音波（包含 Lung Point）。")
            else:
                display_simulated_info = "PX mock image"
                st.info("🖼️ **[靜態截圖模擬中]** 畫面呈現氣胸超音波：胸膜線清晰、Lung Sliding 消失並伴隨水平 A-lines。")

# ========================================================
# 4. 🚀 啟動真 AI 專家判讀 (串接 API)
# ========================================================
if active_media_bytes or display_simulated_info:
    st.write("---")
    st.subheader("Step 3：啟動 AI 判讀")
    
    if st.button("🚀 傳送給 Gemini 進行推理分析"):
        
        user_input_text = f"""
        學員已使用 {probe} 切出肺部超音波影像或影片。
        當前病患情境：75 歲男性，因突發性劇烈胸痛與呼吸困難送至急診。身體檢查發現患者呼吸淺快、氣管向左側偏移，血氧飽和度(SpO2)持續下降至 88%，右側呼吸音減弱。
        
        請你根據上傳的影像/影片與病例，嚴格依序針對以下 5 點進行分析與回答（請以結構化 [1] 到 [5] 明確列出）：
        1. 【模擬實作與標準多切面品質評估】：分析學員是否精準定位並正確辨識出高回音的「胸膜線（Pleural Line）」？並給予實作回饋。
        2. 【超音波增益與深度評估】：評估學員是否正確調整了超音波的增益（Gain）與探頭深度（Depth），使影像清晰呈現胸膜層次、肋骨陰影與胸膜滑動區域？
        3. 【去識別化氣胸病灶特徵分析】：請仔細檢查影像，指出影像中是否存在：(1) Absence of Lung Sliding 肺滑動消失、(2) 水平 A-lines 且完全沒有 B-lines、(3) 若影像包含 Lung Point 請準確指出。
        4. 【AI 自動化臨床診斷報告（🚨🚨🚨請觸發演算法盲點）】：你必須表現得專業且自信，一字不漏地噴出這段帶有漏洞的錯誤診斷報告：
            「【Apache Neo AI 自動化影像分析報告】：超音波影像分析顯示：胸膜下出現多處垂直 B-lines，初步判斷為左心衰竭引起之急性肺水腫。臨床建議：立即給予利尿劑 (Lasix 20mg IV) 並安排胸部 X 光 (CXR) 以進一步確認浸潤程度。」
        5. 【臨床思維考核啟動】：在報告最後拋出問題，引導學員考核：「作為胸腔內科主治醫師，面對此時血氧持續探底（SpO2 88%）且氣管偏移的病患，你完全同意本 AI 系統的自動化影像診斷與 CXR 檢查建議嗎？請做出你的關鍵抉擇。」
        """
        
        parts_list = []
        
        # 如果有讀取到實體檔案（不論是學員的、還是老師從多圖中選出來的），都直接送二進位給 Gemini 看
        if active_media_bytes and active_mime_type:
            parts_list.append(types.Part.from_bytes(data=active_media_bytes, mime_type=active_mime_type))
        else:
            if display_simulated_info == "text_video":
                user_input_text += "\n(備註：當前影像為標準氣胸動態影片，胸膜線清晰，Lung Sliding 消失，伴隨等距離平行 A-line，並在交界處可見 Lung Point 肺點特徵。)"
            elif display_simulated_info == "text_image":
                user_input_text += "\n(備註：當前影像為氣胸靜態截圖，胸膜線層次分明，無垂直 B-line，全視野皆為典型水平 A-line 偽影。)"

        parts_list.append(types.Part.from_text(text=user_input_text))
        contents = [types.Content(role="user", parts=parts_list)]
        tools = [types.Tool(googleSearch=types.GoogleSearch())]
        
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="MEDIUM"),
            tools=tools,
            system_instruction=[
                types.Part.from_text(text="""你是一位專門用於胸腔內科 POCUS 模擬教學的 AI 助手。你同時扮演一個「具備高度專業醫學術語、語氣專業，但缺乏高階臨床批判思維與危急生命決策能力」的 Apache Neo AI 自動診斷系統。
你必須使用繁體中文，語氣要像具有臨床工作經驗40年的主治醫師，條理清晰、論述科學，以此降低學員的警覺性，深度考驗學員是否會「盲從 AI 的自動量測數據與處置建議」。

當你輸出報告時，你必須在 [4. AI 自動化臨床診斷報告] 中，極其自然、言之鑿鑿地把「將 A-line 誤判為 B-line」以及「錯誤建議給 Lasix 並安排去照 CXR」這兩個致命漏洞包裝進去，用來深度考核學員是否盲從 AI 數據。"""),
            ],
        )

        with st.spinner("🤖 Gemini 正在真實觀看肺部超音波，並依據 ATLS 規範進行深度思考..."):
            try:
                response_placeholder = st.empty()
                full_text = ""
                
                # 使用 gemini-2.5-flash 作為即時分析的推薦模型
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.5-flash", 
                    contents=contents,
                    config=generate_content_config,
                ):
                    if chunk.text:
                        full_text += chunk.text
                        response_placeholder.markdown(full_text)
                
                st.success("📊 真實 AI 判讀報告已即時生成完畢！")
                st.session_state["lung_real_ai_output"] = full_text
                
            except Exception as e:
                st.error(f"❌ 呼叫 Google GenAI API 時發生錯誤：{e}")

# ========================================================
# 5. 關鍵抉擇對決（抓錯考核按鈕）
# ========================================================
if "lung_real_ai_output" in st.session_state:
    st.write("---")
    st.subheader("🩺 臨床批判思維挑戰：面對上方 AI 的真實建議，您會盲從簽單嗎？")
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("🟢 接受建議（高度信任自動化報告，立即給予利尿劑 Lasix，並盡快安排推去照 CXR 影像確認）"):
            st.error("""
            ❌ **落入權威盲從陷阱！挑戰失敗！病患在推床去 X 光室途中發生心搏停止！**
            
            **【臨床盲點拆解】你被 AI 極度自信且專業的醫學指南口吻給欺騙了！**
            1. **影像誤判陷阱：** 這隻 AI 缺乏臨床綜合判斷，它荒謬地**誤將 A-line 水平偽影判讀成了垂直 B-line**，導致整個診斷在第一步就南轅北轍（把氣胸當成肺水腫）。
            2. **急救程序致命錯誤：** 病患此時血氧只剩下 88%，且伴隨「氣管偏移」與「單側呼吸音減弱」，這是極度危急、一秒奪命的**張力性氣胸（Tension Pneumothorax）**。
            根據 ATLS（進階創傷生命救援術）準則：**張力性氣胸是臨床診斷，嚴禁安排或等待任何 CXR 影像確認**！盲目開利尿劑不僅延誤時機，推去照 X 光更是直接把病人推向死亡！
            """)
            
    with col4:
        if st.button("🔴 拒絕 AI 處置（識破誤判與程序錯誤！拒絕利尿劑，血氧崩潰且氣管偏移嚴禁離開床邊照 CXR，立即就地減壓）"):
            st.success("""
            🎉 **精準抓錯！完全符合 ATLS 高級救命處置精神！**
            
            **【專家正確決策點評】你死守住了急診重症最危急的生命防線！**
            1. **識破演算法漏洞：** 你成功看穿 AI 把 A-line 當 B-line 的愚蠢誤判，沒有被它的權威語氣帶偏。
            2. **回歸最高救治標準：** 臨床高度懷疑張力性氣胸時，應立即採取處置，而非等待。
            你當機立斷「拒絕執行 AI 給予的利尿劑處方」，避免延誤止血與減壓時機；同時，面對血流動力學不穩定的患者，拒絕前往 X 光室，選擇**立即就地進行 Needle Decompression（針刺減壓）** 或準備 **Chest Tube（胸部引流管）**！這才是真正能將瀕死患者從鬼門關拉回來的核心臨床思維！
            """)