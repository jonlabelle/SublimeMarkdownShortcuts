# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import re
import sublime
import sublime_plugin


ORDER_LIST_PATTERN = re.compile(r'(\s*)(\d+)(\.\s+)\S+')
UNORDER_LIST_PATTERN = re.compile(r'(\s*[-+**]+)(\s+)\S+')
EMPTY_LIST_PATTERN = re.compile(r'(\s*([-+**]|\d+\.+))\s+$')


class BoldCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        selection = self.view.sel()
        for region in selection:
            region_text = self.view.substr(region)
            if len(region_text) > 3 and region_text[0:2] == '**' and region_text[len(region_text) - 2:len(region_text)] == '**':
                self.view.replace(edit, region, region_text[2:len(region_text) - 2])
            else:
                self.view.replace(edit, region, '**' + region_text + '**')


class ItalicCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        selection = self.view.sel()
        for region in selection:
            region_text = self.view.substr(region)
            if len(region_text) > 1 and region_text[0:1] == '_' and region_text[len(region_text) - 1:len(region_text)] == '_':
                self.view.replace(edit, region, region_text[1:len(region_text) - 1])
            else:
                self.view.replace(edit, region, '_' + region_text + '_')


class DeletedCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        selection = self.view.sel()
        for region in selection:
            region_text = self.view.substr(region)
            if len(region_text) > 3 and region_text[0:2] == '~~' and region_text[len(region_text) - 2:len(region_text)] == '~~':
                self.view.replace(edit, region, region_text[2:len(region_text) - 2])
            else:
                self.view.replace(edit, region, '~~' + region_text + '~~')


class SmartListCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            line_region = self.view.line(region)

            # the content before point at the current line.
            before_point_region = sublime.Region(line_region.a, region.a)
            before_point_content = self.view.substr(before_point_region)

            # Disable smart list when folded.
            folded = False
            for i in self.view.folded_regions():
                if i.contains(before_point_region):
                    self.view.insert(edit, region.a, '\n')
                    folded = True
            if folded:
                break

            match = EMPTY_LIST_PATTERN.match(before_point_content)
            if match:
                self.view.erase(edit, before_point_region)
                break

            match = ORDER_LIST_PATTERN.match(before_point_content)
            if match:
                insert_text = match.group(1) + str(int(match.group(2)) + 1) + match.group(3)
                self.view.insert(edit, region.a, '\n' + insert_text)
                break

            match = UNORDER_LIST_PATTERN.match(before_point_content)
            if match:
                insert_text = match.group(1) + match.group(2)
                self.view.insert(edit, region.a, '\n' + insert_text)
                break

            self.view.insert(edit, region.a, '\n')

        self.adjust_view()

    def adjust_view(self):
        for region in self.view.sel():
            self.view.show(region)


class Heading2Command(sublime_plugin.TextCommand):

    def run(self, edit):
        region = self.view.line(self.view.sel()[0])
        current_line_text = self.view.substr(region)

        if current_line_text[0:2] == '# ':
            self.view.replace(edit, region, '#' + current_line_text)
        if current_line_text[0:3] == '## ':
            self.view.replace(edit, region, current_line_text[3:len(current_line_text)])
        if current_line_text[0:4] == '### ':
            self.view.replace(edit, region, current_line_text[1:len(current_line_text)])
        if current_line_text[0:5] == '#### ':
            self.view.replace(edit, region, '#' + current_line_text[3:len(current_line_text)])
        if current_line_text[0:2] != '# ' and current_line_text[0:3] != '## ' and current_line_text[0:4] != '### ' and current_line_text[0:5] != '#### ':
            self.view.replace(edit, region, '## ' + current_line_text)


class Heading3Command(sublime_plugin.TextCommand):

    def run(self, edit):
        region = self.view.line(self.view.sel()[0])
        current_line_text = self.view.substr(region)

        if current_line_text[0:2] == '# ':
            self.view.replace(edit, region, '##' + current_line_text)
        if current_line_text[0:3] == '## ':
            self.view.replace(edit, region, '#' + current_line_text)
        if current_line_text[0:4] == '### ':
            self.view.replace(edit, region, current_line_text[4:len(current_line_text)])
        if current_line_text[0:5] == '#### ':
            self.view.replace(edit, region, '#' + current_line_text[3:len(current_line_text)])
        if current_line_text[0:2] != '# ' and current_line_text[0:3] != '## ' and current_line_text[0:4] != '### ' and current_line_text[0:5] != '#### ':
            self.view.replace(edit, region, '### ' + current_line_text)


class Heading4Command(sublime_plugin.TextCommand):

    def run(self, edit):
        region = self.view.line(self.view.sel()[0])
        current_line_text = self.view.substr(region)

        if current_line_text[0:2] == '# ':
            self.view.replace(edit, region, '###' + current_line_text)
        if current_line_text[0:3] == '## ':
            self.view.replace(edit, region, '##' + current_line_text)
        if current_line_text[0:4] == '### ':
            self.view.replace(edit, region, '#' + current_line_text)
        if current_line_text[0:5] == '#### ':
            self.view.replace(edit, region, current_line_text[5:len(current_line_text)])
        if current_line_text[0:2] != '# ' and current_line_text[0:3] != '## ' and current_line_text[0:4] != '### ' and current_line_text[0:5] != '#### ':
            self.view.replace(edit, region, '#### ' + current_line_text)
