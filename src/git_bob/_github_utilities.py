def rename_file_in_repository(repository, branch_name, old_file_path, new_file_path, commit_message="Rename file"):
    """
    Rename a file in the specified GitHub repository on a given branch.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    branch_name : str
        The name of the branch to rename the file in.
    old_file_path : str
        The current file path.
    new_file_path : str
        The new file path.
    commit_message : str, optional
        The commit message for the rename. Default is "Rename file".

    Returns
    -------
    bool
        True if the file was renamed successfully, False otherwise.
    """
    Log().log(f"-> rename_file_in_repository({repository}, {branch_name}, {old_file_path}, {new_file_path})")

    # Authenticate with GitHub
    repo = get_github_repository(repository)

    try:
        file = get_file_in_repository(repository, branch_name, old_file_path)
        # Create a new file with the old content at the new path
        repo.create_file(new_file_path, commit_message, file.decoded_content.decode(), branch=branch_name)

        # Delete the old file
        repo.delete_file(old_file_path, commit_message, file.sha, branch=branch_name)

        return True
    except Exception as e:
        print(f"Error renaming file: {str(e)}")
        return False


def delete_file_in_repository(repository, branch_name, file_path, commit_message="Delete file"):
    """
    Delete a file from the specified GitHub repository on a given branch.

    Parameters
    ----------
    repository : str
        The full name of the GitHub repository (e.g., "username/repo-name").
    branch_name : str
        The name of the branch to delete the file from.
    file_path : str
        The path of the file to delete.
    commit_message : str, optional
        The commit message for the deletion. Default is "Delete file".

    Returns
    -------
    bool
        True if the file was deleted successfully, False otherwise.
    """
    Log().log(f"-> delete_file_in_repository({repository}, {branch_name}, {file_path})")

    # Authenticate with GitHub
    repo = get_github_repository(repository)

    try:
        file = get_file_in_repository(repository, branch_name, file_path)
        repo.delete_file(file.path, commit_message, file.sha, branch=branch_name)
        return True
    except Exception as e:
        print(f"Error deleting file: {str(e)}")
        return False
