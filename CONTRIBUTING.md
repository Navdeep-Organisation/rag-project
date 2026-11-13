# How to Contribute (Read This First)

> **Important:**
> * **`main` is protected:** Nobody can push directly to `main`. It only receives the final, best-performing pipeline approved by all the team members via a Pull Request (PR).
> * **Work on your team's dedicated branch:** Each team has its own branch (`team-database` and `team-pipeline`) to develop, test, and compare different methods. Keep all experimental methods on your team's branch until the final winning method is selected to merge into `main`.

---

## 1. Team Branches & Folder Ownership

Only edit files inside your assigned team folder and push to your team's branch. If you need changes in the other folder, coordinate with that team first.

| Team | Team Branch | Assigned Folder |
| :--- | :--- | :--- |
| `team-database` | `team-database` | `database/` |
| `team-pipeline` | `team-pipeline` | `pipeline/` |

---

## 2. How to Submit Your Work

### Option A: Directly on GitHub (No Terminal Needed)
1. Open the repository: [Navdeep-Organisation/rag-project](https://github.com/Navdeep-Organisation/rag-project).
2. Switch the branch dropdown (top-left, currently showing `main`) to your team's branch (`team-database` or `team-pipeline`).
3. Navigate to your team's folder (`database/` or `pipeline/`).
4. Click the **✏️ (pencil icon)** to edit an existing file, or click **Add file → Upload files** to add new files.
5. Make your changes and click **Commit changes...** directly to your team's branch (or create a sub-branch `<your-folder>/<short-task-name>` targeting your team's branch).
6. At the end of the project, open a **Pull Request** to merge the final winning setup into `main` for teacher approval.

---

### Option B: Locally via Terminal

#### First-Time Setup
Clone the repository to your computer (use SSH if you have SSH keys configured, otherwise use HTTPS):

    # Using SSH (recommended if configured):
    git clone git@github.com:Navdeep-Organisation/rag-project.git

    # Or using HTTPS:
    git clone https://github.com/Navdeep-Organisation/rag-project.git

    cd rag-project

#### Step 1: Check and Switch to Your Team Branch
Before making any edits, verify which branch you are on and sync with your team's remote branch:

    # Download all remote branches from GitHub
    git fetch origin

    # List all local and remote branches to verify names
    git branch -a

    # Switch to your team's branch (use team-database if you are on the database team)
    git checkout team-pipeline

    # Pull the latest changes from your teammates
    git pull origin team-pipeline

*(Run `git branch --show-current` anytime to confirm you are on `team-pipeline` and NOT `main`.)*

---

#### Step 2: Commit & Push Your Changes
You can either push directly to your team branch or use a short task sub-branch:

**Method 1: Pushing directly to your team branch (`team-pipeline` / `team-database`)**

    # 1. Check which files were modified or added (ensure ONLY your team folder appears)
    git status

    # 2. Stage changes inside your team folder
    git add pipeline/

    # 3. Commit with a clear message
    git commit -m "Add recursive text splitter strategy"

    # 4. Push to your team's branch on GitHub
    git push origin team-pipeline

**Method 2: Working on a feature sub-branch (Recommended for bigger tasks)**
If multiple teammates are editing files at the same time, branch off your team branch so you don't overwrite each other's work:

    # 1. Create and switch to a new task branch from team-pipeline
    git checkout -b pipeline/add-chunking team-pipeline

    # 2. Stage and commit your work
    git add pipeline/
    git commit -m "Add semantic chunking strategy"

    # 3. Push the sub-branch to GitHub (the -u flag links it for future git push/pull)
    git push -u origin pipeline/add-chunking

Then open GitHub, click **Compare & pull request**, and set the **base branch** to `team-pipeline` (not `main`) to merge your task into your team's branch.

---

#### Step 3: Final Merge into `main` (End of Project)
Once all methods are evaluated and the best-performing one is chosen:
1. Create a clean branch from `main` containing only the winning implementation (`git checkout -b pipeline/final-winner main`).
2. Push it and open a **Pull Request** targeting `main` for the teacher to review and approve.

---

## 3. Ground Rules
* **Never push directly to `main`:** Develop and compare all methods on `team-database` or `team-pipeline`.
* **Keep sensitive and heavy files out of Git:** Never commit `.env` files, API keys, PDFs, or vector database files.
* **Write clear commit messages:** Briefly summarize what you changed (e.g., `"Add Unstructured document loader"`).
* **Keep your PR up to date:** If GitHub displays an **Update branch** button on your Pull Request, click it.
* **Ask before guessing:** If you get stuck with Git, ask in the team group before running unfamiliar commands.