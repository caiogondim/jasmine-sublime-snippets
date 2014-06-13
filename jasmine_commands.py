import sublime, sublime_plugin

class JasmineToggleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.settings = sublime.load_settings("JasmineCommands.sublime-settings")
