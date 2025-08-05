Configure Claude Context Sync Extended with full data synchronization.

```bash
if [ -z "$1" ]; then
    echo "Usage: /sync-full-setup <github-repo-url> [essential|full]"
    echo "Sync levels:"
    echo "  essential - CLAUDE.md, settings, sessions, MCP configs"
    echo "  full      - Everything including shell snapshots, slash commands"
    exit 1
fi

LEVEL="${2:-essential}"
python3 ~/claude-sync-extended.py setup --git-repo "$1" --level "$LEVEL"
echo "? Extended sync configured!"
echo "?? Run /sync-status to see what will be synced"
```
