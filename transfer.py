import requests

# Configuration
SOURCE_USER = "Sit314"
TARGET_USER = "ItaiSitnik"
GITHUB_TOKEN = "[INSERT_YOUR_GITHUB_TOKEN_HERE]"  # Token from Sit314 account

HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}


def get_owned_repos():
    """Fetches all public and private repositories owned by the authenticated user."""
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/user/repos?affiliation=owner&per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch repos: {response.status_code} - {response.text}")

        data = response.json()
        if not data:
            break

        # Ensure we only pick repos explicitly owned by SOURCE_USER
        for repo in data:
            if repo["owner"]["login"].lower() == SOURCE_USER.lower():
                repos.append(repo["name"])
        page += 1

    return repos


def transfer_repo(repo_name):
    """Initiates a repository ownership transfer to TARGET_USER."""
    url = f"https://api.github.com/repos/{SOURCE_USER}/{repo_name}/transfer"
    payload = {"new_owner": TARGET_USER}
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 202:
        print(f"[SUCCESS] Transfer requested for: {repo_name}")
    else:
        error_msg = response.json().get("message", response.text)
        print(f"[ERROR] Could not transfer '{repo_name}' (HTTP {response.status_code}): {error_msg}")


def main():
    print(f"Fetching repositories owned by {SOURCE_USER}...")
    repos = get_owned_repos()
    print(f"Found {len(repos)} repositories: {repos}\n")

    for repo in repos:
        transfer_repo(repo)

    print("\nDone! Check the email associated with ItaiSitnik to accept the transfers.")


if __name__ == "__main__":
    main()
