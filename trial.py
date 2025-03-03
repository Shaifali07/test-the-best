import os
import pathlib
baj="text.txt"
directory_path=os.path.join(pathlib.Path(__file__).parent.resolve(),"venv\papers\\")
print(directory_path+baj)
# s=directory_path.join(baj)
# print(s)