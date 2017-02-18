from textwrap import dedent, indent

import sphinx.application
from docutils.parsers.rst import Directive
from docutils import nodes
from docutils.statemachine import StringList
from sphinx.util.nodes import nested_parse_with_titles

from borg_import.main import build_parser


class GenerateUsageDirective(Directive):
    required_arguments = 1
    has_content = False

    @staticmethod
    def _get_command_parser(parser, command):
        for action in parser._actions:
            if action.choices is not None and 'SubParsersAction' in str(action.__class__):
                return action.choices[command]
        raise ValueError('No parser for %s found' % command)

    def write_options_group(self, group, contents, with_title=True):
        def is_positional_group(group):
            return any(not o.option_strings for o in group._group_actions)

        def get_help(option):
            text = dedent((option.help or '') % option.__dict__)
            return '\n'.join('| ' + line for line in text.splitlines())

        def shipout(text):
            for line in text:
                contents.append(indent(line, ' ' * 4))

        if not group._group_actions:
            return

        if with_title:
            contents.append(group.title)
        text = []

        if is_positional_group(group):
            for option in group._group_actions:
                text.append(option.metavar)
                text.append(indent(option.help or '', ' ' * 4))
            shipout(text)
            return

        options = []
        for option in group._group_actions:
            if option.metavar:
                option_fmt = '``%%s %s``' % option.metavar
            else:
                option_fmt = '``%s``'
            option_str = ', '.join(option_fmt % s for s in option.option_strings)
            options.append((option_str, option))
        for option_str, option in options:
            help = indent(get_help(option), ' ' * 4)
            text.append(option_str)
            text.append(help)

        text.append("")
        shipout(text)

    def run(self):
        command = self.arguments[0]
        parser = self._get_command_parser(build_parser(), command)

        full_command = 'borg-import ' + command
        headline = '::\n\n    ' + full_command

        if any(len(o.option_strings) for o in parser._actions):
            headline += ' <options>'

        # Add the metavars of the parameters to the synopsis line
        for option in parser._actions:
            if not option.option_strings:
                headline += ' ' + option.metavar

        headline += '\n\n'

        # Final result will look like:
        # borg-import something <options> FOO_BAR REPOSITORY
        contents = headline.splitlines()

        for group in parser._action_groups:
            self.write_options_group(group, contents)

        if parser.epilog:
            contents.append('Description')
            contents.append('~~~~~~~~~~~')
            contents.append('')

        node = nodes.paragraph()
        nested_parse_with_titles(self.state, StringList(contents), node)
        gen_nodes = [node]

        if parser.epilog:
            paragraphs = parser.epilog.split('\n\n')
            for paragraph in paragraphs:
                node = nodes.paragraph()
                nested_parse_with_titles(self.state, StringList(paragraph.split('\n')), node)
                gen_nodes.append(node)

        return gen_nodes


def setup(app: sphinx.application.Sphinx):
    app.add_directive('generate-usage', GenerateUsageDirective)
