"""
電話號碼命理分析系統
使用八大數字磁場和八十一靈動數來分析電話號碼的吉凶
"""

from datetime import datetime
from typing import Dict, List, Tuple
import re


class PhoneNumerology:
    """電話號碼命理分析類"""
    
    # 八大數字磁場定義
    MAGNETIC_FIELDS = {
        '天醫': {
            'pairs': ['13', '31', '68', '86', '49', '94', '27', '72'],
            'meaning': '財富、智慧、正桃花、婚姻',
            'score': 10,
            'type': 'lucky'
        },
        '生氣': {
            'pairs': ['14', '41', '67', '76', '93', '39', '82', '28'],
            'meaning': '貴人、樂天、人際關係',
            'score': 9,
            'type': 'lucky'
        },
        '延年': {
            'pairs': ['19', '91', '87', '78', '34', '43', '26', '62'],
            'meaning': '事業、專業能力、領導力',
            'score': 9,
            'type': 'lucky'
        },
        '伏位': {
            'pairs': ['11', '22', '33', '44', '55', '66', '77', '88', '99'],
            'meaning': '等待、蓄勢待發',
            'score': 5,
            'type': 'neutral'
        },
        '絕命': {
            'pairs': ['12', '21', '69', '96', '48', '84', '37', '73'],
            'meaning': '投資、冒險、壓力',
            'score': -8,
            'type': 'unlucky'
        },
        '禍害': {
            'pairs': ['17', '71', '89', '98', '46', '64', '32', '23'],
            'meaning': '口舌是非、小人',
            'score': -7,
            'type': 'unlucky'
        },
        '五鬼': {
            'pairs': ['18', '81', '97', '79', '36', '63', '24', '42'],
            'meaning': '聰明、機智但易有意外',
            'score': -6,
            'type': 'unlucky'
        },
        '六煞': {
            'pairs': ['16', '61', '74', '47', '38', '83', '29', '92'],
            'meaning': '桃花、感情波折',
            'score': -5,
            'type': 'unlucky'
        }
    }
    
    # 八十一靈動數吉凶對照表
    LINGDONG_81 = {
        1: {'type': '大吉', 'meaning': '宇宙起源,天地開泰', 'score': 10},
        2: {'type': '凶', 'meaning': '混飩未定,分離破敗', 'score': -5},
        3: {'type': '大吉', 'meaning': '進取如意,增進繁榮', 'score': 10},
        4: {'type': '凶', 'meaning': '破敗凶變,萬事休止', 'score': -8},
        5: {'type': '大吉', 'meaning': '福祿長壽,福德集門', 'score': 10},
        6: {'type': '吉', 'meaning': '安穩餘慶,吉人天相', 'score': 8},
        7: {'type': '吉', 'meaning': '剛毅果斷,勇往直前', 'score': 8},
        8: {'type': '吉', 'meaning': '意志剛健,勤勉發展', 'score': 8},
        9: {'type': '凶', 'meaning': '興盡凶始,窮乏困苦', 'score': -8},
        10: {'type': '凶', 'meaning': '萬事終局,充滿損耗', 'score': -8},
        11: {'type': '大吉', 'meaning': '穩健吉慶,富貴榮達', 'score': 10},
        12: {'type': '凶', 'meaning': '意志薄弱,家庭寂寞', 'score': -5},
        13: {'type': '大吉', 'meaning': '智略超群,博學多才', 'score': 10},
        14: {'type': '凶', 'meaning': '淪落天涯,失意煩悶', 'score': -5},
        15: {'type': '大吉', 'meaning': '福壽雙全,立身興家', 'score': 10},
        16: {'type': '大吉', 'meaning': '貴人相助,興家興業', 'score': 10},
        17: {'type': '吉', 'meaning': '突破萬難,剛柔兼備', 'score': 8},
        18: {'type': '吉', 'meaning': '有志竟成,內名有運', 'score': 8},
        19: {'type': '凶', 'meaning': '風雲蔽月,災苦重來', 'score': -7},
        20: {'type': '凶', 'meaning': '非業破運,災禍不安', 'score': -7},
        21: {'type': '大吉', 'meaning': '獨立權威,明月光照', 'score': 10},
        22: {'type': '凶', 'meaning': '秋草逢霜,兩士相爭', 'score': -5},
        23: {'type': '大吉', 'meaning': '旭日東升,質實剛堅', 'score': 10},
        24: {'type': '大吉', 'meaning': '家門餘慶,金錢豐盈', 'score': 10},
        25: {'type': '吉', 'meaning': '英俊剛毅,資性聰敏', 'score': 8},
        26: {'type': '凶', 'meaning': '波瀾重疊,變怪奇異', 'score': -4},
        27: {'type': '吉帶凶', 'meaning': '足智多謀,先苦後甜', 'score': 3},
        28: {'type': '凶', 'meaning': '家親緣薄,離群獨處', 'score': -6},
        29: {'type': '吉', 'meaning': '智謀兼備,欲望難足', 'score': 7},
        30: {'type': '吉帶凶', 'meaning': '一成一敗,絕處逢生', 'score': 3},
        31: {'type': '大吉', 'meaning': '智勇得志,心想事成', 'score': 10},
        32: {'type': '大吉', 'meaning': '權貴顯達,意外惠澤', 'score': 10},
        33: {'type': '大吉', 'meaning': '家門隆昌,才德開展', 'score': 10},
        34: {'type': '凶', 'meaning': '破家亡身,財命危險', 'score': -8},
        35: {'type': '吉', 'meaning': '溫和平靜,智達通暢', 'score': 8},
        36: {'type': '凶', 'meaning': '風浪不息,俠義薄運', 'score': -5},
        37: {'type': '吉', 'meaning': '權威顯達,吉人天相', 'score': 8},
        38: {'type': '吉', 'meaning': '磨鐵成針,刻意經營', 'score': 7},
        39: {'type': '大吉', 'meaning': '富貴榮華,變化無窮', 'score': 10},
        40: {'type': '吉帶凶', 'meaning': '謹慎保安,豪膽邁進', 'score': 3},
        41: {'type': '大吉', 'meaning': '德高望重,事事如意', 'score': 10},
        42: {'type': '吉帶凶', 'meaning': '寒嬋在柳,十藝不成', 'score': 2},
        43: {'type': '凶帶吉', 'meaning': '邪途散財,外祥內苦', 'score': -2},
        44: {'type': '凶', 'meaning': '須眉難展,力量有限', 'score': -6},
        45: {'type': '大吉', 'meaning': '順風揚帆,萬事如意', 'score': 10},
        46: {'type': '凶', 'meaning': '羅網繫身,離祖成家', 'score': -5},
        47: {'type': '大吉', 'meaning': '點鐵成金,開花結果', 'score': 10},
        48: {'type': '吉', 'meaning': '智謀兼備,德量榮達', 'score': 8},
        49: {'type': '吉帶凶', 'meaning': '吉凶難分,不斷辛勞', 'score': 2},
        50: {'type': '吉帶凶', 'meaning': '小舟入海,吉凶參半', 'score': 2},
        51: {'type': '吉帶凶', 'meaning': '一盛一衰,浮沉不定', 'score': 2},
        52: {'type': '吉', 'meaning': '草木逢春,雨過天晴', 'score': 7},
        53: {'type': '吉帶凶', 'meaning': '外祥內患,先吉後凶', 'score': 1},
        54: {'type': '凶', 'meaning': '雖傾全力,難望成功', 'score': -6},
        55: {'type': '吉帶凶', 'meaning': '外美內苦,假面繁榮', 'score': 1},
        56: {'type': '凶', 'meaning': '缺乏實行,難望成功', 'score': -5},
        57: {'type': '吉', 'meaning': '寒雪青松,晚年昌隆', 'score': 7},
        58: {'type': '吉帶凶', 'meaning': '先苦後甘,浮沉多端', 'score': 2},
        59: {'type': '凶', 'meaning': '遇事猶疑,難望成功', 'score': -6},
        60: {'type': '凶', 'meaning': '黑暗無光,心迷意亂', 'score': -7},
        61: {'type': '吉', 'meaning': '名利雙收,繁榮富貴', 'score': 8},
        62: {'type': '凶', 'meaning': '基礎虛弱,搖搖欲墜', 'score': -6},
        63: {'type': '吉', 'meaning': '萬物化育,繁榮之象', 'score': 8},
        64: {'type': '凶', 'meaning': '骨肉分離,孤兒悲愁', 'score': -7},
        65: {'type': '大吉', 'meaning': '吉運自來,能享盛名', 'score': 10},
        66: {'type': '凶', 'meaning': '內外不和,信用缺乏', 'score': -5},
        67: {'type': '大吉', 'meaning': '富貴長壽,光明正大', 'score': 10},
        68: {'type': '吉', 'meaning': '思慮周詳,計劃力行', 'score': 8},
        69: {'type': '凶', 'meaning': '動搖不安,常陷逆境', 'score': -6},
        70: {'type': '凶', 'meaning': '慘淡經營,難免貧困', 'score': -7},
        71: {'type': '吉帶凶', 'meaning': '吉凶參半,惟賴勇氣', 'score': 2},
        72: {'type': '吉帶凶', 'meaning': '先甘後苦,不能持久', 'score': 1},
        73: {'type': '吉帶凶', 'meaning': '盛衰交加,可守成功', 'score': 2},
        74: {'type': '凶', 'meaning': '智能不足,坐食山空', 'score': -6},
        75: {'type': '吉帶凶', 'meaning': '先吉後凶,退守可安', 'score': 1},
        76: {'type': '凶帶吉', 'meaning': '傾覆離散,骨肉分離', 'score': -3},
        77: {'type': '吉帶凶', 'meaning': '先苦後甘,不可倉促', 'score': 2},
        78: {'type': '吉帶凶', 'meaning': '有得有失,華而不實', 'score': 1},
        79: {'type': '凶', 'meaning': '挽回乏力,身疲力盡', 'score': -7},
        80: {'type': '凶', 'meaning': '凶星入度,清本縮小', 'score': -7},
        81: {'type': '大吉', 'meaning': '萬物回春,還原復始', 'score': 10}
    }
    
    def __init__(self, birthdate: str = "1990/09/25"):
        """
        初始化分析器
        
        Args:
            birthdate: 出生日期，格式為 YYYY/MM/DD
        """
        self.birthdate = birthdate
        self.birth_year, self.birth_month, self.birth_day = map(int, birthdate.split('/'))
    
    def analyze_magnetic_fields(self, phone_number: str) -> Dict:
        """
        分析電話號碼的八大數字磁場
        
        Args:
            phone_number: 電話號碼（只包含數字）
            
        Returns:
            包含磁場分析結果的字典
        """
        # 移除所有非數字字符
        clean_number = re.sub(r'\D', '', phone_number)
        
        # 提取所有連續的兩位數組合
        pairs = [clean_number[i:i+2] for i in range(len(clean_number)-1)]
        
        # 分析每個組合
        field_counts = {}
        field_details = []
        total_score = 0
        
        for pair in pairs:
            for field_name, field_info in self.MAGNETIC_FIELDS.items():
                if pair in field_info['pairs']:
                    if field_name not in field_counts:
                        field_counts[field_name] = 0
                    field_counts[field_name] += 1
                    field_details.append({
                        'pair': pair,
                        'field': field_name,
                        'meaning': field_info['meaning'],
                        'type': field_info['type'],
                        'score': field_info['score']
                    })
                    total_score += field_info['score']
                    break
        
        return {
            'pairs': pairs,
            'field_counts': field_counts,
            'field_details': field_details,
            'total_score': total_score,
            'average_score': total_score / len(pairs) if pairs else 0
        }
    
    def calculate_lingdong_81(self, phone_number: str, use_last_n: int = 4) -> Dict:
        """
        計算八十一靈動數
        
        Args:
            phone_number: 電話號碼
            use_last_n: 使用末幾位數字（4或8）
            
        Returns:
            包含靈動數分析結果的字典
        """
        # 移除所有非數字字符
        clean_number = re.sub(r'\D', '', phone_number)
        
        # 取末N位
        last_digits = clean_number[-use_last_n:]
        number_value = int(last_digits)
        
        # 計算靈動數: (number % 80) or 80
        lingdong_num = (number_value % 80) or 80
        
        # 獲取對應的吉凶資訊
        lingdong_info = self.LINGDONG_81.get(lingdong_num, {
            'type': '未知',
            'meaning': '無資料',
            'score': 0
        })
        
        return {
            'last_digits': last_digits,
            'number_value': number_value,
            'lingdong_number': lingdong_num,
            'type': lingdong_info['type'],
            'meaning': lingdong_info['meaning'],
            'score': lingdong_info['score']
        }
    
    def calculate_five_elements_compatibility(self, phone_number: str) -> Dict:
        """
        計算五行相容性（簡化版）
        基於出生年份的天干地支和號碼數字的五行屬性
        
        Args:
            phone_number: 電話號碼
            
        Returns:
            包含五行相容性分析的字典
        """
        # 天干地支對應五行
        heavenly_stems = ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己']
        elements_map = {
            '庚': '金', '辛': '金',
            '壬': '水', '癸': '水',
            '甲': '木', '乙': '木',
            '丙': '火', '丁': '火',
            '戊': '土', '己': '土'
        }
        
        # 計算出生年的天干
        year_index = (self.birth_year - 4) % 10
        birth_stem = heavenly_stems[year_index]
        birth_element = elements_map[birth_stem]
        
        # 數字對應五行（簡化版）
        digit_elements = {
            '1': '木', '2': '木',
            '3': '火', '4': '火',
            '5': '土', '6': '土',
            '7': '金', '8': '金',
            '9': '水', '0': '水'
        }
        
        # 五行相生相剋
        element_relations = {
            '木': {'生': '火', '剋': '土', '被生': '水', '被剋': '金'},
            '火': {'生': '土', '剋': '金', '被生': '木', '被剋': '水'},
            '土': {'生': '金', '剋': '水', '被生': '火', '被剋': '木'},
            '金': {'生': '水', '剋': '木', '被生': '土', '被剋': '火'},
            '水': {'生': '木', '剋': '火', '被生': '金', '被剋': '土'}
        }
        
        # 分析號碼中的數字
        clean_number = re.sub(r'\D', '', phone_number)
        element_counts = {}
        
        for digit in clean_number:
            element = digit_elements[digit]
            element_counts[element] = element_counts.get(element, 0) + 1
        
        # 計算相容性分數
        compatibility_score = 0
        element_analysis = []
        
        for element, count in element_counts.items():
            if element == birth_element:
                # 同元素：中性
                score = 5 * count
                relation = '同'
            elif element == element_relations[birth_element]['生']:
                # 我生：消耗能量
                score = 3 * count
                relation = '我生'
            elif element == element_relations[birth_element]['被生']:
                # 生我：增強能量
                score = 8 * count
                relation = '生我'
            elif element == element_relations[birth_element]['剋']:
                # 我剋：需要付出
                score = 2 * count
                relation = '我剋'
            else:  # 被剋
                # 剋我：壓力
                score = -3 * count
                relation = '剋我'
            
            compatibility_score += score
            element_analysis.append({
                'element': element,
                'count': count,
                'relation': relation,
                'score': score
            })
        
        return {
            'birth_year': self.birth_year,
            'birth_element': birth_element,
            'element_counts': element_counts,
            'element_analysis': element_analysis,
            'compatibility_score': compatibility_score
        }
    
    def comprehensive_analysis(self, phone_number: str) -> Dict:
        """
        綜合分析電話號碼
        
        Args:
            phone_number: 電話號碼
            
        Returns:
            完整的分析報告
        """
        # 執行各項分析
        magnetic_analysis = self.analyze_magnetic_fields(phone_number)
        lingdong_analysis = self.calculate_lingdong_81(phone_number)
        five_elements_analysis = self.calculate_five_elements_compatibility(phone_number)
        
        # 計算綜合評分（加權平均）
        # 40% 磁場分析, 30% 靈動數, 30% 五行相容性
        magnetic_normalized = (magnetic_analysis['average_score'] + 10) / 20 * 100  # 正規化到0-100
        lingdong_normalized = (lingdong_analysis['score'] + 10) / 20 * 100
        elements_normalized = min(100, max(0, five_elements_analysis['compatibility_score']))
        
        final_score = (
            magnetic_normalized * 0.4 +
            lingdong_normalized * 0.3 +
            elements_normalized * 0.3
        )
        
        # 生成推薦等級
        if final_score >= 80:
            recommendation = '★★★★★ 極力推薦'
        elif final_score >= 70:
            recommendation = '★★★★☆ 非常適合'
        elif final_score >= 60:
            recommendation = '★★★☆☆ 適合'
        elif final_score >= 50:
            recommendation = '★★☆☆☆ 普通'
        else:
            recommendation = '★☆☆☆☆ 不推薦'
        
        return {
            'phone_number': phone_number,
            'birthdate': self.birthdate,
            'magnetic_fields': magnetic_analysis,
            'lingdong_81': lingdong_analysis,
            'five_elements': five_elements_analysis,
            'final_score': round(final_score, 2),
            'recommendation': recommendation
        }
    
    def generate_report(self, phone_number: str) -> str:
        """
        生成易讀的分析報告
        
        Args:
            phone_number: 電話號碼
            
        Returns:
            格式化的報告文字
        """
        analysis = self.comprehensive_analysis(phone_number)
        
        report = f"""
{'='*60}
電話號碼命理分析報告
{'='*60}

📱 號碼: {analysis['phone_number']}
🎂 出生日期: {analysis['birthdate']}

{'─'*60}
【八大數字磁場分析】
{'─'*60}
"""
        
        # 磁場分析
        field_counts = analysis['magnetic_fields']['field_counts']
        if field_counts:
            for field_name, count in sorted(field_counts.items(), key=lambda x: -x[1]):
                field_info = self.MAGNETIC_FIELDS[field_name]
                report += f"  • {field_name} ({field_info['type']}): 出現 {count} 次\n"
                report += f"    意義: {field_info['meaning']}\n"
        else:
            report += "  無特殊磁場組合\n"
        
        report += f"\n  磁場評分: {analysis['magnetic_fields']['total_score']:.1f}\n"
        
        # 靈動數分析
        report += f"""
{'─'*60}
【八十一靈動數分析】
{'─'*60}
  末四碼: {analysis['lingdong_81']['last_digits']}
  靈動數: {analysis['lingdong_81']['lingdong_number']}
  吉凶: {analysis['lingdong_81']['type']}
  意義: {analysis['lingdong_81']['meaning']}
  評分: {analysis['lingdong_81']['score']}
"""
        
        # 五行分析
        report += f"""
{'─'*60}
【五行相容性分析】
{'─'*60}
  出生年份: {analysis['five_elements']['birth_year']} 年
  本命五行: {analysis['five_elements']['birth_element']}
  
  號碼五行分布:
"""
        for elem_info in analysis['five_elements']['element_analysis']:
            report += f"    {elem_info['element']}: {elem_info['count']} 個 ({elem_info['relation']}) - 得分: {elem_info['score']}\n"
        
        report += f"\n  五行相容評分: {analysis['five_elements']['compatibility_score']}\n"
        
        # 綜合評分
        report += f"""
{'='*60}
【綜合評分】
{'='*60}
  總分: {analysis['final_score']}/100
  推薦度: {analysis['recommendation']}
{'='*60}
"""
        
        return report
    
    def recommend_numbers(self, count=10):
        """
        根據出生日期推薦適合的電話號碼組合
        真正基於個人出生日期產生個性化推薦
        
        Args:
            count: 推薦的組合數量
            
        Returns:
            推薦的數字組合列表
        """
        # 計算五行
        heavenly_stems = ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己']
        elements_map = {
            '庚': '金', '辛': '金',
            '壬': '水', '癸': '水',
            '甲': '木', '乙': '木',
            '丙': '火', '丁': '火',
            '戊': '土', '己': '土'
        }
        
        year_index = (self.birth_year - 4) % 10
        birth_stem = heavenly_stems[year_index]
        birth_element = elements_map[birth_stem]
        
        # 五行對應的吉利數字 (優先順序排序)
        element_lucky_digits = {
            '金': ['7', '8', '9', '0', '4', '5'],  # 金生水,土生金,本命金
            '木': ['1', '2', '3', '4', '9', '0'],  # 木生火,水生木,本命木
            '水': ['9', '0', '1', '2', '7', '8'],  # 水生木,金生水,本命水
            '火': ['3', '4', '1', '2', '5', '6'],  # 火生土,木生火,本命火
            '土': ['5', '6', '3', '4', '9', '0']   # 土生金,火生土,本命土
        }
        
        lucky_digits = element_lucky_digits.get(birth_element, ['1', '3', '5', '7', '9'])
        
        # 根據出生月日計算個人幸運數字
        personal_lucky_digit = str((self.birth_month + self.birth_day) % 10)
        
        # 根據出生年計算次要幸運數字
        secondary_lucky_digit = str(sum(int(d) for d in str(self.birth_year)) % 10)
        
        # 吉星磁場組合 (按五行相容性排序)
        lucky_pairs = []
        for field_name in ['天醫', '生氣', '延年']:  # 只使用吉星
            field_info = self.MAGNETIC_FIELDS[field_name]
            lucky_pairs.extend(field_info['pairs'])
        
        # 根據五行篩選最適合的磁場組合
        element_compatible_pairs = []
        for pair in lucky_pairs:
            # 檢查組合中是否包含五行吉利數字
            if any(d in pair for d in lucky_digits[:3]):  # 使用前3個最吉利的數字
                element_compatible_pairs.append(pair)
        
        # 生成推薦組合
        recommendations = []
        seen = set()
        
        # 策略1: 個人專屬組合 (基於出生月日)
        personal_combos = [
            personal_lucky_digit + secondary_lucky_digit,
            secondary_lucky_digit + personal_lucky_digit,
            personal_lucky_digit + lucky_digits[0],
            lucky_digits[0] + personal_lucky_digit,
            personal_lucky_digit * 2,  # 重複數字
        ]
        
        for combo in personal_combos:
            if combo not in seen and len(combo) == 2:
                seen.add(combo)
                # 檢查是否為吉星磁場
                field_name = self._get_field_name(combo)
                if field_name in ['天醫', '生氣', '延年']:
                    reason = f'個人專屬組合 + {field_name}磁場'
                    score = 95
                else:
                    reason = f'個人專屬組合 (基於{self.birth_month}月{self.birth_day}日)'
                    score = 88
                
                recommendations.append({
                    'pattern': combo,
                    'type': '個人專屬',
                    'reason': reason,
                    'score': score
                })
        
        # 策略2: 五行相容的吉星磁場
        for pair in element_compatible_pairs[:8]:
            if pair not in seen:
                seen.add(pair)
                field_name = self._get_field_name(pair)
                recommendations.append({
                    'pattern': pair,
                    'type': '吉星磁場',
                    'reason': f'{field_name}磁場 + 適合{birth_element}命',
                    'score': 92
                })
        
        # 策略3: 五行最吉利數字組合
        for i in range(min(3, len(lucky_digits))):
            for j in range(min(3, len(lucky_digits))):
                combo = lucky_digits[i] + lucky_digits[j]
                if combo not in seen:
                    seen.add(combo)
                    field_name = self._get_field_name(combo)
                    if field_name in ['天醫', '生氣', '延年']:
                        reason = f'五行相生 + {field_name}磁場'
                        score = 90
                    else:
                        reason = f'五行相生數字 (適合{birth_element}命)'
                        score = 85
                    
                    recommendations.append({
                        'pattern': combo,
                        'type': '五行相生',
                        'reason': reason,
                        'score': score
                    })
        
        # 策略4: 基於出生年的靈動數組合
        # 使用出生年的數字來計算對應的靈動數
        year_sum = sum(int(d) for d in str(self.birth_year))
        target_lingdong = year_sum % 81
        if target_lingdong == 0:
            target_lingdong = 81
        
        # 找出接近的大吉靈動數
        lucky_lingdong = [1, 3, 5, 11, 13, 15, 16, 21, 23, 24, 31, 32, 33, 41, 45, 47, 65, 67, 81]
        closest_lingdong = min(lucky_lingdong, key=lambda x: abs(x - target_lingdong))
        
        # 生成對應的4位數組合
        for offset in [0, 80, 160, 240]:
            base = closest_lingdong + offset
            if base > 9999:
                break
            pattern = str(base).zfill(4)[-4:]
            if pattern[:2] not in seen:
                seen.add(pattern[:2])
                recommendations.append({
                    'pattern': pattern[:2],
                    'type': '靈動大吉',
                    'reason': f'對應靈動數{closest_lingdong} (基於{self.birth_year}年)',
                    'score': 87
                })
        
        # 策略5: 生日數字組合
        birth_digits = [str(self.birth_month // 10), str(self.birth_month % 10),
                       str(self.birth_day // 10), str(self.birth_day % 10)]
        birth_digits = [d for d in birth_digits if d != '0']  # 移除0
        
        if len(birth_digits) >= 2:
            for i in range(min(2, len(birth_digits))):
                for j in range(min(2, len(birth_digits))):
                    if i != j:
                        combo = birth_digits[i] + birth_digits[j]
                        if combo not in seen:
                            seen.add(combo)
                            field_name = self._get_field_name(combo)
                            if field_name in ['天醫', '生氣', '延年']:
                                reason = f'生日數字 + {field_name}磁場'
                                score = 89
                            else:
                                reason = f'生日數字組合 ({self.birth_month}/{self.birth_day})'
                                score = 82
                            
                            recommendations.append({
                                'pattern': combo,
                                'type': '生日數字',
                                'reason': reason,
                                'score': score
                            })
        
        # 按分數排序並返回指定數量
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        # 確保返回的數量足夠,如果不夠則補充其他吉星組合
        if len(recommendations) < count:
            for pair in lucky_pairs:
                if pair not in seen and len(recommendations) < count:
                    seen.add(pair)
                    field_name = self._get_field_name(pair)
                    recommendations.append({
                        'pattern': pair,
                        'type': '吉星磁場',
                        'reason': f'{field_name}磁場',
                        'score': 85
                    })
        
        return recommendations[:count]
    
    def _get_field_name(self, pair):
        """獲取數字對應的磁場名稱"""
        for field_name, field_info in self.MAGNETIC_FIELDS.items():
            if pair in field_info['pairs']:
                return field_name
        return '未知'


def main():
    """主程式示例"""
    # 創建分析器（使用預設出生日期 1990/09/25）
    analyzer = PhoneNumerology("1990/09/25")
    
    # 分析示例號碼
    test_numbers = [
        "0978-759-196",
        "0912-345-196"
    ]
    
    for number in test_numbers:
        print(analyzer.generate_report(number))
        print("\n")


if __name__ == "__main__":
    main()
