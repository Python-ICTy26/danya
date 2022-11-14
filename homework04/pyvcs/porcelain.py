import os
import pathlib
import shutil
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    return commit_tree(
        gitdir=gitdir, tree=write_tree(gitdir, read_index(gitdir)), message=message, author=author
    )


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    head = gitdir / "refs" / "heads" / obj_name

    if head.exists():
        with head.open(mode="r") as f:
            obj_name = f.read()

    index = read_index(gitdir)

    for file in index:
        if pathlib.Path(file.name).is_file():
            name = file.name.split("/")
            if len(name) > 1:
                shutil.rmtree(name[0])
            else:
                os.chmod(file.name, 0o777)
                os.remove(file.name)

    obj_path = gitdir / "objects" / obj_name[:2] / obj_name[2:]

    with obj_path.open(mode="rb") as obj_file:
        commit = obj_file.read()

    for tree_file in find_tree_files(commit_parse(commit).decode(), gitdir):

        name = tree_file[0].split("/")
        if len(name) > 1:
            pathlib.Path(name[0]).absolute().mkdir()

        with open(tree_file[0], "w") as tree_path:
            header, content = read_object(tree_file[1], gitdir)
            tree_path.write(content.decode())
