@echo off
chcp 65001 >nul
title Pocket-TTS SSL 修复工具

echo ========================================
echo   Pocket-TTS SSL 证书修复工具
echo ========================================
echo.

cd /d "d:\trea speech synthesis"

echo [1/3] 检查 Python 环境...
"d:\trea speech synthesis\venv\Scripts\python.exe" --version
echo.

echo [2/3] 修复 SSL 证书问题...
echo.

REM 方法1: 更新 certifi 证书
echo 正在更新 certifi 证书库...
"d:\trea speech synthesis\venv\Scripts\python.exe" -m pip install --upgrade certifi --quiet

REM 方法2: 设置环境变量
echo 设置 HuggingFace SSL 验证环境变量...
set HF_HTTPS_VERIFY=0

REM 方法3: 尝试运行修复脚本
echo.
echo [3/3] 运行 SSL 修复...
"d:\trea speech synthesis\venv\Scripts\python.exe" -c "
import ssl
import certifi
import os

print('当前证书路径:', certifi.where())

# 尝试更新证书
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# 测试连接
import httpx
try:
    response = httpx.get('https://huggingface.co', timeout=10, verify=certifi.where())
    print('HuggingFace 连接测试: 成功')
except Exception as e:
    print('HuggingFace 连接测试: 失败')
    print('错误:', str(e)[:100])
"

echo.
echo 修复完成！现在可以尝试运行后端服务。
echo 注意: 如果问题仍然存在，可能需要配置代理或使用 VPN。
echo.

pause
