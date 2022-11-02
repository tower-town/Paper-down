import pytest
from paper.parse import parse
import click

class TestParse():
    def test_parse(self):
        @cloup.command()
        @cloup.pass_context()
        def invoke_parse(ctx):
            ctx.invoke(parse, path="..\down.txt")
        
        invoke_parse()