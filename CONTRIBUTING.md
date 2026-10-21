How to add your work (read this first) 
main is protected: nobody can change it directly. Every change goes in through a pull request (a request to add your work to main)
that the teacher approves. 
Who works whereTeam Your folderteam-database database/team-pipeline pipeline/ 
Change files in your own team’s folder only. If you need something changed in the other folder, ask that team. 
Way 1: on the GitHub website (easiest, no installs) 
Open https://github.com/Navdeep-Organisation/rag-project
Open the file you want to change and click the ✏️ pencil icon (or Add file → Upload files to add new files).
Make your change, then click Commit changes...
GitHub says you can’t change main. Choose Create a new branch for this commit and start a pull request. Name the branch
<your-folder>/<task>, e.g. database/add-chromadb.
Click Propose changes, then Create pull request.
Done. Wait for the teacher’s approval; the teacher merges it. 
Way 2: on your own computer (terminal) 
First time only: 
git clone https://github.com/Navdeep-Organisation/rag-project.git
cd rag-project

Every new task: 
git checkout main
git pull
git checkout -b database/add-chromadb

(Use your own folder and a short task name instead of database/add-chromadb.) 
Work on your files, then save and send them: 
git add .
git commit -m "Add ChromaDB setup"
git push -u origin database/add-chromadb

Then open the repo on GitHub, click the yellow Compare & pull request button, and click Create pull request. 
Rules 
One branch per task. Start a new branch for the next task.
Never commit .env, API keys, PDFs or vector database files.
Write a clear commit message: what you changed, in a few words.
If GitHub shows Update branch on your pull request, click it.
Stuck? Ask in the team group before trying random commands.
