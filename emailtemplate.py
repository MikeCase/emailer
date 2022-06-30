from abc import ABCMeta, abstractmethod, abstractstaticmethod

from jinja2 import Environment, FileSystemLoader
from markdown import markdownFromFile

class IEmail(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, design_template, output_file):
        """ Implement in child class """

    @abstractstaticmethod
    def render_template(self, data, extra_data):
        """ Implement in child class """


class JinjaTemplate(IEmail):

    def __init__(self, design_template, output_file='email_file.html'):
        """Jinja template class for rendering jinja templates to email."""
        self.file_loader = FileSystemLoader('templates')
        self.env = Environment(loader=self.file_loader)
        self.email_template = design_template
        self.output_file = output_file
        self.template = None

    def render_template(self, data, extra_data):
        my_template = self.env.get_template(self.email_template)
        self.template = my_template.render(data=data, extra_data=extra_data)
        return self.template

    def output_html(self, data, extra_data):
        output = self.render_template(data, extra_data)
        with open(self.output_file, 'w') as outputfile:
            outputfile.writelines(output)

class MarkdownTemplate(IEmail):

    def __init__(self, design_template, output_file='email_file.html'):
        """Markdown template class for rendering markdown to html email."""
        self.email_template = design_template
        self.output_file = output_file
        self.template = None

    def render_template(self, data, extra_data):
        markdownFromFile(input=self.email_template, output=self.output_file)
        with open(self.output_file, 'r') as template:
            template = template.readlines()
            self.template = "\n".join(template)
        return self.template

    def output_html(self, data, extra_data):
        output = self.render_template(data, extra_data)

class PlainTextTemplate(IEmail):
    def __init__(self):
        pass

    def render_template(self):
        pass


class TemplateFactory:

    @staticmethod
    def build_email(template_type, *args, **kwargs):
        if template_type == 'jinja':
            return JinjaTemplate(*args, **kwargs)
        if template_type == 'markdown':
            return MarkdownTemplate(*args, **kwargs)
        print("Invalid template type")
        return -1