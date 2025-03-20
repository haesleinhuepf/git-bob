def erase_outputs_of_code_cells(file_content):
    """
    Erase outputs of code cells in a Jupyter notebook.

    Parameters
    ----------
    notebook : str
        The notebook content as a string.
    """
    import re
    import json

    # removed invalid characters
    clean_file_content = re.sub(r'[\x00-\x1f\x7f]', '', file_content)

    notebook = json.loads(clean_file_content)
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            cell['outputs'] = []
            cell['execution_count'] = None
        # cell['id'] = None

    notebook["metadata"] = {}

    file_content = json.dumps(notebook, indent=1)
    return file_content


def restore_outputs_of_code_cells(new_content, original_ipynb_file_content):
    """
    Restore outputs of code cells in a Jupyter notebook from another notebook.
    """
    import json
    print("Recovering outputs in ipynb file")
    original_notebook = json.loads(original_ipynb_file_content)
    new_notebook = json.loads(new_content)

    original_code_cells = [cell for cell in original_notebook['cells'] if cell['cell_type'] == 'code']
    new_code_cells = [cell for cell in new_notebook['cells'] if cell['cell_type'] == 'code']

    if len(original_code_cells) != len(new_code_cells):
        raise ValueError("Number of code cells in the original and new notebooks do not match.")

    for o_cell, n_cell in zip(original_code_cells, new_code_cells):
        if "\n".join(o_cell['source']).strip() == "\n".join(n_cell['source']).strip():
            print("Original cell content", o_cell)
            print("New cell content", n_cell)
            if "outputs" in o_cell.keys():
                n_cell['outputs'] = o_cell['outputs']
                n_cell['execution_count'] = o_cell['execution_count']
        else:  # if code is different, any future results may be different, too
            raise ValueError("Code cells are different. Cannot restore outputs.")

    new_notebook["metadata"] = original_notebook["metadata"]
    return json.dumps(new_notebook, indent=1)


def execute_notebook(notebook_content, timeout=600, kernel_name='python3'):
    """
    Execute a Jupyter notebook and return whether an error occurred.

    Args:
        notebook_content (str): Content of the notebook file as string in json format.
        timeout (int): Timeout in seconds for each cell (default 600).
        kernel_name (str): The kernel to use for execution (default 'python3').

    Returns:
        str: content of the executed notebook.

    """
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor
    import jupyter_client
    import traceback

    # Get the list of available kernels
    kernels = jupyter_client.kernelspec.KernelSpecManager().get_all_specs()

    # Print the names of the kernels
    print("Available Jupyter kernels:")
    for name, spec in kernels.items():
        print(f"- {name}")

    # Load the notebook
    notebook = nbformat.reads(notebook_content, as_version=4)

    # Initialize the processor to execute the notebook
    ep = ExecutePreprocessor(timeout=timeout, kernel_name=kernel_name)

    error = None
    try:
        # Execute the notebook
        ep.preprocess(notebook, {'metadata': {'path': './'}})
    except Exception as e:
        # store traceback
        error = traceback.format_exc()
        print("Error during notebook execution:", e)

    # Save executed notebook
    notebook_content = nbformat.writes(notebook)

    # If we reach here, execution was successful
    return notebook_content, error
