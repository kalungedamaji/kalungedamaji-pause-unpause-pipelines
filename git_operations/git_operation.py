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

