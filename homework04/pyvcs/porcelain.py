import shutil
import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object, read_tree
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    index = read_index(gitdir)
    return commit_tree(gitdir, write_tree(gitdir, index), message, author=author)


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    # PUT YOUR CODE HERE
    update_ref(gitdir, "HEAD", obj_name)

    hash = commit_parse(read_object(obj_name, gitdir)[1])
    files = find_tree_files(hash, gitdir)

    index = read_index(gitdir)
    names = []
    for i in index:
        names.append(i.name)

    update_index(gitdir, [pathlib.Path(i[1]) for i in files], write=True)

    for i in names:
        first = i.split("/")[0]
        if pathlib.Path(first).is_dir():
            shutil.rmtree(first)
        else:
            if pathlib.Path(first).exists():
                os.remove(first)

    for i in files:
        isFound = i[1].find("/")
        if isFound != -1:
            elem1 = os.path.split(i[1])[0]
            if pathlib.Path(elem1).exists() == False:
                os.makedirs(elem1)
        with open(i[1], "wb") as f:
            f.write(read_object(i[0], gitdir)[1])
