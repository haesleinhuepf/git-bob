def load_image_from_url(url):
    import urllib
    import io
    from PIL import Image
    from .._logger import Log
    Log().log("Loading image from URL: " + url)

    # Load the bytestream from the URL
    with urllib.request.urlopen(url) as response:
        bytestream = response.read()

    # Open the image from bytestream using PIL
    image = Image.open(io.BytesIO(bytestream))
    return image


def image_to_url(image):
    """
    Convert an image to a URL.
    """
    if isinstance(image, str) and (image.startswith("data:image") or image.startswith("http")):
        return image

    import base64
    import io
    from PIL import Image

    if isinstance(image, str):
        return image

    if isinstance(image, bytes):
        image = Image.open(io.BytesIO(image))

    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def download_url(url, output_path):
    """
    Downloads a file from the specified URL and saves it to the given output path.

    Args:
        url (str): The URL of the file to download.
        output_path (str): The path where the file will be saved.

    Returns:
        None
    """
    print("Downloading ", url, " to ", output_path)
    import requests
    import os
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Write the content to the output file in binary mode
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"File downloaded successfully and saved to {output_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while downloading the file: {e}")


def get_file_info(root_dir='.'):
    """Get a dictionary of files with their last change dates"""
    import os
    file_info = {}
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_info[file_path] = os.path.getmtime(file_path)
    return file_info


def get_modified_files(old_file_info, root_dir='.'):
    """Get a list of modified files since get_file_info was called"""
    import os
    modified_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path not in old_file_info:
                modified_files.append(file_path)  # New file
            elif os.path.getmtime(file_path) != old_file_info[file_path]:
                modified_files.append(file_path)  # Modified file

    result = []
    for m in modified_files:
        m = m.replace("\\", "/")
        if m.startswith("./"):
            m = m[2:]
        result.append(m)
    return result


def images_from_url_responses(response, input_shape=None):
    """Turns a list of OpenAI's URL responses into PIL images."""
    from skimage.io import imread
    from skimage import transform
    from PIL import Image
    # Removed unnecessary conversion to numpy arrays

    pil_images = [Image.fromarray(imread(item.url)) for item in response.data]

    if input_shape is not None:
        pil_images = [img.resize(input_shape) for img in pil_images]

    if len(pil_images) == 1:
        return pil_images[0]
    else:
        return pil_images



def read_text_file(filename):
    """Read the content of a text file."""
    with open(filename, 'r') as file:
        return file.read()


def write_text_file(filename, content):
    """Write content to a text file."""
    with open(filename, 'w') as file:
        file.write(content)


def read_binary_file(filename):
    """Read the content of a binary file."""
    with open(filename, 'rb') as file:
        return file.read()


def write_binary_file(filename, content):
    """Write content to a binary file."""
    with open(filename, 'wb') as file:
        file.write(content)


def is_ignored(filename, repository, branch_name):
    """Check if a file is ignored according to .gitbobignore patterns

    Parameters
    ----------
    filename : str
        The filename to check
    repository : str
        The repository name
    branch_name : str
        The branch name

    Returns
    -------
    bool
        True if the file should be ignored
    """
    from ._config import Config

    # Always ignore .github and .gitlab files
    if ".github" in filename or ".gitlab" in filename:
        return True

    try:
        gitbob_ignore = Config.git_utilities.decode_file(
            Config.git_utilities.get_file_in_repository(repository, branch_name, ".gitbobignore")
        )
        patterns = gitbob_ignore.splitlines()

        from fnmatch import fnmatch
        return any(fnmatch(filename, pattern.strip()) for pattern in patterns if pattern.strip())
    except:
        return False


def run_cli(command:str, check=False, verbose=False):
    import subprocess

    result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
    if verbose:
        print("\n", result.stdout)
        print("\n", result.stderr)

    return f"## Command\n```\n{command}\n```\n## StdOut\n```\n{result.stdout}\n```\n## StdErr\n```\n{result.stderr}\n```\n"