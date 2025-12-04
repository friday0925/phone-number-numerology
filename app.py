"""
Flask 後端 API 服務
提供電話號碼命理分析的 REST API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from phone_numerology import PhoneNumerology
import re

app = Flask(__name__)
CORS(app)  # 允許跨域請求

@app.route('/')
def index():
    """首頁 - 返回 API 資訊"""
    return jsonify({
        'name': '電話號碼命理分析 API',
        'version': '1.0.0',
        'endpoints': {
            'POST /analyze': '分析電話號碼',
            'GET /health': '健康檢查'
        }
    })

@app.route('/health')
def health():
    """健康檢查端點"""
    return jsonify({'status': 'healthy'})

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    分析電話號碼
    
    Request Body:
    {
        "phone_number": "0978-759-196",
        "birthdate": "1990/09/25"
    }
    
    Response:
    {
        "report": "分析報告內容...",
        "score": 85.5,
        "recommendation": "★★★★☆ 非常適合"
    }
    """
    try:
        # 獲取請求數據
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '請提供 JSON 數據'}), 400
        
        phone_number = data.get('phone_number', '').strip()
        birthdate = data.get('birthdate', '').strip()
        
        # 驗證輸入
        if not phone_number or not birthdate:
            return jsonify({'error': '請提供手機號碼和出生日期'}), 400
        
        # 驗證手機號碼格式
        phone_clean = re.sub(r'\D', '', phone_number)
        if not re.match(r'^09\d{8}$', phone_clean):
            return jsonify({'error': '手機號碼格式不正確，請輸入 09 開頭的 10 位數字'}), 400
        
        # 驗證出生日期格式
        if not re.match(r'^\d{4}/\d{2}/\d{2}$', birthdate):
            return jsonify({'error': '出生日期格式不正確，請使用 YYYY/MM/DD 格式'}), 400
        
        # 驗證日期數值
        try:
            year, month, day = map(int, birthdate.split('/'))
            if not (1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31):
                raise ValueError
        except:
            return jsonify({'error': '出生日期數值不正確'}), 400
        
        # 格式化手機號碼
        if len(phone_clean) == 10:
            formatted_phone = f"{phone_clean[:4]}-{phone_clean[4:7]}-{phone_clean[7:]}"
        else:
            formatted_phone = phone_number
        
        # 執行分析
        analyzer = PhoneNumerology(birthdate)
        report = analyzer.generate_report(formatted_phone)
        analysis = analyzer.comprehensive_analysis(formatted_phone)
        
        # 返回結果
        return jsonify({
            'success': True,
            'phone_number': formatted_phone,
            'birthdate': birthdate,
            'report': report,
            'score': analysis['final_score'],
            'recommendation': analysis['recommendation'],
            'details': {
                'magnetic_fields': analysis['magnetic_fields']['field_counts'],
                'lingdong_81': {
                    'number': analysis['lingdong_81']['lingdong_number'],
                    'type': analysis['lingdong_81']['type'],
                    'meaning': analysis['lingdong_81']['meaning']
                },
                'five_elements': {
                    'birth_element': analysis['five_elements']['birth_element'],
                    'compatibility_score': analysis['five_elements']['compatibility_score']
                }
            }
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'分析過程發生錯誤: {str(e)}'}), 500

if __name__ == '__main__':
    print("="*60)
    print("電話號碼命理分析 API 服務")
    print("="*60)
    print("伺服器啟動於: http://localhost:5000")
    print("API 端點: http://localhost:5000/analyze")
    print("請在瀏覽器中開啟 index.html 使用網頁介面")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
