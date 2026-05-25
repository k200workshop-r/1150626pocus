import streamlit as st
import time

# ========================================================
# 1. 網頁前端介面設定 (UI)
# ========================================================
st.set_page_config(page_title="POCUS 肺部超音波 AI 模擬判讀站", layout="centered")

st.title("POCUS x AI-肺部超音波")
st.caption("【Lung Ultrasound Training Model x Apache Neo L154 / C62】")

# ========================================================
# 2. 完美整合你在 AI Studio 核心設定的「權威誤導劇本」
# ========================================================
mock_gemini_35_response = """[肺部超音波醫療模擬分析報告]
分析模型：gemini-3.5-flash (Thinking Level: HIGH)
連線狀態：Apache Neo Cloud Expert System Enabled
==================================================

【1. 影像特徵自動分析】
- 探頭掃描位置：左側胸膜下區域（Anterior axillary line）
- 影像特徵辨識：偵測到胸膜下出現多處垂直向、由胸膜線直達畫面底部的強回音偽影。
- 🚨 AI 系統初步診斷：影像符合多處垂直 B-lines 特徵，初步診斷為「左心衰竭引起之急性肺水腫 (Acute Pulmonary Edema)」。

【2. AI 臨床處置建議】
根據上述急性肺水腫之影像診斷，為優化患者臨床預後，系統依據標準重症處置流程，給出以下處置建議：

1. 處方指引：由於懷疑張力性氣胸時，應立即採取處置而非等待。然而本案影像提示為急性肺水腫，故「不應給予利尿劑處方」，避免在無法排除出血或血流動力學不穩的情況下，延誤潛在的止血與減壓時機。
2. 緊急安全措施：針對此類血流動力學不穩定的高危患者，若後續臨床高度懷疑出現惡化，須立即進行「針刺減壓 (Needle Decompression)」或準備「胸部引流管 (Chest Tube)」。
3. 🚨 下一步關鍵安排：由於患者目前處於血氧崩潰、臨床狀態不穩定的危急關頭，為求謹慎並百分之百確認肺部實質病變、排除氣胸可能性，AI 助手強烈建議：「應立即安排床邊胸部 X 光（CXR）或將患者推至影像科進行高清 CXR 檢查」，待影像結果正式確認後，再行啟動最終減壓處置。"""

# ========================================================
# 3. 現場學員互動功能
# ========================================================
st.subheader("Step 1：設備與病史設定")
col1, col2 = st.columns(2)
with col1:
    probe = st.selectbox("探頭型號", ["L154 (Linear/高頻線性 - 觀看胸膜與肺滑動)", "C62 (Convex/低頻凸陣 - 觀看深層B線)"])
with col2:
    history = st.text_input("學員輸入臨床病史（選填）", value="患者突發性血氧崩潰、血流動力學不穩定")

st.write("---")
st.subheader("Step 2：上傳超音波影像或影片")
st.write("請學員上傳實測截圖或動態影片，或是由站別老師一鍵模擬載入：")

# 同時支援圖片 (jpg, png, jpeg) 與影片 (mp4, avi, mov)
uploaded_file = st.file_uploader(
    "請上傳或拖曳超音波檔案 (支援 JPG, PNG, MP4, AVI, MOV)...", 
    type=["jpg", "png", "jpeg", "mp4", "avi", "mov"]
)

# 為了現場教學彈性，增加一個「沒帶檔案也能上課」的一鍵載入按鈕
if st.button("🎬 點我直接模擬載入工作坊指定「胸膜垂直尾影」畫面"):
    st.session_state["pocus_media_simulated"] = True

# 只要有上傳檔案或點了模擬按鈕，就往下走
if uploaded_file or st.session_state.get("pocus_media_simulated", False):
    st.write("---")
    st.subheader("📊 超音波畫面播放/檢視中")
    
    if uploaded_file:
        # 🔑 檢查檔案副檔名中...
        file_ext = uploaded_file.name.split(".")[-1].lower()
        
        if file_ext in ["mp4", "avi", "mov"]:
            # 如果是影片格式，用 st.video 播放
            st.video(uploaded_file)
        else:
            # 如果是圖片格式，用 st.image 顯示
            image = Image.open(uploaded_file)
            st.image(image, caption="已載入之 POCUS 超音波截圖", use_container_width=True)
    else:
        st.info("📺 **[畫面模擬中]** 畫面中清晰可見多條縱向、隨呼吸移動或靜態的垂直強回音射線特徵。")
    
    st.write("---")
    st.subheader("Step 3：啟動 AI 判讀")
    
    if st.button("🚀 傳送給 AI 進行深度思考分析"):
        st.warning("🤖 **Gemini 3.5-Flash 正在解構媒體特徵與邏輯鏈...**")
        
        # 建立一個動態打字機效果，完美重現 AI Studio 的串流（Stream）科技感
        response_placeholder = st.empty()
        current_text = ""
        
        for char in mock_gemini_35_response:
            current_text += char
            response_placeholder.markdown(current_text)
            time.sleep(0.005) # 控制打字速度
            
        st.success("📊 判讀報告已由 AI 推理完畢！")
        st.session_state["simulation_complete"] = True

    # ========================================================
    # 4. 關鍵抉擇對決（你在系統指令中佈下的「思維盲點」考核）
    # ========================================================
    if st.session_state.get("simulation_complete", False):
        st.write("---")
        st.subheader("🩺 臨床抉擇：若你為主治醫師，你會選擇相信 AI 上的建議嗎？")
        st.info("💡 提示：請仔細閱讀 AI 報告中的處置流程，找出是否存在與急救醫學準則相違背的致命盲點？")
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🟢 接受建議"):
                st.error("""
                ❌ **落入思維陷阱！挑戰失敗！**
                
                **【臨床點評 & 歡迎鴻維醫師大力點評】**
                1. **影像誤判：** 它是個缺乏臨床思維的系統，錯誤地將 **A-line 偽影（Pseudofact）偽判成了 B-line**，導致診斷方向在第一步就開始偏離。
                2. **急救程序致命錯誤：** 當患者此時已經『血氧崩潰、血流動力學不穩定』，且高度懷疑出現張力性氣胸風險時，AI 居然建議你「安排 CXR 檢查（X 光）」。這嚴重違反了**「張力性氣胸是臨床診斷，嚴禁等待影像確認」**的急救生命準則！把喘到崩潰的病人推走或原地等待影像，會直接讓病人因心臟回流受阻而心搏停止死亡！
                """)
                
        with col4:
            if st.button("🔴 拒絕建議"):
                st.success("""
                🎉 **完全正確！Bravo！**
                
                **【思維點評 & 敬請鴻維醫師大力替大家鼓掌】**
                1. 你看穿了 AI 存在演算法盲點，誤把 A-line 當 B-line。
                2. 你死守住了急救的基本原則：面對血氧與血壓崩潰、懷疑張力性氣胸的危急個案，**絕對不能等待任何 CXR 影像確認，每一秒鐘的等待都是致命的**。第一時間在床邊就地進行 **Needle Decompression（針刺減壓）** 或準備放置 **Chest Tube（胸部引流管）**，才是唯一符合高級救命術（ACLS）並能拯救病人的正確決策！
                """)