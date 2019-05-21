# Explainable-Text-Classifier
Explainable Text Classifier @ Web Application 

# Current Progress 
### 5/20/2019
1. Django: 40%
2. Task1: 50%
3. Task0: 0%

# Git cheatsheet
### How to acquire a repository - git clone
`git clone <repository-name>`     e.g. `git clone https://github.com/torvalds/linux.git`

This code will clone the repository into the local disk. Most importantly, this repository folder will include git config files, so you can `git push`,`git pull`,`git add .` and etc.

### How to create a repository?
* `git init` - Create initial configuration files for your project.
* `git add ./<file>` - Prepare the files for the next `commit`. If use `.`, you will add all files/folders into next `commit`.
* `git commit -m "<your-comment>"` - Commit files into **your local repository**.
* `git remote add origin <remote-repository-address>` - link your **local repository to remote repository**.
* `git push origin <branch-name>` - Push your local repository into the remote repository.

### How to commit your change?
Similar as create a repository
* `git add .`
* `git commit -m "<your-comment>"`
* `git push origin <branch-name>`

### How to deal with conflict when commit?
Imagine you create a version 5 based on a version 4 repository. Someone has already commit a version 5 based on version 4 repository. Thus, your commit **is not higher than** the newest version. 
* Solution 1: `git push origin <branch-name> -f`.
* Solution 2: `git pull` then *git* tells you your version and the newest version has some conflicts. Solve these conflicts manually and **commit** again.

### How to update your version?
Imagine you are in version 4 repository. Someone has already commit a version 5 based on version 4. Then, you had better `git pull` before making any change. Otherwise, you will fall into *conflicts when commit*.
* `git fetch` - Fetch all updated branches information from **remote repository** to **local repository**.
* `git pull` - Update the current branch where you are.

### Everything about branch.
* `git fetch` - same. Very useful to synchronize your local information with the remote information.
* `git branch` - check all local branches.
* `git checkout -b <branch-name>` - create a new branch. You need to commit to remote repository.
* `git checkout <branch-name>` - switch to another branch.
* `git merge <branch-name>` - your will merge from another branch to your branch.
##### Deal with conflicits
* `git checkout <branch-name>` If you make any change to the newest version, you must *commit your version*, before switch to another branch. Otherwise, you can use `git stash` to push your version into a *stack*, recover to the unchanged code, and `git pop` to pop the version from the *stack* when returning back to this branch.
* `git merge <branch-name>` Very similar as *conflict when commit*. But,it is very friendly when *conflict when merge*. The git will merge as many as files it can, and mark all conflicts needed to resolve. So you delete the choice you don't want to keep and commit the change again.
