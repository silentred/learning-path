#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import click

@click.command
def hello():
    click.echo("hello world")