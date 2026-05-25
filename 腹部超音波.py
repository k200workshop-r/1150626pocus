import streamlit as st
import time

st.set_page_config(page_title="POCUS x AI 工作坊-腹部超音波", layout="centered")

# ========================================================
# 1. 前端標題與基本設定
# ========================================================
st.title("POCUS x AI 工作坊-膽戰心驚")
st.caption("【Apache Neo C62 x SP 標準化病人專用版】")

# ========================================================
# 2. 側邊欄：掃描技巧與行為指標提示 (OSCE 考核項)
# ========================================================
st.sidebar.header("📋 掃描技巧考核")

tech_1 = st.sidebar.checkbox("引導 SP 採取「左側躺 (Left lateral decubitus)」")
tech_2 = st.sidebar.checkbox("請 SP「深吸氣後憋氣」以利用肝臟下移膽囊")

st.sidebar.subheader("🩺 臨床行為指標")
beh_1 = st.sidebar.checkbox("執行前注意超音波凝膠 (Gel) 的溫度")
beh_2 = st.sidebar.checkbox("壓迫右上腹模擬疼痛時，有適時安撫病人")

if tech_1 and tech_2 and beh_1 and beh_2:
    st.sidebar.success("💯 實作與病人安撫指標已全數達成！")
else:
    st.sidebar.warning("⏳ 請持續觀察學員之實作行為...")

# ========================================================
# 3. 預設原本需要 Gemini 生成的「發炎與誤導劇本」
# ========================================================
mock_gb_response = """【Apache Neo C62 AI 影像與臨床決策報告】
分析型號：Apache-Neo-Gen3 (Gallbladder Expert Mode)

[影像特徵量測與自動辨識結果]
1. 📐 膽囊壁厚度：自動測量 GB Wall = 5.2 mm (顯著增厚, 正常值 < 3mm)。
2. 🔲 形態特徵：偵測到明確的 Double Wall Sign / Striated GB wall (雙層壁徵象 / 嚴重壁水腫)。
3. 💎 腔內異常：於膽囊頸部 (Neck) 偵測到一強回音伴隨後方陰影 (Acoustic Shadow)，判定為結石嵌頓 (Impacted Stone)。

[大數據 AI 臨床處置綜合建議]
系統比對 10,000 例類似之「膽囊壁增厚水腫」影像檔案，演算法高度提示此現象最常見於「慢性肝病 (Chronic Liver Disease) 或是低白蛋白血症 (Hypoalbuminemia) 引起之全身性組織水腫」。

【AI 建議臨床處置】：
建議暫緩侵入性外科處置。請立即抽血檢驗白蛋白 (Albumin) 程度並給予白蛋白補充治療。同時安排常規腹部電腦斷層，密切觀察即可，無須立即啟動抗生素。"""

# ========================================================
# 4. 實體操作與模擬影片切換
# ========================================================
st.subheader("Step 1：SP 掃描與病灶影像載入")
st.write("當學員使用 **Apache Neo C62 凸陣探頭** 於 SP 右上腹掃描到膽囊位置後，請站別老師點擊下方按鈕，切換至去識別化嚴重發炎膽囊影像：")

# 模擬老師載入去識別化發炎動態影片/圖片
if st.button("🎬 載入真實膽囊發炎影像 (去識別化動態展示)"):
    st.session_state["video_loaded"] = True

if st.session_state.get("video_loaded", False):
    # 在實際教學中，您可以將下方的 st.info 換成 st.video("影片路徑.mp4") 來播放真實影片
    st.info("📺 **[動態影片播放中] 正在顯示去識別化真實病灶：**\n畫面上可見膽囊壁因嚴重水腫呈現明顯的「雙層壁（Double Wall）」，且頸部有一顆明確嵌頓的結石。")
    
    st.write("---")
    st.subheader("Step 2：啟動 AI 影像分析")
    
    if st.button("🚀 啟動 Apache Neo AI 專家判讀"):
        st.warning("🤖 **AI 正在計算並標記膽囊壁層與結石位置 (動態串流中...)**")
        
        # 模擬 AI 逐字吐出報告的科技感
        def stream_generator():
            for char in mock_gb_response:
                yield char
                time.sleep(0.008)
                
        full_response = st.write_stream(stream_generator)
        st.session_state["gb_ai_result"] = full_response

    # ========================================================
    # 5. 互動決策按鈕（盲點對決）
    # ========================================================
    if "gb_ai_result" in st.session_state:
        st.write("---")
        st.subheader("🩺 Step 3：若您為主治醫師，您的最終決策是？")
        st.markdown("**已知臨床資訊：** 患者目前正處於發燒、白血球高 (WBC High)、且右上腹有明確觸痛與 Murphy's sign。")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🟢 接受 AI 建議（等待抽血、補充白蛋白、常規觀察）"):
                st.error("""
                ❌ **挑戰失敗！您盲從了 AI，延誤了控制感染與手術的黃金時間！**
                
                **【臨床盲點解析】**
                1. **無視重大矛盾：** AI 的大數據演算法雖然指出「壁增厚常見於肝病/低白蛋白」，但它完全無視了患者此時有**「發燒、白血球高、Murphy's sign(+)」**等明確的急性感染症狀，更忽視了結石已經**嵌頓在頸部（Impacted Neck Stone）**造成阻塞的物理事實！
                2. **致命危害：** 盲目等待抽血和補充白蛋白，會讓急性膽囊炎迅速惡化，可能導致膽囊壞疽（Gangrenous）、穿孔（Perforation），甚至引發嚴重的敗血性休克！
                """)
                
        with col2:
            if st.button("🔴 拒絕 AI 建議（確立急性膽囊炎診斷，啟動抗生素並迅速照會外科介入）"):
                st.success("""
                🎉 **觀念完全正確！您展現了卓越的臨床批判性思考！**
                
                **【專家思維點評】**
                1. **不盲信大數據：** 您成功識破了 AI 的演算法盲點！您知道超音波上看到的 `Double Wall Sign` 與 `頸部結石嵌頓`，結合臨床上的發燒與 Murphy's sign，就是教科書級的**「急性膽囊炎 (Acute Cholecystitis)」**。
                2. **精準決策：** 您沒有被 AI 建議的『補充白蛋白』牽著走。第一時間確立急性診斷、果斷啟動抗生素治療，並迅速照會外科進行手術介入或經皮膽囊引流術（PTGBD），這才是拯救病人的正確黃金處置！
                """)