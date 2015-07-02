#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import click

@click.group(invoke_without_command=False)
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
@click.pass_context
def cli(ctx, **kwargs):
    print ctx
    print kwargs
    for x in range(kwargs['count']):
        click.echo('Hello %s!' % kwargs['name'])
    print ctx.invoked_subcommand
    print ctx.args
    ctx.obj = {"myObj": "awsome"}
    #ctx.invoke(hello2)
    print "after invoking"
    return ctx

@cli.command()
@click.pass_context
def hello2(ctx):
    print ctx.obj
    print "hello2!!!"

@cli.command()
@click.pass_context
def initdb(ctx):
    click.echo('Initialized the database')

@cli.command()
def dropdb():
    click.echo('Dropped the database')



if __name__ == '__main__':
    cli()