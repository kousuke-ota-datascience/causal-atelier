"""Private Linux directory capabilities for local scientific runs."""
from __future__ import annotations

import ctypes
import os
import stat
import sys
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

from ariadne.shared.content_ref import ContractViolation, safe_relative_key

_DIR = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
_FILE = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC
_LIBC = ctypes.CDLL(None, use_errno=True)
_LOCAL_FS = {0xEF53, 0x58465342}


def _filesystem(fd: int) -> int:
    buffer = (ctypes.c_long * 64)()
    if _LIBC.fstatfs(fd, ctypes.byref(buffer)) != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))
    return buffer[0]


def _security(message: str) -> ContractViolation:
    return ContractViolation("INPUT_SECURITY", "input", message)


def _open_absolute(path: Path) -> int:
    fd = os.open("/", _DIR)
    try:
        for component in path.parts[1:]:
            child = os.open(component, _DIR, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


@dataclass(frozen=True)
class LocalPrincipal:
    uid: int

    @classmethod
    def current(cls) -> LocalPrincipal:
        uid = os.geteuid()
        if uid == 0:
            raise _security("Local execution requires a non-root effective UID")
        return cls(uid)


@dataclass(frozen=True)
class VerifiedRootIdentity:
    device: int
    inode: int
    owner_uid: int
    mode: int
    filesystem: int
    capability: object = field(repr=False)


@dataclass(frozen=True, init=False, eq=False)
class TrustedLocalRoot:
    _path: Path
    _fd: int
    _identity: VerifiedRootIdentity

    @classmethod
    def open(cls, path: Path, *, allowed_directory: Path) -> TrustedLocalRoot:
        path, allowed = Path(path), Path(allowed_directory)
        if (
            sys.platform != "linux" or not path.is_absolute() or not allowed.is_absolute()
            or ".." in path.parts or ".." in allowed.parts or not path.is_relative_to(allowed)
        ):
            raise _security("Root must be confined to the configured local directory")
        fd = None
        try:
            fd = _open_absolute(path)
            identity = cls._facts(fd, object())
            root = object.__new__(cls)
            object.__setattr__(root, "_path", path)
            object.__setattr__(root, "_fd", fd)
            object.__setattr__(root, "_identity", identity)
            fd = None
            return root
        except OSError as error:
            raise _security("Unable to verify the local root") from error
        finally:
            if fd is not None:
                os.close(fd)

    @staticmethod
    def _facts(fd: int, capability: object) -> VerifiedRootIdentity:
        info = os.fstat(fd)
        filesystem = _filesystem(fd)
        mode = stat.S_IMODE(info.st_mode)
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != LocalPrincipal.current().uid or mode != 0o700:
            raise _security("Root ownership or private directory mode is invalid")
        if filesystem not in _LOCAL_FS:
            raise _security("Root filesystem must be local ext4 or XFS")
        return VerifiedRootIdentity(info.st_dev, info.st_ino, info.st_uid, mode, filesystem, capability)

    def verify(self) -> VerifiedRootIdentity:
        try:
            current = self._facts(self._fd, self._identity.capability)
            fd = _open_absolute(self._path)
            try:
                named = self._facts(fd, self._identity.capability)
            finally:
                os.close(fd)
        except OSError as error:
            raise _security("Root directory capability is unavailable") from error
        if current != self._identity or named != current:
            raise _security("Root directory identity changed")
        return current

    def fileno(self) -> int:
        self.verify()
        return self._fd

    def close(self) -> None:
        if self._fd >= 0:
            fd = self._fd
            object.__setattr__(self, "_fd", -1)
            os.close(fd)

    def __enter__(self) -> TrustedLocalRoot:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()


def _check_fd(fd: int, identity: VerifiedRootIdentity, *, directory: bool) -> os.stat_result:
    info = os.fstat(fd)
    mode, kind = (0o700, stat.S_ISDIR) if directory else (0o600, stat.S_ISREG)
    if (
        not kind(info.st_mode) or stat.S_IMODE(info.st_mode) != mode or info.st_uid != identity.owner_uid
        or info.st_dev != identity.device or _filesystem(fd) != identity.filesystem
        or (not directory and info.st_nlink != 1)
    ):
        raise _security("File or directory is outside the approved private filesystem boundary")
    return info


@contextmanager
def private_directory(parent: int, key: str, identity: VerifiedRootIdentity, *, create: bool = False):
    if not safe_relative_key(key) or "/" in key:
        raise _security("Invalid directory component")
    if create:
        try:
            os.mkdir(key, 0o700, dir_fd=parent)
        except FileExistsError:
            pass
    fd = os.open(key, _DIR, dir_fd=parent)
    try:
        _check_fd(fd, identity, directory=True)
        yield fd
    finally:
        os.close(fd)


def _stamp(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_uid, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def read_private_file(parent: int, key: str, identity: VerifiedRootIdentity) -> bytes:
    if not safe_relative_key(key) or "/" in key:
        raise _security("Invalid file component")
    fd = os.open(key, _FILE, dir_fd=parent)
    try:
        before = _check_fd(fd, identity, directory=False)
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read()
        after = _check_fd(fd, identity, directory=False)
        named = os.stat(key, dir_fd=parent, follow_symlinks=False)
        if _stamp(before) != _stamp(after) or _stamp(after) != _stamp(named) or len(data) != before.st_size:
            raise _security("File identity or size changed during the read")
        return data
    finally:
        os.close(fd)


def read_relative(root: TrustedLocalRoot, key: str) -> bytes:
    from contextlib import ExitStack

    if not safe_relative_key(key):
        raise _security("Invalid relative content key")
    identity = root.verify()
    directories, filename = key.split("/")[:-1], key.split("/")[-1]
    with ExitStack() as stack:
        parent = root.fileno()
        opened = []
        for component in directories:
            child = stack.enter_context(private_directory(parent, component, identity))
            opened.append((parent, component, child))
            parent = child
        data = read_private_file(parent, filename, identity)
        for ancestor, component, child in reversed(opened):
            named = os.stat(component, dir_fd=ancestor, follow_symlinks=False)
            if _stamp(named) != _stamp(_check_fd(child, identity, directory=True)):
                raise _security("Directory identity changed during the read")
        if root.verify() != identity:
            raise _security("Root identity changed during the read")
        return data
