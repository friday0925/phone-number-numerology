"""
分析已找到的電話號碼
讀取 found_numbers.txt 並進行命理分析
"""

from phone_numerology import PhoneNumerology
import os
import sys
import argparse
from pathlib import Path
import re


def get_desktop_path():
    """獲取桌面路徑"""
    return str(Path.home() / "Desktop")


def sanitize_filename(phone_number: str) -> str:
    """將電話號碼轉換為合法的檔案名稱"""
    # 移除所有非數字和連字號的字符
    sanitized = re.sub(r'[^0-9-]', '', phone_number)
    return sanitized


def analyze_found_numbers(birthdate: str = "1985/11/11", phone_number: str = None):
    """
    分析已找到的電話號碼
    
    Args:
        birthdate: 出生日期 (格式: YYYY/MM/DD)
        phone_number: 指定的電話號碼 (可選,如果提供則只分析此號碼)
    """
    # 創建分析器
    analyzer = PhoneNumerology(birthdate)
    
    # 如果指定了電話號碼,只分析該號碼
    if phone_number:
        print(f"📊 分析指定的電話號碼: {phone_number}\n")
        report_content = analyzer.generate_report(phone_number)
        print(report_content)
        
        # 儲存報告到桌面,以電話號碼命名
        desktop_path = get_desktop_path()
        filename = f"{sanitize_filename(phone_number)}.txt"
        report_file = os.path.join(desktop_path, filename)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\n✅ 報告已儲存至桌面: {filename}")
        print(f"   完整路徑: {report_file}")
        return
    
    # 讀取找到的號碼
    numbers_file = "found_numbers.txt"
    
    if not os.path.exists(numbers_file):
        print(f"❌ 找不到檔案: {numbers_file}")
        print("請先執行 cht_crawler.py 來搜尋電話號碼,或使用 --phone 參數指定號碼")
        return
    
    with open(numbers_file, 'r', encoding='utf-8') as f:
        numbers = [line.strip() for line in f if line.strip()]
    
    if not numbers:
        print("❌ 沒有找到任何電話號碼")
        return
    
    print(f"📊 找到 {len(numbers)} 個符合條件的電話號碼\n")
    print("開始進行命理分析...\n")
    
    # 分析所有號碼
    results = []
    for number in numbers:
        # 格式化號碼(加上連字號)
        if len(number) == 10:
            formatted = f"{number[:4]}-{number[4:7]}-{number[7:]}"
        else:
            formatted = number
        
        analysis = analyzer.comprehensive_analysis(formatted)
        results.append(analysis)
    
    # 按照綜合評分排序
    results.sort(key=lambda x: x['final_score'], reverse=True)
    
    # 生成排名報告
    print("="*70)
    print("電話號碼排名(依綜合評分)")
    print("="*70)
    print(f"{'排名':<6} {'號碼':<15} {'綜合評分':<12} {'推薦度':<20}")
    print("-"*70)
    
    for i, result in enumerate(results, 1):
        print(f"{i:<6} {result['phone_number']:<15} {result['final_score']:<12.2f} {result['recommendation']}")
    
    print("="*70)
    print()
    
    # 顯示前3名的詳細分析
    top_n = min(3, len(results))
    print(f"\n{'='*70}")
    print(f"前 {top_n} 名詳細分析")
    print(f"{'='*70}\n")
    
    for i in range(top_n):
        print(f"\n{'#'*70}")
        print(f"第 {i+1} 名")
        print(f"{'#'*70}")
        print(analyzer.generate_report(results[i]['phone_number']))
    
    # 儲存完整報告到桌面
    desktop_path = get_desktop_path()
    
    # 為每個號碼生成獨立的報告檔案
    saved_files = []
    for i, result in enumerate(results, 1):
        phone_num = result['phone_number']
        filename = f"{sanitize_filename(phone_num)}_分析報告.txt"
        report_file = os.path.join(desktop_path, filename)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write(f"電話號碼命理分析報告 - 排名第 {i} 名\n")
            f.write(f"出生日期: {birthdate}\n")
            f.write("="*70 + "\n\n")
            f.write(analyzer.generate_report(phone_num))
            f.write("\n\n")
            f.write("="*70 + "\n")
            f.write(f"綜合評分: {result['final_score']}/100\n")
            f.write(f"推薦度: {result['recommendation']}\n")
            f.write(f"排名: 第 {i} 名 (共 {len(results)} 個號碼)\n")
            f.write("="*70 + "\n")
        
        saved_files.append(filename)
    
    # 同時生成一個總覽報告
    summary_filename = f"電話號碼分析總覽_{len(results)}個號碼.txt"
    summary_file = os.path.join(desktop_path, summary_filename)
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("電話號碼命理分析完整報告\n")
        f.write(f"出生日期: {birthdate}\n")
        f.write(f"分析數量: {len(results)} 個號碼\n")
        f.write("="*70 + "\n\n")
        
        f.write("排名總覽\n")
        f.write("-"*70 + "\n")
        f.write(f"{'排名':<6} {'號碼':<15} {'綜合評分':<12} {'推薦度':<20}\n")
        f.write("-"*70 + "\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"{i:<6} {result['phone_number']:<15} {result['final_score']:<12.2f} {result['recommendation']}\n")
        
        f.write("\n\n")
        f.write("="*70 + "\n")
        f.write("詳細分析\n")
        f.write("="*70 + "\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"\n{'#'*70}\n")
            f.write(f"第 {i} 名\n")
            f.write(f"{'#'*70}\n")
            f.write(analyzer.generate_report(result['phone_number']))
            f.write("\n\n")
    
    print(f"\n✅ 分析報告已儲存至桌面:")
    print(f"   📄 總覽報告: {summary_filename}")
    print(f"   📱 個別報告: {len(saved_files)} 個檔案")
    for filename in saved_files:
        print(f"      - {filename}")
    print(f"\n   完整路徑: {desktop_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='電話號碼命理分析系統',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用範例:
  # 使用預設出生日期分析 found_numbers.txt 中的所有號碼
  python analyze_results.py
  
  # 指定出生日期分析所有號碼
  python analyze_results.py --birthdate 1990/09/25
  
  # 分析指定的電話號碼
  python analyze_results.py --phone 0978-759-196
  
  # 指定出生日期和電話號碼
  python analyze_results.py --birthdate 1990/09/25 --phone 0978-759-196
        '''
    )
    
    parser.add_argument(
        '--birthdate', '-b',
        type=str,
        default='1963/08/20',
        help='出生日期 (格式: YYYY/MM/DD, 預設: 1989/01/25)'
    )
    
    parser.add_argument(
        '--phone', '-p',
        type=str,
        default=None,
        help='要分析的電話號碼 (可選,如果不提供則分析 found_numbers.txt 中的所有號碼)'
    )
    
    args = parser.parse_args()
    
    # 驗證出生日期格式
    try:
        parts = args.birthdate.split('/')
        if len(parts) != 3:
            raise ValueError
        year, month, day = map(int, parts)
        if not (1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31):
            raise ValueError
    except:
        print(f"❌ 錯誤: 出生日期格式不正確,請使用 YYYY/MM/DD 格式 (例如: 1990/09/25)")
        sys.exit(1)
    
    # 執行分析
    analyze_found_numbers(birthdate=args.birthdate, phone_number=args.phone)

