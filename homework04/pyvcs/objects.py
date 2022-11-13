import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

# from pyvcs.refs import update_ref
from pyvcs.repo import repo_find

# from repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    store_encoded = f"{fmt} {len(data)}\0".encode() + data
    hash = hashlib.sha1(store_encoded).hexdigest()

    if write:
        hash_title, hash_content = hash[:2], hash[2:]
        gitdir = repo_find()
        hash_path = gitdir / "objects" / hash_title
        hash_path.mkdir(exist_ok=True, parents=True)
        with open(hash_path / hash_content, "wb") as hash_file:
            hash_file.write(zlib.compress(store_encoded))

    return hash


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if not 4 <= len(obj_name) <= 40:
        raise Exception(f"Not a valid object name {obj_name}")
    objects = []
    gitdir = repo_find()
    objs_path = gitdir / "objects" / obj_name[:2]
    for obj_path in objs_path.iterdir():
        if obj_path.name.find(obj_name[2:]) == 0:
            objects.append(obj_name[:2] + obj_path.name)
    if len(objects):
        return objects
    else:
        raise Exception(f"Not a valid object name {obj_name}")


def find_object(obj_name: str, gitdir: pathlib.Path) -> tp.Optional[str]:
    if obj_name[2:] in str(gitdir.parts[-1]):
        return f"{gitdir.parts[-2]}{gitdir.parts[-1]}"
    else:
        return None


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = gitdir / "objects" / sha[:2] / sha[2:]
    with open(path, "rb") as f:
        content = zlib.decompress(f.read())
    separator = content.find(b"\x00")
    header = content[:separator]
    fmt = header[: header.find(b" ")]
    data = content[(separator + 1) :]
    return fmt.decode(), data


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    result = []
    while len(data) != 0:
        mode = int(data[: data.find(b" ")].decode())
        data = data[data.find(b" ") + 1 :]
        name = data[: data.find(b"\x00")].decode()
        data = data[data.find(b"\x00") + 1 :]
        sha = bytes.hex(data[:20])
        data = data[20:]
        result.append((mode, name, sha))
    return result


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find()
    for obj in resolve_object(obj_name, gitdir):
        header, content = read_object(obj, gitdir)
        if header == "tree":
            result = ""
            tree_files = read_tree(content)
            for f in tree_files:
                result += str(f[0]).zfill(6) + " "
                result += read_object(f[2], repo_find())[0] + " "
                result += f[2] + "\t"
                result += f[1] + "\n"
            print(result)
        else:
            print(content.decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    result = []
    header, data = read_object(tree_sha, gitdir)
    for f in read_tree(data):
        if read_object(f[2], gitdir)[0] == "tree":
            tree = find_tree_files(f[2], gitdir)
            for blob in tree:
                name = f[1] + "/" + blob[0]
                result.append((name, blob[1]))
        else:
            result.append((f[1], f[2]))
    return result


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    index = data.find(b"tree")

    return data[index + 5 : index + 45]
