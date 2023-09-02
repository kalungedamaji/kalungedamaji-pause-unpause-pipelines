from git import Repo
def commit_and_push_code(config_repo_path, branch_name, commit_message):
    print("\n Started committing the changes on branch  \n" + branch_name)
    PATH_OF_GIT_REPO = config_repo_path+'.git'  # make sure .git folder is properly configured

    repo = Repo(PATH_OF_GIT_REPO)

    # Checkout the main branch
    main_branch = "main"
    repo.git.checkout(main_branch)

    # Fetch the latest changes from the remote
    repo.remotes.origin.fetch()

    # Create  New Branch
    new_branch = repo.create_head(branch_name)
    new_branch.checkout()

    # Add and commit the changes
    repo.index.add('*')
    repo.index.commit(commit_message)

    # Push the changes to the remote repository
    origin = repo.remote(name='origin')
    origin.push(new_branch)

    # Switch back to main branch
    repo.git.checkout(main_branch)
    print("\n Pushed changes to the branch " + branch_name)

def checkout_configuration_repo():
    repo_url = "https://github.gamesys.co.uk/Data/vitruvian-deployment-configurations"
    local_directory = "/vitruvian-deployment-configurations"

    # Clone the GitHub repository to the local directory
    repo = git.Repo.clone_from(repo_url, local_directory)

    # Optionally, you can perform additional Git operations on the repository if needed
    # For example, you can fetch, pull, or commit changes programmatically

    # Fetch updates from the remote repository (equivalent to 'git fetch' command)
    repo.remotes.origin.fetch()

    # Pull changes from the remote repository (equivalent to 'git pull' command)
    repo.remotes.origin.pull()
