Param(
  [string]$RepoName = "udf",
  [switch]$Private
)

# Requires GitHub CLI (gh) logged in: gh auth login
$Visibility = if ($Private) { "--private" } else { "--public" }

Write-Host "Creating repo $RepoName on GitHub..."
# Create the repo (exits nonzero if exists)
gh repo create $RepoName $Visibility -y
if ($LASTEXITCODE -ne 0) {
  Write-Host "gh repo create failed. Does the repo already exist?" -ForegroundColor Yellow
}

# Set remote and push
$User = (gh api user --jq .login)
git remote add origin "https://github.com/$User/$RepoName.git" 2>$null
git push -u origin main

