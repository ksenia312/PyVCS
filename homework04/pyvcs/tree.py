import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    data = b""
    for i in index:
        if "/" in i.name:
            border = i.name.find("/")
            folder = (i.name[: border]).encode()  # second
            mode = oct(i.mode)[2:].encode()
            children = b"" + mode + b" " + i.name[border + 1:].encode() + b"\0" + i.sha1
            hash = bytes.fromhex(hash_object(children, fmt="tree", write=True))
            data += b"40000 " + folder + b"\0" + hash
        else:
            mode = oct(i.mode)[2:].encode()
            data += mode + b" " + i.name.encode() + b"\0" + i.sha1
    return hash_object(data, fmt="tree", write=True)


def commit_tree(
        gitdir: pathlib.Path,
        tree: str,
        message: str,
        parent: tp.Optional[str] = None,
        author: tp.Optional[str] = None, ) -> str:

    data = [f"tree {tree}"]
    if parent:
        data.append(f"parent {parent}")
    if not author:
        name, email = os.getenv("GIT_AUTHOR_NAME"), os.getenv("GIT_AUTHOR_EMAIL")
        author = "{} <{}>".format(name, email)

    zone = time.timezone
    offset = "+" if zone < 0 else "-"
    zone = abs(zone)
    zone = zone // 60
    offset += f"{zone // 60:02}"
    offset += f"{zone % 60:02}"

    local = time.localtime()
    sec = time.mktime(local)
    sec = int(sec)

    data.append(f"author {author} {sec} {offset}")
    data.append(f"committer {author} {sec} {offset}")
    data.append(f"\n{message}\n")
    encData = "\n".join(data)
    encData = encData.encode()

    return hash_object(encData, "commit", write=True)
