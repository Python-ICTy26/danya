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

    # def __init__(self, ctime_, ctime_ns, mtime_s, mtime_n, dev, ino, mode, uid, gid, size, sha1, flags, name):
    #     self.ctime_s = ctime_s
    #     self.ctime_n = ctime_n
    #     self.mtime_s = mtime_s
    #     self.mtime_n = mtime_n
    #     self.dev = dev
    #     self.ino = ino
    #     self.mode = mode
    #     self.uid = uid
    #     self.gid = gid
    #     self.size = size
    #     self.sha1 = sha1
    #     self.flags = flags
    #     self.name = name

    def pack(self) -> bytes:
        print(*self)
        return struct.pack('L3sd', *self)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        return GitIndexEntry('L3sd', *struct.unpack(data))


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    # PUT YOUR CODE HERE
    ...


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # PUT YOUR CODE HERE
    ...


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    ...


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...
