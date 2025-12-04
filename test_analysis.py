"""
快速測試分析功能 - 支援命令列參數
"""

from phone_numerology import PhoneNumerology
import sys

def main():
    # 預設值
    birthdate = "1990/09/25"
    test_number = "0978-759-196"
    
    # 檢查命令列參數
    if len(sys.argv) > 1:
        if '--help' in sys.argv or '-h' in sys.argv:
            print("""
電話號碼分析測試腳本

使用方法:
  python test_analysis.py [出生日期] [電話號碼]

參數:
  出生日期    格式: YYYY/MM/DD (可選,預設: 1990/09/25)
  電話號碼    格式: 0XXX-XXX-XXX (可選,預設: 0978-759-196)

範例:
  python test_analysis.py
  python test_analysis.py 1995/03/15
  python test_analysis.py 1995/03/15 0912-345-196
            """)
            return
        
        if len(sys.argv) >= 2:
            birthdate = sys.argv[1]
        if len(sys.argv) >= 3:
            test_number = sys.argv[2]
    
    # 創建分析器
    print("="*70)
    print("測試電話號碼分析功能")
    print("="*70)
    print(f"\n出生日期: {birthdate}")
    print(f"測試號碼: {test_number}\n")
    
    try:
        analyzer = PhoneNumerology(birthdate)
        report = analyzer.generate_report(test_number)
        print(report)
        print("\n✅ 分析功能測試成功!")
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
