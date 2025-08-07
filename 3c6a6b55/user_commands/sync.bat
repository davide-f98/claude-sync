@echo off
REM Sync scripts launcher for Windows
if "%1"=="sync-pull" (
    powershell -ExecutionPolicy Bypass -File "%~dp0sync.ps1" sync-pull
    goto :eof
)
if "%1"=="sync-push" (
    powershell -ExecutionPolicy Bypass -File "%~dp0sync.ps1" sync-push
    goto :eof
)
if "%1"=="sync-pull-full" (
    powershell -ExecutionPolicy Bypass -File "%~dp0sync.ps1" sync-pull-full
    goto :eof
)
if "%1"=="sync-push-full" (
    powershell -ExecutionPolicy Bypass -File "%~dp0sync.ps1" sync-push-full
    goto :eof
)
if "%1"=="sync-full" (
    powershell -ExecutionPolicy Bypass -File "%~dp0sync.ps1" sync-full
    goto :eof
)
if "%1"=="sync-status" (
    powershell -ExecutionPolicy Bypass -File "%~dp0sync.ps1" sync-status
    goto :eof
)
echo Usage: %0 [sync-pull|sync-push|sync-pull-full|sync-push-full|sync-full|sync-status]
echo.
echo Essential sync:
echo   sync-pull          - Pull context and basic settings
echo   sync-push          - Push context and basic settings
echo.
echo Extended sync:
echo   sync-pull-full     - Pull ALL Claude data (sessions, MCP, etc.)
echo   sync-push-full     - Push ALL Claude data
echo   sync-full          - Complete bidirectional sync
echo   sync-status        - Show detailed sync status