# Huge thanks to RubyTests( https://github.com/maltize/sublime-text-2-ruby-tests )
import sublime, sublime_plugin
import re
import os
import functools

class JasmineToggleCommand(sublime_plugin.TextCommand):  
    def run(self, edit, split_view = False):
        self.load_settings()

        file_type = self.file_type()

        if not file_type:
            return

        possible_alternates = file_type.possible_alternate_files()
        alternates = self.project_files(lambda file: file in possible_alternates)

        for alternate in alternates:
            if re.search(file_type.parent_dir_name(), alternate):
                alternates = [alternate]
                break

        if alternates:
            if split_view:
                ShowPanels(self.window()).split()
            if len(alternates) == 1:
                self.window().open_file(alternates.pop())
            else:
                callback = functools.partial(self.on_selected, alternates)
                self.window().show_quick_panel(alternates, callback)
        else:
            SpecFileInterface(self, split_view).interact()

    def load_settings(self):
        settings = sublime.load_settings("Jasmine_BDD.sublime-settings")
        self.ignored_directories = settings.get("ignored_directories")

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

    def window(self):
        return self.view.window()

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
        return [
            self.file_name.replace("_spec.js", ".js"),
            self.file_name.replace(".spec.js", ".js")
        ]

    @classmethod
    def test(cls, file_name):
        return re.search('\w+\.spec.js', file_name) or re.search('\w+\_spec.js', file_name)


class SpecFileInterface:
    relative_paths = []
    full_torelative_paths = {}
    rel_path_start = 0

    def __init__(self, command, split_view):
        self.ignored_directories = command.ignored_directories
        self.window = command.window()
        self.current_file = command.view.file_name()
        self.split_view = split_view

    def interact(self):
        self.build_relative_paths()
        self.window.show_quick_panel(self.relative_paths, self.dir_selected)

    def build_relative_paths(self):
        folders = self.active_project(self.window.folders())
        view = self.window.active_view()
        self.relative_paths = []
        self.full_torelative_paths = {}
        # TODO: refactor!
        for path in folders:
            rootfolders = os.path.split(path)[-1]
            self.rel_path_start = len(os.path.split(path)[0]) + 1
            if self.is_valid_path(path):
                self.full_torelative_paths[rootfolders] = path
                self.relative_paths.append(rootfolders)

            for base, dirs, files in os.walk(path):
                for ignored_dir in self.ignored_directories:
                    if ignored_dir in dirs:
                        dirs.remove(ignored_dir)
                for dir in dirs:
                    relative_path = os.path.join(base, dir)[self.rel_path_start:]
                    if self.is_valid_path(relative_path):
                        self.full_torelative_paths[relative_path] = os.path.join(base, dir)
                        self.relative_paths.append(relative_path)

    def active_project(self, folders):
        for folder in folders:
            project_name = os.path.split(folder)[-1]
            if re.search(project_name, self.current_file):
                return [folder]
        return folders

    def is_valid_path(self, path):
        if not re.search("spec", self.current_file): # TODO: jasmine_path setting 
            return re.search("spec", path)
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
        if re.search("spec", self.current_file): # TODO: jasmine_path setting
            return re.sub('.spec.js|_spec.js', '.js', current_file)
        else:
            return current_file.replace('.js', '.spec.js') # TODO: file_extension setting

    def file_name_input(self, file_name):
        full_path = os.path.join(self.selected_dir, file_name)

        if os.path.lexists(full_path):
            self.window.open_file(full_path)
            return
        else:
            self.create_and_open_file(full_path)

    def create_and_open_file(self, path):
        if not os.path.exists(path):
            self.create(path)

        if self.split_view:
            ShowPanels(self.window).split()

        with open(path, 'w') as f:
            f.write("")
        view = self.window.open_file(path)
        sublime.set_timeout(lambda: view.run_command("insert_snippet", { "name": "Packages/Jasmine BDD/snippets/describe.sublime-snippet" }), 0)

    def create(self, filename):
        base, filename = os.path.split(filename)
        self.create_folder(base)

    def create_folder(self, base):
        if not os.path.exists(base):
            parent = os.path.split(base)[0]
            if not os.path.exists(parent):
                self.create_folder(parent)
            os.mkdir(base)
