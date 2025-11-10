# PowerShell Test Script for Vanna AI API
# Usage: .\test-vanna-api.ps1

Write-Host "🚀 Testing Vanna AI API..." -ForegroundColor Green

# Test 1: Health Check
Write-Host "`n📊 Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
    Write-Host "✅ Health Status:" -ForegroundColor Green
    $healthResponse | ConvertTo-Json -Depth 3
}
catch {
    Write-Host "❌ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 2: Root Endpoint
Write-Host "`n🏠 Testing Root Endpoint..." -ForegroundColor Yellow
try {
    $rootResponse = Invoke-RestMethod -Uri "http://localhost:8000/" -Method GET
    Write-Host "✅ Root Response:" -ForegroundColor Green
    $rootResponse | ConvertTo-Json -Depth 3
}
catch {
    Write-Host "❌ Root endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Chat Endpoint
Write-Host "`n💬 Testing Chat Endpoint..." -ForegroundColor Yellow
try {
    $chatBody = @{
        question = "What is the total spend?"
        context = @{}
    } | ConvertTo-Json

    $chatResponse = Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method POST -Body $chatBody -ContentType "application/json"
    Write-Host "✅ Chat Response:" -ForegroundColor Green
    $chatResponse | ConvertTo-Json -Depth 3
}
catch {
    Write-Host "❌ Chat endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Error details: $($_.Exception)" -ForegroundColor Red
}

# Test 4: More Complex Questions
$testQuestions = @(
    "Who are the top 5 vendors by spend?",
    "Show overdue invoices",
    "What is the monthly invoice trend?",
    "Show spending by category"
)

foreach ($question in $testQuestions) {
    Write-Host "`n🤔 Testing Question: '$question'" -ForegroundColor Yellow
    try {
        $questionBody = @{
            question = $question
            context = @{}
        } | ConvertTo-Json

        $questionResponse = Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method POST -Body $questionBody -ContentType "application/json"
        
        if ($questionResponse.error) {
            Write-Host "⚠️  Response with error: $($questionResponse.error)" -ForegroundColor Red
        } else {
            Write-Host "✅ SQL Generated: $($questionResponse.sql)" -ForegroundColor Green
            Write-Host "📊 Data rows returned: $($questionResponse.data.Count)" -ForegroundColor Cyan
        }
    }
    catch {
        Write-Host "❌ Question failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n🎉 API Testing Complete!" -ForegroundColor Green