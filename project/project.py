from .file import File
import pathlib
from pathlib import PosixPath
from typing import List
import logging

log = logging.getLogger(__name__)


class Project:
    EXCLUDE = ['__pycache__', 'venv', '.idea', '.git', '.gitignore']

    def __init__(self, project_path: str or PosixPath, debug=False):
        log.setLevel(logging.WARNING)
        if debug:
            log.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        # formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.debug('Project initialized.')
        self.all_files = []
        self.lines_count = None
        self.character_counts = None
        self.files_count = None
        self.dir_count = None
        self.project = pathlib.Path(project_path)

    @property
    def project(self):
        return self.__project_path

    @project.getter
    def project(self):
        return self.__project_path

    @project.setter
    def project(self, value: PosixPath):
        self.all_files = get_files_path(value, exclude=self.EXCLUDE)
        self.__count()
        self.__project_path = value

    def __iter__(self):
        return self.all_files.__iter__()

    def __count(self):
        self.lines_count = 0
        self.character_counts = 0
        self.files_count = 0
        self.dir_count = 0
        for file in self.all_files:
            if file.is_file:
                self.files_count += 1
            if file.is_dir:
                self.dir_count += 1
            if file.lines:
                self.lines_count += file.lines
            if file.characters:
                self.character_counts += file.characters

    def __repr__(self):
        result = f'Files: {self.files_count}\n' \
                 f'Dirs: {self.dir_count}\n' \
                 f'Lines: {self.lines_count}\n' \
                 f'Characters: {self.character_counts}'
        return result


def get_files_path(search_path: PosixPath,
                   show_folder=True,
                   deep=True,
                   exclude: List[str] = None) -> List[File]:
    all_files = []
    for path in search_path.iterdir():
        if exclude and path.name in exclude:
            continue
        if path.is_dir() and show_folder:
            all_files.append(File(path))
        if path.is_dir() and deep:
            all_files += get_files_path(path, exclude=exclude)
        if path.is_file():
            all_files.append(File(path))
    return all_files
