import pathlib
from pathlib import PosixPath
from typing import List
import logging

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
        log.debug('\n' + path.name.center(30, '-'))
        self.__get_info(path)
        log.debug(path.name.center(30, '-') + '\n')
        
    def __count(self):
        log.debug('Counting lines and characters.')
        if self.is_dir or not self.is_file or self.sufix not in self.SUFIX:
        	return
        self.characters = 0
        self.lines = 0
        with open(self.path, 'r') as file:
        	while line := file.readline():
        		self.lines += 1
        		self.characters += len(str(line))
        log.debug(f'Lines: {self.lines}, characters: {self.characters}.')
        
    def __call__(self):
    	pass

    def __get_info(self, path: PosixPath):
        log.debug(f'Get info of {path.name} ')
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
        if 'st_fstype' in dir(stats):
        	self.filesystem = stats.st_fstype
        if 'st_creator' in dir(stats):
        	self.creator = stats.st_creator
        if 'st_type' in dir(stats):
        	self.type = stats.st_type
        self.__count()
        
    def __repr__(self):
    	result =  '<'
    	if self.is_file:
    		result += 'File '
    	if self.is_dir:
    		result += 'Directory'
    	result += f'{self.name}>'
    	log.debug('File representation {result}')
    	return result

    def __str__(self):

        return f'[' \
               f'Name: {self.name}\n' \
               f'Sufix: {self.sufix}\n' \
               f'Type: {self.type}\n' \
               f'File: {self.is_file}, Dir: {self.is_dir}\n' \
               f'Size: {self.size}, Real size: {self.real_size}\n' \
               f'Platform: {self.platform}\n' \
               f'Creator: {self.creator}\n' \
               f'Created: {self.created_time}\n' \
               f'Filesystem: {self.filesystem}\n'\
               f'Lines count {self.lines}\n'\
               f'Characters count {self.characters}]\n'


class Project:
    EXCLUDE = ['__pycache__', 'venv', '.idea', '.git']

    def __init__(self, project_path: str or PosixPath, debug=False):
        log.setLevel(logging.WARNING)
        if debug:
        	log.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.debug('Project initialized.')
        self.all_files = []
        self.project = pathlib.Path(project_path)
        self.lines_count = None
        self.character_counts = None
        self.files_count = None
        self.dir_count = None

    @property
    def project(self):
        return self.__project_path

    @project.getter
    def project(self):
        log.debug('project.getter.')
        return self.__project_path

    @project.setter
    def project(self, value: PosixPath):
        log.debug(f'project.setter {value}')
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
    		print(file)
    		if file.is_file:
    			self.files_count += 1
    		if file.is_dir:
    			self.dir_count += 1
    		if file.lines:
    			self.lines_count += file.lines
    		if file.characters:
    			self.character_counts += file.characters


def get_files_path(search_path: PosixPath,
                   show_folder=True,
                   deep=True,
                   exclude: List[str] = None) -> List[PosixPath]:
    log.debug(f'get_files_path {search_path}')
    all_files = []
    for path in search_path.iterdir():
        if exclude and path.name in exclude:
            continue
        log.debug(f'Checking for {path}')
        if path.is_dir() and show_folder:
            all_files.append(File(path))
        if path.is_dir() and deep:
            all_files += get_files_path(path, exclude=exclude)
        if path.is_file():
            log.debug(f'Add file {path.name}')
            all_files.append(File(path))
    return all_files
