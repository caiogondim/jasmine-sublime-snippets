# Huge thanks to RubyTests( https://github.com/maltize/sublime-text-2-ruby-tests )
import sublime, sublime_plugin
import re
import os
import functools

class BaseCommand(sublime_plugin.TextCommand):
    def run(self, edit, split_view = False):
        self.load_settings()
        self.create_base_spec_folder()
        self.split_view = split_view
        self._run(edit)

    def load_settings(self):
        settings = sublime.load_settings("Jasmine_BDD.sublime-settings")
        self.ignored_directories = settings.get("ignored_directories", [])
        self.jasmine_path = settings.get("jasmine_path", "spec")

    def create_base_spec_folder(self):
        base, _ = os.path.split(self.view.file_name())
        for folder in self.window().folders():
            spec_path = os.path.join(folder, self.jasmine_path)
            if re.search(folder, base) and not os.path.exists(spec_path):
                os.mkdir(spec_path)

    def window(self):
        return self.view.window()

class JasmineToggleCommand(BaseCommand):
    def _run(self, edit):
        file_type = self.file_type()
        if not file_type:
            return

        alternates = self.reduce_alternatives(file_type)
        if alternates:
            self.show_alternatives(alternates)
        else:
            SpecFileInterface(self).interact()

    def reduce_alternatives(self, file_type):
        alternates = self.project_files(lambda file: file in file_type.possible_alternate_files())
        for alternate in alternates:
            if re.search(file_type.parent_dir_name(), alternate):
                alternates = [alternate]
                break
        return alternates

    def show_alternatives(self, alternates):
        if self.split_view:
            ShowPanels(self.window()).split()
        if len(alternates) == 1:
            self.window().open_file(alternates.pop())
        else:
            callback = functools.partial(self.on_selected, alternates)
            self.window().show_quick_panel(alternates, callback)

    def file_type(self):
        file_name = self.view.file_name()
        if JasmineFile.test(file_name):
            return JasmineFile(file_name)
        elif JSFile.test(file_name):
            return JSFile(file_name)

    def on_selected(self, alternates, index):
        if index == -1:
            return
        self.window().open_file(alternates[index])

    def project_files(self, file_matcher):
        directories = self.window().folders()
        return [os.path.join(dirname, file) for directory in directories for dirname, _, files in self.walk(directory) for file in filter(file_matcher, files)]

    def walk(self, directory):
        for dir, dirnames, files in os.walk(directory):
            dirnames[:] = [dirname for dirname in dirnames if dirname not in self.ignored_directories]
            yield dir, dirnames, files

class JasmineCreateSpecCommand(BaseCommand):
    def _run(self, edit):
        SpecFileInterface(self).interact()

##
# Classes
##

class ShowPanels():
    def __init__(self, window):
        self.window = window

    def split(self):
        self.window.run_command('set_layout', {
            "cols": [0.0, 0.5, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
        })
        self.window.focus_group(1)

class BaseFile():
    def __init__(self, file_name):
        self.folder_name, self.file_name = os.path.split(file_name)
        self.absolute_path = file_name

    def parent_dir_name(self):
        head_dir, tail_dir = os.path.split(self.folder_name)
        return tail_dir

class JSFile(BaseFile):
    def possible_alternate_files(self):
        return [
            self.file_name.replace(".js", "_spec.js"),
            self.file_name.replace(".js", ".spec.js")
        ]

    @classmethod
    def test(cls, file_name):
        return re.search('\w+\.js', file_name)

class JasmineFile(BaseFile):
    def possible_alternate_files(self):
        possible_set = set([self.file_name.replace("_spec.js", ".js"), self.file_name.replace(".spec.js", ".js")])
        file_name_set = set([self.file_name])
        return list(possible_set - file_name_set)

    @classmethod
    def test(cls, file_name):
        return re.search('\w+\.spec.js', file_name) or re.search('\w+\_spec.js', file_name)

class SpecFileInterface():
    relative_paths = []
    full_torelative_paths = {}
    rel_path_start = 0

    def __init__(self, command):
        self.ignored_directories = command.ignored_directories
        self.jasmine_path = command.jasmine_path
        self.window = command.window()
        self.current_file = command.view.file_name()
        self.split_view = command.split_view

    def interact(self):
        self.build_relative_paths()
        self.window.show_quick_panel(self.relative_paths, self.dir_selected)

    def build_relative_paths(self):
        folders = self.active_project(self.window.folders())
        self.relative_paths = []
        self.full_torelative_paths = {}
        for path in folders:
            rootfolders = os.path.split(path)[-1]
            self.rel_path_start = len(os.path.split(path)[0]) + 1
            self.add_path(rootfolders, path)
            self.walk_dir_paths(path)

    def add_path(self, path_key, path_value):
        if self.is_valid_path(path_key) and self.is_valid_path(path_value):
            self.full_torelative_paths[path_key] = path_value
            self.relative_paths.append(path_key)

    def walk_dir_paths(self, path):
        for base, dirs, files in os.walk(path):
            self.remove_ignored_directories(dirs)
            for dir in dirs:
                dir_path = os.path.join(base, dir)
                relative_path = dir_path[self.rel_path_start:]
                self.add_path(relative_path, dir_path)

    def remove_ignored_directories(self, dirs):
        for ignored_dir in self.ignored_directories:
            if ignored_dir in dirs:
                dirs.remove(ignored_dir)

    def active_project(self, folders):
        for folder in folders:
            project_name = os.path.split(folder)[-1]
            if re.search(project_name, self.current_file):
                return [folder]
        return folders

    def is_valid_path(self, path):
        if not re.search(self.jasmine_path, self.current_file):
            return re.search(self.jasmine_path, path)
        return True

    def dir_selected(self, selected_index):
        if selected_index != -1:
            self.selected_dir = self.relative_paths[selected_index]
            self.selected_dir = self.full_torelative_paths[self.selected_dir]
            self.window.show_input_panel("File name", self.suggest_file_name(self.selected_dir), self.file_name_input, None, None)

    def suggest_file_name(self, path):
        current_file = os.path.split(self.current_file)[-1]
        return self.set_file_name(path, current_file)

    def set_file_name(self, path, current_file):
        if re.search(self.jasmine_path, self.current_file):
            return re.sub('.spec.js|_spec.js', '.js', current_file)
        else:
            return current_file.replace('.js', '.spec.js')

    def file_name_input(self, file_name):
        full_path = os.path.join(self.selected_dir, file_name)

        if os.path.lexists(full_path):
            self.window.open_file(full_path)
            return
        else:
            self.create_and_open_file(full_path)

    def create_and_open_file(self, path):
        if not os.path.exists(path):
            self.create_folders(path)

        if self.split_view:
            ShowPanels(self.window).split()

        with open(path, 'w') as f:
            f.write("")

        view = self.window.open_file(path)
        sublime.set_timeout(lambda: view.run_command("insert_snippet", { "name": "Packages/Jasmine BDD/snippets/describe.sublime-snippet" }), 0)

    def create_folders(self, filename):
        base, filename = os.path.split(filename)
        if not os.path.exists(base):
            parent = os.path.split(base)[0]
            if not os.path.exists(parent):
                self.create_folders(parent)
            os.mkdir(base)
