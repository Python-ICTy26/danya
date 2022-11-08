import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    workdir = pathlib.Path(workdir)
    git_dir = os.environ.get("GIT_DIR") or ".git"
    path = workdir / git_dir
    if path.exists():
        return path
    for dir in path.parents:
        if dir.name == git_dir:
            return dir
    raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    workdir = pathlib.Path(workdir)
    if not workdir.is_dir():
        raise Exception(f"{workdir.name} is not a directory")

    dir_name = os.environ.get("GIT_DIR") or '.git'
    path = workdir / dir_name

    # if path.exists():
    #     print('Reinitialized existing pyvcs repository')
    #     return path

    try:
        path.mkdir(parents=True)
        (path / "refs" / "heads").mkdir(parents=True)
        (path / "refs" / "tags").mkdir(parents=True)
        (path / "objects").mkdir(parents=True)
    except FileExistsError:
        print('exist')

    with open(path / "HEAD", 'w') as head, open(path / "config", 'w') as config, open(path / "description", 'w') as description:
        head.write("ref: refs/heads/master\n")
        config.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
        description.write("Unnamed pyvcs repository.\n")

    return path

