#!/usr/bin/env python3
import sys
import os
sys.path.append('C:\\Users\\cg14849\\.claude\\commands')

from claude_sync_extended import ClaudeSyncExtended

# Create sync instance
sync = ClaudeSyncExtended()

# Run just the staging part
print("Testing staging process...")
staging_dir = sync.prepare_sync_data()
print(f"Staging completed in: {staging_dir}")

# List what was actually staged
import os
print("\nFiles staged:")
for root, dirs, files in os.walk(staging_dir):
    for file in files:
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(full_path, staging_dir)
        print(f"  {rel_path}")