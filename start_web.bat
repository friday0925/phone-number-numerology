@echo off
echo ============================================================
echo 電話號碼命理分析系統 - 網頁介面啟動
echo ============================================================
echo.

echo [1/3] 檢查 Python 環境...
python --version
if errorlevel 1 (
    echo 錯誤: 找不到 Python，請先安裝 Python 3.x
    pause
    exit /b 1
)
echo.

echo [2/3] 安裝必要套件...
pip install flask flask-cors
if errorlevel 1 (
    echo 警告: 套件安裝可能失敗，但仍嘗試啟動服務
)
echo.

echo [3/3] 啟動 Flask 服務...
echo.
echo ============================================================
echo 服務啟動後，請在瀏覽器中開啟:
echo   - 方法 1: 直接雙擊 index.html
echo   - 方法 2: 訪問 http://localhost:5000
echo.
echo 按 Ctrl+C 可停止服務
echo ============================================================
echo.

python app.py

pause
