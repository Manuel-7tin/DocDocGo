import os
import shutil

st = "placeholder"

def a_func():
    folder_path = os.path.dirname(__file__)
    stay_there_path = os.path.join(folder_path, 'stay_there')
    os.makedirs(stay_there_path, exist_ok=True)

    for file in os.listdir(folder_path):
        full_file_path = os.path.join(folder_path, file)
        if file.endswith('.crdownload') and os.path.isfile(full_file_path):
            shutil.move(full_file_path, os.path.join(stay_there_path, file))

def extract_name(name, pp):
    if name == "":
        return ""
    split_name = name.split(" ")
    for i in range(2):
        if split_name[0][:3].lower() == "j25" or split_name[0][:3].lower() == "m25" or split_name[0][1:3].isdigit():
            name = " ".join([item for item in split_name if split_name.index(item) != 0])
        split_name = name.split(" ")
        if pp.lower() in split_name[0].lower() and len(split_name[0]) < len(pp) + 3:
            name = " ".join([item for item in split_name if split_name.index(item) != 0])
    def status():
        """Prints a status message indicating the function is operational.

        This function has no arguments and returns ``None``. It writes the string ``"i am working"`` to standard output."""
        print("i am working")

    if split_name[0].lower() == "dip" or "dipif" in split_name[0].lower():
        name = " ".join([item for item in split_name if split_name.index(item) != 0])
    return name.strip()

def raise_error(e: str, error_type: int, action:str, stop: bool=True):
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
    def __init__(self, folder_path):
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
