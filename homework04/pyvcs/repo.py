import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    name = os.getenv("GIT_DIR", ".pyvcs")
    workdir = pathlib.Path(workdir)

    while pathlib.Path(workdir.absolute().root) != workdir.absolute():
        if (workdir / name).is_dir():
            return workdir / name
        workdir = workdir.parent

    if (workdir / name).is_dir():
        return workdir / name
    raise AssertionError("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    name = os.getenv("GIT_DIR", ".pyvcs")
    workdir = pathlib.Path(workdir)
    path = workdir / name

    if workdir.is_file():
        raise AssertionError(f"{workdir} is not a directory")
    os.makedirs(path / "refs" / "heads", exist_ok=True)
    os.makedirs(path / "refs" / "tags", exist_ok=True)

    (path / "objects").mkdir()

    with (path / "config").open("w") as f:
        f.write(
            "[core]\n\t"
            "repositoryformatversion = 0\n\t"
            "filemode = true\n\t"
            "bare = false\n\t"
            "logallrefupdates = false\n"
        )

    with (path / "HEAD").open("w") as f:
        f.write("ref: refs/heads/master\n")

    with (path / "description").open("w") as f:
        f.write("Unnamed pyvcs repository.\n")

    return path
