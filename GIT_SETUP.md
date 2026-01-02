# Git Setup Guide - Push to GitHub

## Initial Setup

### Option 1: Push Existing Repository (Recommended)

If you already have the code locally:

```bash
# Navigate to project directory
cd D:\DoganSystem

# Initialize git (if not already initialized)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Complete DoganSystem implementation"

# Add remote repository
git remote add origin https://github.com/doganlap/DoganSystem.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Option 2: Create New Repository

If starting fresh:

```bash
# Navigate to project directory
cd D:\DoganSystem

# Initialize git
git init

# Add README
echo "# DoganSystem" >> README.md
git add README.md
git commit -m "first commit"

# Rename branch to main
git branch -M main

# Add remote
git remote add origin https://github.com/doganlap/DoganSystem.git

# Push
git push -u origin main
```

## Files Included

The repository includes:
- ✅ `README.md` - Complete project documentation
- ✅ `.gitignore` - Proper ignore patterns for .NET, Python, Node.js
- ✅ `LICENSE` - MIT License
- ✅ All source code
- ✅ Documentation files

## What's Excluded (.gitignore)

- Environment files (`.env`)
- Database files (`*.db`, `*.sqlite`)
- Build outputs (`bin/`, `obj/`)
- Node modules (`node_modules/`)
- Python cache (`__pycache__/`)
- IDE files (`.vs/`, `.idea/`)
- Logs (`*.log`)

## Authentication

If prompted for credentials:

1. **Personal Access Token** (Recommended):
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate new token with `repo` scope
   - Use token as password when pushing

2. **SSH Key** (Alternative):
   ```bash
   # Generate SSH key
   ssh-keygen -t ed25519 -C "your_email@example.com"
   
   # Add to GitHub: Settings > SSH and GPG keys
   
   # Change remote to SSH
   git remote set-url origin git@github.com:doganlap/DoganSystem.git
   ```

## Verify Setup

```bash
# Check remote
git remote -v

# Check status
git status

# View commits
git log
```

## Common Commands

```bash
# Add changes
git add .

# Commit
git commit -m "Your commit message"

# Push
git push

# Pull latest
git pull

# Check status
git status

# View branches
git branch
```

## Troubleshooting

### Error: "remote origin already exists"
```bash
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/doganlap/DoganSystem.git
```

### Error: "failed to push some refs"
```bash
# Pull first, then push
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Error: Authentication failed
- Use Personal Access Token instead of password
- Or set up SSH keys

## Next Steps

After pushing:
1. ✅ Verify files on GitHub
2. ✅ Add repository description
3. ✅ Add topics/tags
4. ✅ Set up GitHub Actions (optional)
5. ✅ Add collaborators (optional)
