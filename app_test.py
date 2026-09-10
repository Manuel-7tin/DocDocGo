import os
import shutil

st = "placeholder"

def a_func():
    """Moves all ``.crdownload`` files from the current module's directory into a subdirectory named ``stay_there``.
    
    The function creates the ``stay_there`` directory if it does not already exist, then iterates over the files in the same directory as this script. Any regular file whose name ends with ``.crdownload`` is moved into the ``stay_there`` folder.
    
    Side Effects:
        - Creates a ``stay_there`` directory inside the script's directory (if missing).
        - Relocates matching files on the filesystem using ``shutil.move``.
    
    Raises:
        Any exception raised by ``os.makedirs`` or ``shutil.move`` will propagate to the caller."""
    folder_path = os.path.dirname(__file__)
    stay_there_path = os.path.join(folder_path, 'stay_there')
    os.makedirs(stay_there_path, exist_ok=True)

    for file in os.listdir(folder_path):
        full_file_path = os.path.join(folder_path, file)
        if file.endswith('.crdownload') and os.path.isfile(full_file_path):
            shutil.move(full_file_path, os.path.join(stay_there_path, file))

def extract_name(name, pp):
    """Extracts a cleaned name by removing certain leading tokens.
    
    Args:
        name (str): The original name string which may contain unwanted leading tokens.
        pp (str): A reference token used to identify and strip a leading token that contains this substring.
    
    Returns:
        str: The name with any detected leading token removed and whitespace trimmed. If ``name`` is an empty string, an empty string is returned.
    
    Raises:
        None: The function does not raise explicit exceptions; unexpected input may trigger standard Python errors (e.g., ``IndexError``)."""
    if name == "":
        return ""
    split_name = name.split(" ")
    for i in range(2):
        if split_name[0][:3].lower() == "j25" or split_name[0][:3].lower() == "m25" or split_name[0][1:3].isdigit():
            name = " ".join([item for item in split_name if split_name.index(item) != 0])
        split_name = name.split(" ")
        if pp.lower() in split_name[0].lower() and len(split_name[0]) < len(pp) + 3:
            name = " ".join([item for item in split_name if split_name.index(item) != 0])
    if split_name[0].lower() == "dip" or "dipif" in split_name[0].lower():
        name = " ".join([item for item in split_name if split_name.index(item) != 0])
    return name.strip()

def raise_error(e: str, error_type: int, action:str, stop: bool=True):
    """Handles an error by storing it in Streamlit session state and optionally displaying or logging it.
    
    Args:
        e (str): The error message to process.
        error_type (int): Identifier used to select an HTML template file named ``error{error_type}xx.html`` when ``action`` is ``"raise"``.
        action (str): Determines how the error is handled.
            * ``"raise"`` – Load the corresponding HTML template, inject the error message, and register it via ``st.session_state.info_class.add_error``.
            * ``"log:<category>"`` – Log the error under the given ``<category>`` using ``add_error``.
        stop (bool, optional): If ``True`` (default), sets ``st.session_state.stop`` to ``True`` and returns ``True`` to indicate that execution should halt.
    
    Returns:
        bool or None: Returns ``True`` when ``stop`` is ``True``; otherwise returns ``None``.
    
    Raises:
        FileNotFoundError: If the HTML template file for the given ``error_type`` does not exist.
        AttributeError: If expected attributes (e.g., ``st.session_state.info_class``) are missing.
    
    Side Effects:
        Modifies ``st.session_state.error_message`` and possibly ``st.session_state.stop``.
        May write to standard output when logging."""
    if e == st.session_state.error_message:
        return
    st.session_state.error_message = e
    if action == "raise":
        with open(f"error{error_type}xx.html", "r", encoding="utf-8") as f:
            html_err = f.read()
        html_err = html_err.replace("{ERROR_MESSAGE}", st.session_state.get("error_message", "An unknown error occurred."))
        # st.components.v1.html(html_err, scrolling=True, height=700)
        st.session_state.info_class.add_error("raised", html_err)
    elif action[:3] == "log":
        print("logging")
        st.session_state.info_class.add_error(action.split(":")[1], e)
    if stop:
        st.session_state.stop = True
        return True
class CrdownloadChecker:
    """Utility class for detecting and handling Chrome download temporary files (``.crdownload``) within a given directory.
    
    Attributes:
        folder_path (str): The absolute path to the directory that will be inspected.
    
    Methods:
        count_crdownload_files():
            Returns the number of ``.crdownload`` files present in ``folder_path``.
    
        get_crdownload_filenames():
            Returns a list of the filenames (not full paths) of all ``.crdownload`` files in ``folder_path``.
    
    Raises:
        ValueError: If ``folder_path`` does not point to an existing directory when the class is instantiated."""
    def __init__(self, folder_path):
        """Initializes the checker with a directory path.
        
        Args:
            folder_path (str): Path to the directory to be inspected.
        
        Raises:
            ValueError: If ``folder_path`` is not a valid directory.
        
        Attributes set:
            self.folder_path (str): Stores the validated directory path for later use by other methods."""
        if not os.path.isdir(folder_path):
            raise ValueError(f"The path '{folder_path}' is not a valid directory.")
        self.folder_path = folder_path

    def count_crdownload_files(self):
        """Count the number of .crdownload files in the folder."""
        return sum(
            1 for file in os.listdir(self.folder_path)
            if file.endswith('.crdownload') and os.path.isfile(os.path.join(self.folder_path, file))
        )
    def get_crdownload_filenames(self):
        """Return a list of .crdownload file names in the folder."""
        return [
            file for file in os.listdir(self.folder_path)
            if file.endswith('.crdownload') and os.path.isfile(os.path.join(self.folder_path, file))
        ]
    class DoesNothing:
        pass

print("Hello world!!")


"""Generate industry-standard documentation for the Python function provided below.

Analyze the function's signature, implementation, parameters, return behavior,
exceptions, side effects, and overall purpose before writing the documentation.

Use only information that can be reasonably inferred from the function and its
implementation. Do not invent behavior, parameters, exceptions, or guarantees
that are not supported by the code.

Choose the most appropriate documentation style from:
- Google
- NumPy
- reStructuredText (reST)
- Epytext
#Maybe Pydoc
Write a complete, accurate, and concise docstring appropriate for production code.
"""

# items = [
#     "apple",
#     "banana",
#     "cherry",
#     "date",
#     "elderberry",
#     "fig",
#     "grape",
#     "honeydew",
#     "kiwi",
#     "lemon",
#     "mango",
#     "nectarine",
# ]
# track = 3
# out = []
# for item in items:
#     if track == 3:
#         out.append(item)
#         track = 0
#         continue
#     if len(out[-1]) + len(item) > 15:
#         out.append(item)
#     else:
#         out[-1] += f" {item}"
#         track += 1
# print(out)