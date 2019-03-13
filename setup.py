import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]
packages = ["os", "pygame", "operator", "string", "random" , "math"]
include_files = ["main.py", "Pieces3.py", "gridfunctions.py" , "Tile.py", "spriteclasses.py",
 "img"]


cx_Freeze.setup(name = "Chess",
        description = "A Basic Chess Game using Pygame Library",
        options = {"build_exe": {"packages": packages, "include_files": include_files}},
        executables = executables
        )