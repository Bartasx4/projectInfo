import pathlib
from pathlib import PosixPath
from typing import List
import logging

log = logging.getLogger(__name__)


class File:

    def __init__(self, path):
        self.path = path
        self.name = None
        self.absolute = None
        self.is_file = None
        self.is_dir = None
        self.size = None
        self.real_size = None
        self.characters = None
        self.lines = None
        self.functions = None
        self.platform = None
        self.created_time = None
        self.filesystem = None
        self.creator = None
        self.type = None

    @property
    def path(self):
        return self._path

    @path.getter
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def __get_info(self, path: PosixPath):
        stats = path.stat()
        self.name = path.name
        self.absolute = path.absolute()
        self.is_file = path.is_file()
        self.is_dir = path.is_dir()
        self.size = stats.st_size
        self.real_size = stats.st_rsize
        self.platform = stats.st_ino
        self.created_time = stats.st_birthtime
        self.filesystem = stats.st_fstype
        self.creator = stats.st_creator
        self.type = stats.st_type

    def __str__(self):
        return f'File {self.path}\n' \
               f'Name: {self.name}\n' \
               f'Absolute: {self.absolute}\n' \
               f'Type: {self.type}' \
               f'File: {self.is_file}, Dir: {self.is_dir}\n' \
               f'Size: {self.size}, Real size: {self.real_size}\n' \
               f'Platform: {self.platform}\n' \
               f'Creator: {self.creator}\n' \
               f'Created: {self.created_time}\n' \
               f'Filesystem: {self.filesystem}\n'


class Project:
    EXCLUDE = ['__pycache__', 'venv', '.idea', '.git']

    def __init__(self, project_path: str or PosixPath):
        log.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.debug('Project initialized.')
        self.all_files = []
        self.project = pathlib.Path(project_path)

    @property
    def project(self):
        return self.__project_path

    @project.getter
    def project(self):
        log.debug('project.getter.')
        return self.__project_path

    @project.setter
    def project(self, value: PosixPath):
        log.debug(f'project.setter {value=}')
        self.all_files = get_files_path(value, exclude=self.EXCLUDE)
        self.__project_path = value


def get_files_path(search_path: PosixPath,
                   show_folder=False,
                   deep=True,
                   exclude: List[str] = None) -> List[PosixPath]:
    log.debug(f'get_files_path {search_path=}')
    all_files = []
    for path in search_path.iterdir():
        if exclude and path.name in exclude:
            continue
        log.debug(f'Checking for {path=}')
        if path.is_dir() and show_folder:
            all_files.append(path)
        if path.is_dir() and deep:
            all_files += get_files_path(path, exclude=exclude)
        if path.is_file():
            log.debug(f'Add file{path.name}')
            all_files.append(path)
    return all_files
