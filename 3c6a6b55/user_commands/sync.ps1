param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("sync-pull", "sync-push", "sync-pull-full", "sync-push-full", "sync-full", "sync-status")]
    [string]$Command = "sync-status"
)

Set-Location "C:\Users\cg14849\.claude\commands"

switch ($Command) {
    "sync-pull" {
        Write-Host "Running sync-pull..."
        & python claude-sync-extended.py setup --git-repo https://github.com/davide-f98/claude-sync --level essential
        & python claude-sync-extended.py pull
    }
    "sync-push" {
        Write-Host "Running sync-push..."
        & python claude-sync-extended.py setup --git-repo https://github.com/davide-f98/claude-sync --level essential
        # Use sync to handle remote changes automatically
        & python claude-sync-extended.py sync
    }
    "sync-pull-full" {
        Write-Host "Running sync-pull-full..."
        & python claude-sync-extended.py setup --git-repo https://github.com/davide-f98/claude-sync --level full
        & python claude-sync-extended.py pull
    }
    "sync-push-full" {
        Write-Host "Running sync-push-full..."
        & python claude-sync-extended.py setup --git-repo https://github.com/davide-f98/claude-sync --level full
        # Use sync instead of push to handle remote changes automatically
        & python claude-sync-extended.py sync
    }
    "sync-full" {
        Write-Host "Running sync-full..."
        & python claude-sync-extended.py setup --git-repo https://github.com/davide-f98/claude-sync --level full
        & python claude-sync-extended.py sync
    }
    "sync-status" {
        Write-Host "Running sync-status..."
        & python claude-sync-extended.py status
    }
}