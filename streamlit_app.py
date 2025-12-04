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
    .main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #ffffff !important; text-align: center; font-size: 2.5rem !important; margin-bottom: 0.5rem !important; }
    .subtitle { color: #f0f0f0; text-align: center; font-size: 1.1rem; margin-bottom: 2rem; }
    .stTextInput > div > div > input {
        border-radius: 10px; border: 2px solid #e0e0e0; padding: 12px; font-size: 16px;
    }
    .stButton > button {
        width: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; border-radius: 10px; padding: 12px;
        font-size: 18px; font-weight: 600; margin-top: 1rem;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2); }
    .result-box {
        background: white; border-radius: 15px; padding: 25px;
        margin-top: 2rem; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    .info-box {
        background: rgba(255, 255, 255, 0.95); border-left: 4px solid #2196f3;
        padding: 15px; border-radius: 8px; margin-bottom: 1.5rem;
    }
    .stDownloadButton > button { background: #4caf50 !important; color: white !important; border-radius: 8px; margin-top: 1rem; }
    .recommendation-card {
        background: #f8f9fa; border-left: 4px solid #667eea;
        padding: 12px; margin: 8px 0; border-radius: 6px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.2); border-radius: 8px 8px 0 0;
        color: white; font-weight: 600;
    }
    .stTabs [aria-selected="true"] { background-color: white !important; color: #667eea !important; }
</style>
""", unsafe_allow_html=True)

# 標題
st.markdown("# 📱 電話號碼命理分析")
st.markdown('<p class="subtitle">使用八大數字磁場 × 八十一靈動數 × 五行相容性</p>', unsafe_allow_html=True)

# 創建標籤頁
tab1, tab2 = st.tabs(["🔍 號碼分析", "✨ 號碼推薦"])

# ===== 標籤頁 1: 號碼分析 =====
with tab1:
    st.markdown("""
    <div class="info-box">
        💡 <strong>分析現有號碼</strong><br>
        輸入您的手機號碼和出生日期，立即獲得專業的命理分析報告
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        phone_number = st.text_input(
            "📞 手機號碼",
            placeholder="例: 0978-759-196",
            help="請輸入 09 開頭的台灣手機號碼",
            key="analyze_phone"
        )

    with col2:
        birthdate_analyze = st.text_input(
            "🎂 出生年月日",
            placeholder="例: 1990/09/25",
            help="格式: YYYY/MM/DD",
            key="analyze_birthdate"
        )

    if st.button("🔮 開始分析", use_container_width=True, key="analyze_btn"):
        error_msg = None
        clean_phone = re.sub(r'\D', '', phone_number)
        
        if not phone_number:
            error_msg = "請輸入手機號碼"
        elif not re.match(r'^09\d{8}$', clean_phone):
            error_msg = "手機號碼格式不正確，請輸入 09 開頭的 10 位數字"
        
        if not error_msg:
            if not birthdate_analyze:
                error_msg = "請輸入出生日期"
            elif not re.match(r'^\d{4}/\d{2}/\d{2}$', birthdate_analyze):
                error_msg = "出生日期格式不正確，請使用 YYYY/MM/DD 格式"
            else:
                try:
                    year, month, day = map(int, birthdate_analyze.split('/'))
                    if not (1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31):
                        error_msg = "出生日期數值不正確"
                except:
                    error_msg = "出生日期格式錯誤"
        
        if error_msg:
            st.error(f"❌ {error_msg}")
        else:
            formatted_phone = f"{clean_phone[:4]}-{clean_phone[4:7]}-{clean_phone[7:]}"
            
            try:
                with st.spinner('🔮 分析中...'):
                    analyzer = PhoneNumerology(birthdate_analyze)
                    report = analyzer.generate_report(formatted_phone)
                    analysis = analyzer.comprehensive_analysis(formatted_phone)
                
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                
                score = analysis['final_score']
                if score >= 80: score_color = "#4caf50"
                elif score >= 70: score_color = "#8bc34a"
                elif score >= 60: score_color = "#ffc107"
                elif score >= 50: score_color = "#ff9800"
                else: score_color = "#f44336"
                
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
                
                st.markdown("### 📄 詳細分析報告")
                st.code(report, language=None)
                
                st.download_button(
                    label="💾 下載完整報告",
                    data=report,
                    file_name=f"{clean_phone}_分析報告.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                with st.expander("📈 查看詳細數據"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("磁場評分", f"{analysis['magnetic_fields']['total_score']:.1f}", help="八大數字磁場分析得分")
                    with col2:
                        st.metric("靈動數", analysis['lingdong_81']['lingdong_number'], analysis['lingdong_81']['type'], help="八十一靈動數")
                    with col3:
                        st.metric("五行相容", analysis['five_elements']['compatibility_score'], analysis['five_elements']['birth_element'], help="五行相容性評分")
                    
                    if analysis['magnetic_fields']['field_counts']:
                        st.markdown("#### 🧲 磁場分布")
                        for field_name, count in analysis['magnetic_fields']['field_counts'].items():
                            st.write(f"**{field_name}**: {count} 次")
            
            except Exception as e:
                st.error(f"❌ 分析過程發生錯誤: {str(e)}")

# ===== 標籤頁 2: 號碼推薦 =====
with tab2:
    st.markdown("""
    <div class="info-box">
        ✨ <strong>反推算功能 - 找到最適合您的號碼!</strong><br>
        根據您的出生日期，系統會推薦最適合的電話號碼組合
    </div>
    """, unsafe_allow_html=True)

    birthdate_recommend = st.text_input(
        "🎂 請輸入您的出生年月日",
        placeholder="格式: YYYY/MM/DD (例: 1990/09/25)",
        help="系統將根據您的出生日期推薦適合的號碼組合",
        key="recommend_birthdate"
    )

    col1, col2 = st.columns(2)
    with col1:
        recommend_count = st.slider("推薦數量", min_value=5, max_value=20, value=10, step=5)
    with col2:
        st.write("")  # 佔位

    if st.button("✨ 生成推薦號碼", use_container_width=True, key="recommend_btn"):
        if not birthdate_recommend:
            st.error("❌ 請輸入出生日期")
        elif not re.match(r'^\d{4}/\d{2}/\d{2}$', birthdate_recommend):
            st.error("❌ 出生日期格式不正確，請使用 YYYY/MM/DD 格式")
        else:
            try:
                year, month, day = map(int, birthdate_recommend.split('/'))
                if not (1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31):
                    st.error("❌ 出生日期數值不正確")
                else:
                    with st.spinner('✨ 正在為您推薦最適合的號碼組合...'):
                        analyzer = PhoneNumerology(birthdate_recommend)
                        recommendations = analyzer.recommend_numbers(count=recommend_count)
                        
                        # 計算五行
                        year_index = (year - 4) % 10
                        heavenly_stems = ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己']
                        elements_map = {'庚':'金','辛':'金','壬':'水','癸':'水','甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土'}
                        birth_element = elements_map[heavenly_stems[year_index]]
                    
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="text-align: center; margin-bottom: 2rem;">
                        <h2 style="color: #667eea;">✨ 為您推薦的吉利號碼組合</h2>
                        <p style="color: #666; font-size: 1.1rem;">
                            出生日期: {birthdate_recommend} | 本命五行: <strong>{birth_element}</strong>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### 📋 推薦的數字組合")
                    st.markdown("*以下數字可用於電話號碼的任意位置*")
                    
                    # 分組顯示
                    col1, col2 = st.columns(2)
                    
                    for idx, rec in enumerate(recommendations):
                        with col1 if idx % 2 == 0 else col2:
                            st.markdown(f"""
                            <div class="recommendation-card">
                                <div style="font-size: 1.5rem; font-weight: bold; color: #667eea; margin-bottom: 4px;">
                                    {rec['pattern']}
                                </div>
                                <div style="font-size: 0.9rem; color: #666;">
                                    <strong>{rec['type']}</strong> - {rec['reason']}
                                </div>
                                <div style="font-size: 0.85rem; color: #999; margin-top: 4px;">
                                    推薦指數: {'⭐' * min(5, int(rec['score']/20))}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # 使用建議
                    st.markdown("### 💡 使用建議")
                    st.markdown("""
                    1. **完整號碼**: 可將推薦的組合放在電話號碼的任意位置
                       - 例如: `0978-**13**-196` (使用推薦組合 13)
                       - 例如: `09**68**-759-196` (使用推薦組合 68)
                    
                    2. **組合使用**: 可以組合多個推薦數字
                       - 例如: `09**13**-**68**-196` (同時使用 13 和 68)
                    
                    3. **搜尋號碼**: 使用這些組合在電信商網站搜尋可用號碼
                    
                    4. **驗證分析**: 找到心儀號碼後，可切換到「號碼分析」標籤進行完整分析
                    """)
                    
                    # 生成推薦報告
                    report_text = f"電話號碼推薦報告\n{'='*60}\n\n"
                    report_text += f"出生日期: {birthdate_recommend}\n"
                    report_text += f"本命五行: {birth_element}\n\n"
                    report_text += f"推薦的數字組合 (共 {len(recommendations)} 個):\n"
                    report_text += "="*60 + "\n\n"
                    
                    for idx, rec in enumerate(recommendations, 1):
                        report_text += f"{idx}. 數字組合: {rec['pattern']}\n"
                        report_text += f"   類型: {rec['type']}\n"
                        report_text += f"   說明: {rec['reason']}\n"
                        report_text += f"   推薦指數: {rec['score']}/100\n\n"
                    
                    report_text += "\n使用建議:\n"
                    report_text += "- 可將推薦組合放在電話號碼的任意位置\n"
                    report_text += "- 可組合多個推薦數字使用\n"
                    report_text += "- 建議在電信商網站搜尋包含這些組合的可用號碼\n"
                    
                    st.download_button(
                        label="💾 下載推薦報告",
                        data=report_text,
                        file_name=f"號碼推薦_{birthdate_recommend.replace('/', '')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"❌ 推薦過程發生錯誤: {str(e)}")

# 側邊欄資訊
with st.sidebar:
    st.markdown("### 📚 關於本系統")
    st.markdown("""
    本系統使用傳統中華命理學方法:
    
    **分析功能**:
    - 八大數字磁場
    - 八十一靈動數
    - 五行相容性
    
    **推薦功能** (新!):
    - 吉星磁場組合
    - 五行相生數字
    - 大吉靈動數
    
    ⚠️ **免責聲明**: 分析結果僅供參考娛樂。
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
    電話號碼命理分析系統 v2.0 | Powered by Streamlit
</div>
""", unsafe_allow_html=True)
