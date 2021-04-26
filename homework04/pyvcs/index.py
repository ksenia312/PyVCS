import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        name = str.encode(self.name)
        form = f"!10i20sh{len(name) + 3}s"
        return struct.pack(
            form,
            self.ctime_s, self.ctime_n, self.mtime_s, self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            name
        )

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        form = f"!10i20sh{len(data) - 62}s"
        index = struct.unpack(form, data)
        index = list(index)
        index[-1] = index[-1].strip(b"\00")
        index[-1] = index[-1].decode()
        return GitIndexEntry(*index)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    reading_index, a, b = [], 8, 12
    path = gitdir / 'index'
    if not path.exists():
        return reading_index
    else:
        with path.open("rb") as f:
            data = f.read()

    count = struct.unpack("!i", data[a:b])[0]
    for step in range(count):
        a = data.index(b"\00", a + 68, len(data))
        while not (a - 11) % 8 == 0:
            a += 1
        indexE = GitIndexEntry
        unpacked = indexE.unpack(data[b : a + 1])
        reading_index.append(unpacked)
        b = a + 1
    return reading_index


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # PUT YOUR CODE HERE
    ...


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    ...


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...
