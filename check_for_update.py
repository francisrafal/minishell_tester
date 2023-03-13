import os
import requests
import subprocess
import shutil

print("Checking for updates...")
# Define the repository URL and the local directory path
repo_url = "https://github.com/francisrafal/minishell_tester.git"
local_dir = os.path.join(os.path.expanduser("~"), "minishell_tester")

# Send a GET request to the GitHub API to fetch information about the repository
response = requests.get(f"https://api.github.com/repos/francisrafal/minishell_tester/commits")

# Check if the response contains any commits
if len(response.json()) > 0:
    # Extract the latest commit hash from the JSON response
    latest_commit_remote = response.json()[0]['sha']

    # Use subprocess to run the git log command and get the hash of the latest commit on the local repository
    if os.path.isdir(local_dir):
        output = subprocess.check_output(["git", "log", "-n", "1", "--pretty=format:%H"], cwd=local_dir)
        latest_commit_local = output.decode("utf-8").strip()
    else:
        latest_commit_local = ""

    # Check if the latest commit hash of the remote repository is different from the latest commit hash of the local repository
    if latest_commit_remote != latest_commit_local:
        # Delete the local directory if it already exists
        if os.path.isdir(local_dir):
            shutil.rmtree(local_dir)

        # Use subprocess to run the git clone command and clone the repository to the local directory
        try:
            subprocess.run(["git", "clone", repo_url, local_dir], timeout=10)
            print("Update complete.")
            # Run the updated Python script
        except subprocess.TimeoutExpired:
            # If the clone command times out, retry it once
            print("Clone command timed out. Retrying...")
            subprocess.run(["git", "clone", repo_url, local_dir], timeout=10)
            print("Update complete.")
    else:
        print("Local repository is up to date")
else:
    print("No commits found in repository")
