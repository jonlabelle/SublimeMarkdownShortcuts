# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import re
import sublime
import sublime_plugin


ORDER_LIST_PATTERN = re.compile(r'(\s*)(\d+)(\.\s+)\S+')
UNORDER_LIST_PATTERN = re.compile(r'(\s*[-+**]+)(\s+)\S+')
EMPTY_LIST_PATTERN = re.compile(r'(\s*([-+**]|\d+\.+))\s+$')


class BaseTextCommand(sublime_plugin.TextCommand):

    def run(self, edit, **kwargs):
        regions = self.view.sel()

        if any(map(lambda reg: reg.empty(), regions)):
            regions = [sublime.Region(0, self.view.size())]
        for region in regions:
            text = self.view.substr(region)
            replacement = self.transform(text, **kwargs)
            self.view.replace(edit, region, replacement)

    def should_show_plugin(self):
        view = self.view
        filename = view.file_name()
        if not filename:
            return False
        scopename = view.scope_name(0)
        if scopename.startswith('text.html.markdown') or filename.endswith('.md') or filename.endswith('.markdown'):
            return True
        return False

    def is_visible(self):
        return self.should_show_plugin()

    def is_enabled(self):
        return self.should_show_plugin()


class BoldTextCommand(BaseTextCommand):

    @staticmethod
    def transform(text):
        if len(text) > 3 and text[0:2] == '**' and text[len(text) - 2:len(text)] == '**':
            return text[2:len(text) - 2]
        else:
            return '**' + text + '**'


class ItalicTextCommand(BaseTextCommand):

    @staticmethod
    def transform(text):
        if len(text) > 1 and text[0:1] == '_' and text[len(text) - 1:len(text)] == '_':
            return text[1:len(text) - 1]
        else:
            return '_' + text + '_'


class DeletedTextCommand(BaseTextCommand):

    @staticmethod
    def transform(text):
        if len(text) > 3 and text[0:2] == '~~' and text[len(text) - 2:len(text)] == '~~':
            return text[2:len(text) - 2]
        else:
            return '~~' + text + '~~'


class Heading2TextCommand(BaseTextCommand):

    @staticmethod
    def transform(text):
        if text[0:2] == '# ':
            return '#' + text
        if text[0:3] == '## ':
            return text[3:len(text)]
        if text[0:4] == '### ':
            return text[1:len(text)]
        if text[0:5] == '#### ':
            return '#' + text[3:len(text)]
        if text[0:2] != '# ' and text[0:3] != '## ' and text[0:4] != '### ' and text[0:5] != '#### ':
            return '## ' + text


class Heading3TextCommand(BaseTextCommand):

    @staticmethod
    def transform(text):
        if text[0:2] == '# ':
            return '##' + text
        if text[0:3] == '## ':
            return '#' + text
        if text[0:4] == '### ':
            return text[4:len(text)]
        if text[0:5] == '#### ':
            return '#' + text[3:len(text)]
        if text[0:2] != '# ' and text[0:3] != '## ' and text[0:4] != '### ' and text[0:5] != '#### ':
            return '### ' + text


class Heading4TextCommand(BaseTextCommand):

    @staticmethod
    def transform(text):
        if text[0:2] == '# ':
            return '###' + text
        if text[0:3] == '## ':
            return '##' + text
        if text[0:4] == '### ':
            return '#' + text
        if text[0:5] == '#### ':
            return text[5:len(text)]
        if text[0:2] != '# ' and text[0:3] != '## ' and text[0:4] != '### ' and text[0:5] != '#### ':
            return '#### ' + text


class SmartListCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            line_region = self.view.line(region)

            # the content before point at the current line
            before_point_region = sublime.Region(line_region.a, region.a)
            before_point_content = self.view.substr(before_point_region)

            # Disable smart list when folded
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

    def should_show_plugin(self):
        view = self.view
        filename = view.file_name()
        if not filename:
            return False
        scopename = view.scope_name(0)
        if scopename.startswith('text.html.markdown') or filename.endswith('.md') or filename.endswith('.markdown'):
            return True
        return False

    def is_visible(self):
        return self.should_show_plugin()

    def is_enabled(self):
        return self.should_show_plugin()
