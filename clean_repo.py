import git_filter_repo
import re
from pathlib import Path

def clean_token(blob):
    # Pattern to match the GitHub token
    pattern = r'github_pat_[A-Za-z0-9_-]{59}'
    
    # Replace token with placeholder in settings.json
    if blob.path == b'.github/agents/settings.json':
        content = blob.data.decode('utf-8')
        new_content = re.sub(pattern, '${GITHUB_TOKEN}', content)
        blob.data = new_content.encode('utf-8')

args = git_filter_repo.FilteringOptions.default_options()
args.force = True

git_filter_repo.RepoFilter(
    args,
    filename_callback=lambda x: x,
    blob_callback=clean_token
).run()