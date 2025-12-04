
from phone_numerology import PhoneNumerology
import sys

def test():
    dates = ["1990/09/25", "1995/03/15", "1985/12/08"]
    results = {}
    
    with open("verify_output_v2.txt", "w", encoding="utf-8") as f:
        for d in dates:
            try:
                analyzer = PhoneNumerology(d)
                recs = analyzer.recommend_numbers(count=5)
                patterns = [r['pattern'] for r in recs]
                results[d] = patterns
                f.write(f"Date: {d}\n")
                f.write(f"Patterns: {patterns}\n\n")
            except Exception as e:
                f.write(f"Error for {d}: {e}\n")
            
        # Check for uniqueness
        unique_results = []
        for d in dates:
            if d in results and results[d] not in unique_results:
                unique_results.append(results[d])
                
        if len(unique_results) == len(dates):
            f.write("VERIFICATION SUCCESS: All results are different.\n")
        else:
            f.write("VERIFICATION FAILED: Some results are identical.\n")

if __name__ == "__main__":
    try:
        test()
        print("Test finished. Check verify_output_v2.txt")
    except Exception as e:
        print(f"Error: {e}")
