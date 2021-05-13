import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    path = gitdir / ref
    with path.open("w") as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    path = gitdir / name
    with path.open("w") as f:
        f.write(ref)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD":
        refname = get_ref(gitdir)
    detached = is_detached(gitdir)
    if detached:
        return refname
    with (gitdir / pathlib.Path(refname)).open("r") as f:
        data = f.read()
    return data


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    return ref_resolve(gitdir, "HEAD") if (gitdir / get_ref(gitdir)).exists() \
        else None


def is_detached(gitdir: pathlib.Path) -> bool:
    path = gitdir / "HEAD"
    with path.open("r") as f:
        data = f.read()
        if data.find("ref") == -1:
            return True
    return False


def get_ref(gitdir: pathlib.Path) -> str:
    path = gitdir / "HEAD"
    detached = is_detached(gitdir)
    with path.open("r") as f:
        ref = f.read()[5:-1] if not detached else f.read()
    return ref
