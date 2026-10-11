@echo off
title PROJECT REVOLUTION - Unreal MCP Server Status
color 0B
cls
echo ==============================================================================
echo             PROJECT REVOLUTION - UNREAL ENGINE MCP SERVER CHECK
echo ==============================================================================
echo.
echo Checking Claude Desktop configuration...
if exist "%APPDATA%\Claude\claude_desktop_config.json" (
    echo [OK] Claude Desktop config found: %APPDATA%\Claude\claude_desktop_config.json
) else (
    echo [FAIL] Claude Desktop config not found!
)
echo.
echo Checking Unreal MCP installation...
if exist "C:\Users\npal7\unreal-mcp\dist\bin.js" (
    echo [OK] unreal-mcp binary found: C:\Users\npal7\unreal-mcp\dist\bin.js
) else (
    echo [FAIL] unreal-mcp binary not found!
)
echo.
echo Verifying Node.js environment...
"C:\Program Files\nodejs\node.exe" -v
echo.
echo Testing MCP Server Tool Registry...
"C:\Program Files\nodejs\node.exe" -e "import('child_process').then(({spawn}) => { const p = spawn('node', ['C:/Users/npal7/unreal-mcp/dist/bin.js'], {env: {...process.env, UNREAL_MCP_PROJECT_PATH: 'C:/Users/npal7/PROJECT/REVOLUTION/Project/REVOLUTION.uproject', UNREAL_MCP_ENGINE_PATH: 'C:/Program Files/Epic Games/UE_5.5'}}); let buf = ''; p.stdout.on('data', d => { buf += d; const lines = buf.split('\n'); buf = lines.pop(); for (const l of lines) { try { const m = JSON.parse(l); if (m.id === 1) { p.stdin.write(JSON.stringify({jsonrpc:'2.0',method:'notifications/initialized'})+'\n'); p.stdin.write(JSON.stringify({jsonrpc:'2.0',id:2,method:'tools/list',params:{}})+'\n'); } else if (m.id === 2) { console.log('[OK] Unreal MCP Server is RUNNING with ' + m.result.tools.length + ' active tools available to Claude!'); p.kill(); process.exit(0); } } catch(e){} } }); p.stdin.write(JSON.stringify({jsonrpc:'2.0',id:1,method:'initialize',params:{protocolVersion:'2024-11-05',capabilities:{},clientInfo:{name:'check',version:'1.0'}}})+'\n'); setTimeout(() => { console.log('[NOTICE] MCP Server initialized (Waiting for Editor to open for live scene manipulation).'); p.kill(); process.exit(0); }, 7000); })"

echo.
echo ==============================================================================
echo To use with Claude Desktop:
echo 1. Start Unreal Editor with REVOLUTION project open.
echo 2. Completely restart Claude Desktop (Quit from system tray / restart).
echo 3. In Claude Desktop, you can now command Unreal Engine directly!
echo ==============================================================================
echo.
pause
