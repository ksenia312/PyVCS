import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f"{fmt} {len(data)}\0"
    store = header + data.decode()
    hash = hashlib.sha1(store.encode()).hexdigest()
    if write:
        path = repo_find() / "objects" / hash[:2]
        path.mkdir(exist_ok=True)
        with (path / hash[2:]).open("wb") as f:
            new_data = (fmt + " " + str(len(data))).encode()
            new_data = new_data + b"\00" + data
            f.write(zlib.compress(new_data))
    return hash


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    path = gitdir / "objects"
    if not 4 <= len(obj_name) <= 40:
        raise AssertionError(f"Not a valid object name {obj_name}")
    a = []
    for i in (path / obj_name[:2]).glob(f"{obj_name[2:]}*"):
        a.append(obj_name[:2] + i.name)

    if not a:
        raise AssertionError(f"Not a valid object name {obj_name}")
    return a


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, int]:
    path = gitdir / "objects" / sha[:2] / sha[2:]
    with path.open("rb") as f:
        data = zlib.decompress(f.read())
        fmt = data[:data.find(b" ")].decode()
        content = data[data.find(b"\x00") + 1:]
    return fmt, content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
