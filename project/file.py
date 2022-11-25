import pathlib
import math
import logging
import os
import time

log = logging.getLogger(__name__)


class File:
    SUFIX = ['.py', '.conf', '.config', '.json', '.css', '.xml', '.html', '.css', '.php', '.js', '.ini']

    def __init__(self, path):
        self.name = None
        self.sufix = None
        self.absolute = None
        self.is_file = None
        self.is_dir = None
        self.characters = None
        self.lines = None
        self.size = None
        self.real_size = None
        self.characters = None
        self.lines = None
        self.functions = None
        self.platform = None
        self.created_time = None
        self.last_modified = None
        self.filesystem = None
        self.creator = None
        self.type = None
        self.path = path

    @property
    def path(self):
        return self._path

    @path.getter
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        path = pathlib.Path(value)
        self._path = path
        self.__get_info(path)

    def __count(self):
        if self.is_dir or not self.is_file or self.sufix not in self.SUFIX:
            return
        self.characters = 0
        self.lines = 0
        with open(self.path, 'r') as file:
            while line := file.readline():
                self.lines += 1
                self.characters += len(str(line))

    def __call__(self):
        pass

    def __get_info(self, path):
        stats = path.stat()
        self.sufix = path.suffix
        self.name = path.name
        self.absolute = path.absolute()
        self.is_file = path.is_file()
        self.is_dir = path.is_dir()
        self.size = stats.st_size
        if 'st_rsize' in dir(stats):
            self.real_size = stats.st_rsize
        self.platform = stats.st_ino
        if 'st_birthtime' in dir(stats):
            self.created_time = stats.st_birthtime
        else:
            self.created_time = time.ctime(os.path.getctime(path))
        # self.last_modified = time.ctime(os.path.getmtime(path))
        if 'st_fstype' in dir(stats):
            self.filesystem = stats.st_fstype
        if 'st_creator' in dir(stats):
            self.creator = stats.st_creator
        if 'st_type' in dir(stats):
            self.type = stats.st_type
        self.__count()

    def __repr__(self):
        result = '<'
        if self.is_file:
            result += 'File '
        if self.is_dir:
            result += 'Directory '
        result += f'{self.name}>'
        return result

    def __str__(self):
        result = '\n['
        result += f'Name: {self.name}\n' if self.name else ''
        result += f'Sufix: {self.sufix}\n' if self.sufix else ''
        result += f'Type: {self.type}\n' if self.type else ''
        result += f'File: {self.is_file}\n' if self.is_file else ''
        result += f'Dir: {self.is_dir}\n' if self.is_dir else ''
        result += f'Size: {convert_size(self.size)}\n' if self.size else ''
        result += f'Real size: {convert_size(self.real_size)}\n' if self.real_size else ''
        result += f'Platform: {self.platform}\n' if self.platform else ''
        result += f'Creator: {self.creator}\n' if self.creator else ''
        result += f'Created: {self.created_time}\n' if self.created_time else ''
        result += f'Last modified: {self.last_modified}\n' if self.last_modified else ''
        result += f'Filesystem: {self.filesystem}\n' if self.filesystem else ''
        result += f'Lines: {self.lines}\n' if self.lines else ''
        result += f'Characters: {self.characters}\n' if self.characters else ''
        result += ']'
        return result


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
