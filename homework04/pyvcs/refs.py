import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    ref_path = gitdir / pathlib.Path(ref)
    with ref_path.open(mode="w") as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    if ref_resolve(gitdir, ref) is None:
        return None
    with (gitdir / name).open("w") as f:
        f.write(f"ref: {ref}")


def ref_resolve(gitdir: pathlib.Path, refname: str) -> tp.Optional[str]:
    if refname == "HEAD":
        refname = get_ref(gitdir)
    try:
        file = (gitdir / refname).open("r")
        out = file.read()
        file.close()
        return out
    except:
        return None


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    return ref_resolve(gitdir, "HEAD")


def is_detached(gitdir: pathlib.Path) -> bool:
    ref_path = gitdir / "HEAD"
    with ref_path.open(mode="r") as f:
        ref_inner = str(f.read())
    return ref_inner.find("ref") == -1


def get_ref(gitdir: pathlib.Path) -> str:
    ref_path = gitdir / "HEAD"
    with open(ref_path, mode="r") as f:
        ref_inner = f.read()
    return ref_inner[ref_inner.find(" ") + 1 :].strip()
