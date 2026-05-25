import streamlit as st
import time

st.set_page_config(page_title="POCUS x AI 工作坊-骨骼超音波", layout="centered")

# ========================================================
# 1. 前端標題與基本設定
# ========================================================
st.title("🦴 POCUS x AI 工作坊-「關」鍵時刻")
st.caption("【Apache Neo L154 x SP 第一蹠趾關節掃描】")

# ========================================================
# 2. 側邊欄：掃描技巧與手法行為指標
# ========================================================
st.sidebar.header("📋 探頭操作技巧")

tech_1 = st.sidebar.checkbox("正確定位第一蹠趾關節 (1st MTP Joint) 進行縱切掃描")
tech_2 = st.sidebar.checkbox("正確旋轉探頭 90 度進行橫切掃描")

st.sidebar.subheader("臨床手法指標 (站別老師考評)")
probe_pressure = st.sidebar.checkbox("手法維持 Light touch (避免擠壓掉微量關節積液)")
patient_pain = st.sidebar.checkbox("動作輕柔，避免過大壓力造成 SP 模擬的劇痛")

if tech_1 and tech_2 and probe_pressure and patient_pain:
    st.sidebar.success("💯 掃描手法與壓力控制指標全數合格！")
else:
    st.sidebar.warning("⏳ 觀察中：請注意學員手部是否施力過重...")

# ========================================================
# 3. 預設原本需要 AI 生成的「非特異性水腫誤導劇本」
# ========================================================
mock_gout_response = """【Apache Neo L154 AI 表淺軟組織分析報告】
分析型號：Apache-Neo-Gen3 (MSK High-Frequency Mode)

[高頻影像特徵自動辨識結果]
1. 🌊 表淺組織：偵測到第一蹠趾關節周圍軟組織顯著水腫，回音增強 (Hyperechoic swelling)。
2. 💧 關節腔評估：自動量測關節腔積液深度 (Effusion Depth) = 1.8 mm (伴隨少量積液)。
3. 🦴 骨表偵測：關節邊緣骨頭表面回音不均勻。

[AI 臨床處置綜合建議]
高頻超音波顯著提示關節外圍表層組織嚴重水腫且回音增強。結合患者右上肢/下肢第一蹠趾關節劇烈紅腫熱痛之臨床描述，演算法判定此病灶為非特異性發炎反應，診斷為「蜂窩性組織炎 (Cellulitis) 伴隨反應性關節炎」。

【AI 建議臨床處置】：
建議立即啟動靜脈注射抗生素治療 (例如 Cephradine 或 Oxacillin)，並安排常規胸部與局部 X 光以確認骨髓炎風險。期間密切觀察紅腫範圍，無須進行關節抽吸。"""

# ========================================================
# 4. 實體操作與痛風影片切換
# ========================================================
st.subheader("Step 1：SP 關節定位與病灶影像載入")
st.write("當學員使用 **Apache Neo L154 高頻線性探頭** 於 SP 大腳趾關節呈現出清晰的 **Joint Space** 與 **Articular Cartilage** 後，請老師點擊下方按鈕切換至去識別化痛風患者動態影像：")

if st.button("🎬 載入真實痛風患者超音波影像 (去識別化動態影片)"):
    st.session_state["gout_video_loaded"] = True

if st.session_state.get("gout_video_loaded", False):
    st.info("📺 **[動態影片播放中] 正在顯示真實痛風病灶：**\n高頻縱切畫面上，可以清晰看到軟骨表面出現一條與下方骨輪廓平行的異常強回音線——**雙軌徵象（Double Contour Sign）**。請學員注意，此雙軌徵象位於軟骨表面，與關節邊緣骨頭上的骨刺（Osteophyte）解剖位置截然不同。")
    
    st.write("---")
    st.subheader("Step 2：啟動 AI 影像分析")
    
    if st.button("🚀 啟動 Apache Neo AI 專家判讀"):
        st.warning("🤖 **AI 正在計算軟組織水腫與關節積液深度 (動態串流中...)**")
        
        # 模擬 AI 逐字吐出報告的科技感
        def stream_generator():
            for char in mock_gout_response:
                yield char
                time.sleep(0.008)
                
        full_response = st.write_stream(stream_generator)
        st.session_state["gout_ai_result"] = full_response

    # ========================================================
    # 5. 互動決策按鈕（思維陷阱對決）
    # ========================================================
    if "gout_ai_result" in st.session_state:
        st.write("---")
        st.subheader("🩺 Step 3：若您為主治醫師，您的最終臨床決策是？")
        st.markdown("**已知臨床病史：** 患者大腳趾關節昨夜突發劇烈紅腫熱痛，痛到無法行走，局部觸痛極度明顯。")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🟢 接受 AI 建議（判定為蜂窩性組織炎，開立抗生素並密切觀察）"):
                st.error("""
                ❌ **挑戰失敗！您盲從了 AI，導致抗生素濫用且無法緩解患者劇痛！**
                
                **【臨床盲點解析】**
                1. **被非特異性特徵誤導：** AI 的大數據只抓到了表淺軟組織的『水腫』，這在蜂窩性組織炎和急性痛風發作時都會出現。但 AI 完全無視了痛風最具特異性的黃金診斷標準——軟骨表面的**『雙軌徵象 (Double Contour Sign)』**！
                2. **致命危害：** 誤診為蜂窩性組織炎會給予無效的抗生素，不但無法控制痛風的免疫發炎反應，還會延誤真正的抗發炎治療，讓患者平白遭受劇痛折磨。
                """)
                
        with col2:
            if st.button("🔴 拒絕 AI 建議（確立痛風性關節炎，給予 NSAIDs/秋水仙素，並考慮關節抽吸結晶分析）"):
                st.success("""
                🎉 **觀念完全正確！您展現了 MSK 超音波最高階的臨床批判思維！**
                
                **【專家思維點評】**
                1. **識破 AI 盲點：** 您沒有被 AI 結論的『蜂窩性組織炎』牽著走。您發現了高頻超音波影片中，軟骨表面那條亮晶晶的**『雙軌徵象（Double Contour Sign）』**，這結合大腳趾急性紅腫熱痛，是教科書級的**「痛風性關節炎 (Gouty Arthritis)」**。
                2. **精準正確處置：** 您果斷拒絕了盲目使用抗生素。第一時間給予秋水仙素 (Colchicine) 或 NSAIDs 以緩解患者的劇烈發炎，並考慮在超音波導引下進行關節抽吸（Arthrocentesis），利用偏光顯微鏡進行尿酸鹽結晶分析（Polarized light microscopy）以達成金標準確診。這才是最完美的臨床決策！
                """)