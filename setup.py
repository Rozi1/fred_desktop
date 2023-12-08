# import sys
# sys.setrecursionlimit(10000)
# from distutils.core import setup
# import py2exe

# setup(console=['main.py'])

from cx_Freeze import setup, Executable

base = None  # Replace with your base if needed (e.g., "Win32GUI")

executables = [Executable(
    script="main.py",  # Replace with the name of your main script
    base=base,
    icon=None  # Optionally, specify the path to an icon file for your executable
)]

build_options = {
    "packages": [],  # List any additional packages your script uses
    "excludes": [],  # List any modules or packages to exclude
    "include_files": []  # List data files your script depends on
}

setup(
    name="Fred Text to Speech",
    version="1.0",
    description="Your application description",
    options={"build_exe": build_options},
    executables=executables
)
