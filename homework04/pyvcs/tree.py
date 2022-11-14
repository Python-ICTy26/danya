import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    content = b""
    for file in index:
        if "/" in file.name:
            content += b"40000 "
            dir_name = file.name[: file.name.find("/")]
            content += dir_name.encode() + b"\0"
            next_files = oct(file.mode)[2:].encode() + b" "
            next_files += file.name[file.name.find("/") + 1 :].encode() + b"\0"
            next_files += file.sha1
            sha = hash_object(next_files, fmt="tree", write=True)
            content += bytes.fromhex(sha)
        else:
            content += oct(file.mode)[2:].encode() + b" "
            content += file.name.encode() + b"\0"
            content += file.sha1
    return hash_object(content, fmt="tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    if not author:
        author = f"{os.environ['GIT_AUTHOR_NAME']} <{os.environ['GIT_AUTHOR_EMAIL']}>"
    timestamp = int(time.mktime(time.localtime()))
    mark = "+" if time.timezone < 0 else "-"
    hours = abs(time.timezone // 3600)
    hours_str = "0" + str(hours) if hours < 10 else hours
    secs = abs((time.timezone // 60) % 60)
    secs_str = "0" + str(secs) if secs < 10 else secs
    author_time = f"{timestamp} {mark}{hours_str}{secs_str}"
    content = f"tree {tree}\n"
    if parent:
        content += f"parent {parent}\n"
    content += f"author {author} {author_time}\ncommitter {author} {author_time}\n\n{message}\n"
    hash = hash_object(content.encode("ascii"), "commit", True)
    return hash
