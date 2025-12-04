import streamlit as st
from phone_numerology import PhoneNumerology
import re

# 頁面配置
st.set_page_config(
    page_title="電話號碼命理分析系統",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定義 CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #ffffff !important;
        text-align: center;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    .subtitle {
        color: #f0f0f0;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        font-size: 16px;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px;
        font-size: 18px;
        font-weight: 600;
        margin-top: 1rem;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
    .result-box {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    .info-box {
        background: rgba(255, 255, 255, 0.95);
        border-left: 4px solid #2196f3;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    .stDownloadButton > button {
        background: #4caf50 !important;
        color: white !important;
        border-radius: 8px;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 標題
st.markdown("# 📱 電話號碼命理分析")
st.markdown('<p class="subtitle">使用八大數字磁場 × 八十一靈動數 × 五行相容性</p>', unsafe_allow_html=True)

# 資訊框
st.markdown("""
<div class="info-box">
    💡 <strong>免費線上分析工具</strong><br>
    輸入您的手機號碼和出生日期，立即獲得專業的命理分析報告
</div>
""", unsafe_allow_html=True)

# 創建兩欄輸入
col1, col2 = st.columns(2)

with col1:
    phone_number = st.text_input(
        "📞 手機號碼",
        placeholder="例: 0978-759-196",
        help="請輸入 09 開頭的台灣手機號碼"
    )

with col2:
    birthdate = st.text_input(
        "🎂 出生年月日",
        placeholder="例: 1990/09/25",
        help="格式: YYYY/MM/DD"
    )

# 分析按鈕
if st.button("🔮 開始分析", use_container_width=True):
    # 驗證輸入
    error_msg = None
    
    # 清理手機號碼
    clean_phone = re.sub(r'\D', '', phone_number)
    
    # 驗證手機號碼
    if not phone_number:
        error_msg = "請輸入手機號碼"
    elif not re.match(r'^09\d{8}$', clean_phone):
        error_msg = "手機號碼格式不正確，請輸入 09 開頭的 10 位數字"
    
    # 驗證出生日期
    if not error_msg:
        if not birthdate:
            error_msg = "請輸入出生日期"
        elif not re.match(r'^\d{4}/\d{2}/\d{2}$', birthdate):
            error_msg = "出生日期格式不正確，請使用 YYYY/MM/DD 格式 (例: 1990/09/25)"
        else:
            try:
                year, month, day = map(int, birthdate.split('/'))
                if not (1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31):
                    error_msg = "出生日期數值不正確，請檢查年月日"
            except:
                error_msg = "出生日期格式錯誤"
    
    # 顯示錯誤或執行分析
    if error_msg:
        st.error(f"❌ {error_msg}")
    else:
        # 格式化手機號碼
        formatted_phone = f"{clean_phone[:4]}-{clean_phone[4:7]}-{clean_phone[7:]}"
        
        try:
            with st.spinner('🔮 分析中...'):
                # 執行分析
                analyzer = PhoneNumerology(birthdate)
                report = analyzer.generate_report(formatted_phone)
                analysis = analyzer.comprehensive_analysis(formatted_phone)
            
            # 顯示結果
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            
            # 綜合評分 - 使用大字體和顏色
            score = analysis['final_score']
            if score >= 80:
                score_color = "#4caf50"
            elif score >= 70:
                score_color = "#8bc34a"
            elif score >= 60:
                score_color = "#ffc107"
            elif score >= 50:
                score_color = "#ff9800"
            else:
                score_color = "#f44336"
            
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="color: #667eea; margin-bottom: 0.5rem;">📊 分析結果</h2>
                <div style="font-size: 3rem; font-weight: bold; color: {score_color}; margin: 1rem 0;">
                    {score}/100
                </div>
                <div style="font-size: 1.5rem; color: #666;">
                    {analysis['recommendation']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 詳細報告
            st.markdown("### 📄 詳細分析報告")
            st.code(report, language=None)
            
            # 下載按鈕
            st.download_button(
                label="💾 下載完整報告",
                data=report,
                file_name=f"{clean_phone}_分析報告.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 顯示額外資訊
            with st.expander("📈 查看詳細數據"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "磁場評分",
                        f"{analysis['magnetic_fields']['total_score']:.1f}",
                        help="八大數字磁場分析得分"
                    )
                
                with col2:
                    st.metric(
                        "靈動數",
                        analysis['lingdong_81']['lingdong_number'],
                        analysis['lingdong_81']['type'],
                        help="八十一靈動數"
                    )
                
                with col3:
                    st.metric(
                        "五行相容",
                        analysis['five_elements']['compatibility_score'],
                        analysis['five_elements']['birth_element'],
                        help="五行相容性評分"
                    )
                
                # 磁場分布
                if analysis['magnetic_fields']['field_counts']:
                    st.markdown("#### 🧲 磁場分布")
                    for field_name, count in analysis['magnetic_fields']['field_counts'].items():
                        st.write(f"**{field_name}**: {count} 次")
        
        except Exception as e:
            st.error(f"❌ 分析過程發生錯誤: {str(e)}")

# 側邊欄資訊
with st.sidebar:
    st.markdown("### 📚 關於本系統")
    st.markdown("""
    本系統使用傳統中華命理學方法分析電話號碼:
    
    - **八大數字磁場**: 分析連續數字組合
    - **八十一靈動數**: 計算整體能量
    - **五行相容性**: 配合出生日期分析
    
    ⚠️ **免責聲明**: 分析結果僅供參考娛樂，請以個人喜好為主。
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 相關連結")
    st.markdown("""
    - [GitHub Repository](https://github.com/friday0925/phone-number-numerology)
    - [使用說明](https://github.com/friday0925/phone-number-numerology#readme)
    """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        Made with ❤️ using Streamlit
    </div>
    """, unsafe_allow_html=True)

# 頁腳
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 2rem;">
    電話號碼命理分析系統 | Powered by Streamlit
</div>
""", unsafe_allow_html=True)
