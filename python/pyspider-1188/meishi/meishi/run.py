
import os
import click
import six

import meishi
from meishi.libs import utils


def read_config(ctx, param, value):
    if not value:
        return {}
    import json

    def underline_dict(d):
        if not isinstance(d, dict):
            return d
        return dict((k.replace('-', '_'), underline_dict(v)) for k, v in six.iteritems(d))

    config = underline_dict(json.load(value))
    ctx.default_map = config
    return config

@click.group(invoke_without_command=True)
@click.option('-c', '--config', callback=read_config, type=click.File('r'),
              help='a json file with default values for subcommands. {"webui": {"port":5001}}')
@click.option('--logging-config', default=os.path.join(os.path.dirname(__file__), "logging.conf"),
              help="logging config file for built-in python logging module", show_default=True)
@click.option('--db-host', default='127.0.0.1', help="db host ip, default: locahost")
@click.option('--db-user', default='v1188', help="db user")
@click.option('--db-pass', default='v1188ys', help='db password')
@click.option('--db-name', default='meishi1188', help='db name, default: meishi1188')
@click.version_option(version=meishi.__version__, prog_name=meishi.__name__)
@click.pass_context
def cli(ctx, **kwargs):
    # save args to obj
    ctx.obj = utils.ObjectDict(ctx.obj or {})
    ctx.obj['instances'] = []
    ctx.obj.update(kwargs)

    if ctx.invoked_subcommand is None:
        ctx.invoke(all)
    return ctx

@cli.command()
@click.pass_context
def all(ctx):
    ctx.invoke(importdb)
    ctx.invoke(download)

@cli.command()
@click.pass_context
def importdb(ctx):
    ctx.invoke(recipe)
    ctx.invoke(category)
    ctx.invoke(collection)
    ctx.invoke(material)
    ctx.invoke(relations)

@cli.command()
@click.pass_context
def download(ctx):
    from main.download import start
    start(ctx.obj)


@click.pass_context
def recipe(ctx):
    from main.recipe import start
    start(ctx.obj)

@click.pass_context
def category(ctx):
    from main.category import start
    start(ctx.obj)

@click.pass_context
def collection(ctx):
    from main.collection import start
    start(ctx.obj)

@click.pass_context
def material(ctx):
    from main.material import start
    start(ctx.obj)

@click.pass_context
def relations(ctx):
    from main.relations import start
    start(ctx.obj)


def main():
    cli()

if __name__ == '__main__':
    main()