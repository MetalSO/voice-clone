# 自动环境配置脚本
# 自动检测并安装项目所需的运行时环境和依赖

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  项目环境自动配置脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检测当前环境
Write-Host "[1/6] 检测当前环境..." -ForegroundColor Yellow

$osVersion = [System.Environment]::OSVersion.Version
$nodeVersion = node --version 2>$null
$pythonVersion = python --version 2>$null

Write-Host "  操作系统: Windows $($osVersion.Major).$($osVersion.Minor) Build $($osVersion.Build)" -ForegroundColor White
Write-Host "  Node.js: $($nodeVersion)" -ForegroundColor White
Write-Host "  Python: $($pythonVersion)" -ForegroundColor White

# 检测Java
Write-Host ""
Write-Host "[2/6] 检测Java环境..." -ForegroundColor Yellow

$javaInstalled = $false
$javaHome = $null
$javaVersion = $null

# 检查常见Java安装路径
$javaPaths = @(
    "C:\Program Files\Java",
    "C:\Program Files (x86)\Java",
    "C:\Program Files\Android\jdk",
    "${env:JAVA_HOME}",
    "${env:JDK_HOME}"
)

foreach ($path in $javaPaths) {
    if ($path -and (Test-Path $path)) {
        $jdkPath = Get-ChildItem -Path $path -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "*jdk*" } | Select-Object -First 1
        if ($jdkPath) {
            $javaHome = $jdkPath.FullName
            $javaExe = Join-Path $javaHome "bin\java.exe"
            if (Test-Path $javaExe) {
                $javaVersion = & $javaExe -version 2>&1 | Select-Object -First 1
                $javaInstalled = $true
                break
            }
        }
    }
}

if ($javaInstalled) {
    Write-Host "  Java已安装: $javaHome" -ForegroundColor Green
    Write-Host "  版本: $javaVersion" -ForegroundColor White
    $env:JAVA_HOME = $javaHome
    $env:PATH = "$javaHome\bin;$env:PATH"
} else {
    Write-Host "  Java未安装或未找到" -ForegroundColor Red
}

# 检测Maven
Write-Host ""
Write-Host "[3/6] 检测Maven..." -ForegroundColor Yellow

$mavenInstalled = $false
$mvnVersion = mvn --version 2>$null
if ($LASTEXITCODE -eq 0 -and $mvnVersion) {
    $mavenInstalled = $true
    Write-Host "  Maven已安装" -ForegroundColor Green
    Write-Host "  版本: $mvnVersion" -ForegroundColor White
} else {
    Write-Host "  Maven未安装" -ForegroundColor Red
}

# 安装Maven
if (-not $mavenInstalled) {
    Write-Host ""
    Write-Host "[4/6] 安装Maven..." -ForegroundColor Yellow

    $mavenUrl = "https://dlcdn.apache.org/maven/maven-3/3.9.9/binaries/apache-maven-3.9.9-bin.zip"
    $mavenZip = Join-Path $env:TEMP "apache-maven.zip"
    $mavenDest = "C:\maven"

    Write-Host "  下载Maven..." -ForegroundColor White
    try {
        Invoke-WebRequest -Uri $mavenUrl -OutFile $mavenZip -UseBasicParsing -TimeoutSec 120
        Write-Host "  解压Maven..." -ForegroundColor White
        Expand-Archive -Path $mavenZip -DestinationPath $mavenDest -Force
        $env:PATH = "C:\maven\apache-maven-3.9.9\bin;$env:PATH"
        $env:MAVEN_HOME = "C:\maven\apache-maven-3.9.9"
        Write-Host "  Maven安装成功!" -ForegroundColor Green
        Remove-Item $mavenZip -Force
        $mavenInstalled = $true
    } catch {
        Write-Host "  Maven安装失败: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 验证Java和Maven
Write-Host ""
Write-Host "[5/6] 验证环境..." -ForegroundColor Yellow

if ($javaInstalled) {
    $javaCheck = & java -version 2>&1 | Select-Object -First 1
    Write-Host "  Java: $javaCheck" -ForegroundColor Green
}

if ($mavenInstalled) {
    $mavenCheck = mvn --version 2>&1 | Select-Object -First 1
    Write-Host "  Maven: $mavenCheck" -ForegroundColor Green
}

# 生成配置报告
Write-Host ""
Write-Host "[6/6] 生成配置报告..." -ForegroundColor Yellow

$report = @"
========================================
  环境配置报告
========================================

操作系统: Windows $($osVersion.Major).$($osVersion.Minor) Build $($osVersion.Build)
Node.js: $($nodeVersion)
Python: $($pythonVersion)
Java: $(if($javaInstalled) { $javaHome } else { '未安装' })
Maven: $(if($mavenInstalled) { '已安装' } else { '未安装' })

环境变量:
  JAVA_HOME = $env:JAVA_HOME
  MAVEN_HOME = $env:MAVEN_HOME
  PATH = $($env:PATH.Substring(0, [Math]::Min(100, $env:PATH.Length)))...

========================================
"@

Write-Host $report -ForegroundColor Cyan

# 保存报告
$reportPath = Join-Path $PSScriptRoot "environment-report.txt"
$report | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host ""
Write-Host "配置报告已保存到: $reportPath" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  环境配置完成!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 返回状态
return @{
    JavaInstalled = $javaInstalled
    MavenInstalled = $mavenInstalled
    JavaHome = $javaHome
}
