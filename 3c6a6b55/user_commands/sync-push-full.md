Push ALL Claude data to remote repository for other PCs to access.

```bash
cd ~
echo "Pushing full Claude data to remote..."
python ~/claude-sync-extended-ascii.py push
echo "All data pushed to remote!"
echo "Other PCs can now pull your sessions, settings, and configurations"
```