# Explainable-Text-Classifier
Explainable Text Classifier @ Web Application 

Bootstrap: 
* (Component) https://getbootstrap.com/docs/4.3/components/alerts/
* (Utility)   https://getbootstrap.com/docs/4.3/utilities/borders/
           
JQuery: https://www.w3schools.com/jquery/default.asp .**Selector** and **Traverse** parts are very helpful for you to find a HTML element.

# How to run the application
##### Machine Learning Server
* `cd ./classifierModel`
* `python server.py`

It will launch the ML server, providing PA2's classification task API for Django backend.

##### Django Web Server
in the root directory:
* `python manager.py runserver`

This command will launch the Django Web Server at localhost:8000. Type the url `http://localhost:8000/classifier` to use the web application. **Every time you edit the .html or .py, you don't have to restart the webserver.**

##### Spread the web application to the LAN
`ifconfig` - It will show your ipv4 IP. Then, edit the file *ExplainAny/settings.py* and uncomment `ALLOWED_HOSTS = ['100.81.39.76']`. Fill your IP into the `string` field. Then, use the following command the lanuch the web server:

`python manager.py runserver 0.0.0.0:8000`

Finally, type `<your IP address>:8000/classifier` to visit the website.


# Current Progress 
### 5/20/2019
1. Django: 40%
2. Task1: 50%
3. Task2: 0%

### 5/24/2019
1. Django: 60%
* Add the progress-bar, with dynamic adjustation.
* Replace Form submit with Ajax async submit.

2. Task1: 50%
3. Task2: 5%
* Research on an existing code.

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
