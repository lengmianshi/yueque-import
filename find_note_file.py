import os
from config import config


def find_all_file(home_dir):
    for root, dirs, files in os.walk(home_dir, topdown=False):
        for f in files:
            if 'youdaonote-images' in root:
                continue
            yield os.path.join(root, f)


"""列出所有note文档"""
if __name__ == '__main__':
    home_dir = config['dir']
    for file in find_all_file(home_dir):
        if file.endswith(".note"):
            print(file)
