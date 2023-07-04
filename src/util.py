import subprocess
import json
from os.path import exists


def file_exists(name: str):
    return exists(name)


def write_file(target, content, clear=False):
    with open(target, "w") as f:
        if clear:
            f.truncate(0)
        f.write(content)


def copy_file(source, target):
    subprocess.run("cp " + source + " " + target, shell=True)


def read_file(target):
    with open(target) as f:
        return f.read()


def read_json(file):
    with open(file, "r") as f:
        return json.load(f)


def delete_file(target):
    try:
        subprocess.call(["rm", "-f", target])
    except Exception as e:
        # print("ERROR! tried to delete file", target, "but failed because", e)
        pass
