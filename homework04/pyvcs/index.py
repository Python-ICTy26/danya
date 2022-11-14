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
        values = (
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            self.name.encode(),
        )
        return struct.pack(f">10i20sh{len(self.name)}s3x", *values)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        format = f">10i20sh{len(data) - 62}s"
        unpacked = struct.unpack(format, data)
        unpacked_list = list(unpacked)
        unpacked_list[-1] = unpacked_list[-1][:-3].decode()

        return GitIndexEntry(*unpacked_list)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    res: tp.List[GitIndexEntry] = []

    try:
        with open(gitdir / "index", "rb") as f:
            data = f.read()
    except:
        return res

    content = data[12:-20]
    count = 0
    for _ in range(int.from_bytes(data[8:12], "big")):
        start = count + 62
        end = content[start:].find(b"\x00\x00\x00") + start + 3
        res.append(GitIndexEntry.unpack(content[count:end]))
        count = end
    return res


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    with open(gitdir / "index", "wb") as f:
        # values = (b"DIRC", 2, len(entries))
        hash = struct.pack("!4s2i", *[b"DIRC", 2, len(entries)])
        f.write(hash)
        for entry in entries:
            f.write(entry.pack())
            hash += entry.pack()
        new_hash = str(hashlib.sha1(hash).hexdigest())
        f.write(struct.pack(f">{len(bytearray.fromhex(new_hash))}s", bytearray.fromhex(new_hash)))


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    for file in read_index(gitdir):
        if details:
            print(f"{str(oct(file.mode))[2:]} {file.sha1.hex()} 0	{file.name}")
        else:
            print(file.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    if (gitdir / "index").exists():
        files = read_index(gitdir)
    else:
        files = []
    for path in paths:
        with open(path) as f:
            f_content = f.read()
        hash = hash_object(f_content.encode(), "blob", True)
        stat = os.stat(path)
        files.append(
            GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=0,
                mtime_s=int(stat.st_mtime),
                mtime_n=0,
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                sha1=bytes.fromhex(hash),
                flags=7,
                name=str(path).replace("\\", "/"),
            )
        )
    files = sorted(files, key=lambda x: x.name)
    write_index(gitdir, files)
