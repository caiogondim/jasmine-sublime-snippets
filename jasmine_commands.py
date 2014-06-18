import sublime, sublime_plugin
import re
import os
import functools

class JasmineToggleCommand(sublime_plugin.TextCommand):  
    def run(self, edit, split_view = False):
        self.settings = sublime.load_settings("JasmineCommands.sublime-settings")

        file_type = self.file_type()

        if not file_type:
            sublime.error_message("Only js files are supported")
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
            sublime.error_message("File not found")

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
            dirnames[:] = [dirname for dirname in dirnames if dirname]
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
