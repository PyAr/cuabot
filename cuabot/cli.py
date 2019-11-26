import click
import yaml
from cuabot.cuabot import CUABot

@click.group()
def cli():
    pass

@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
def run(config_file):
    with open(config_file, 'rt', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    cuabot = CUABot(config)
    cuabot.run()

@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.argument('qr_file', type=click.Path())
def generate_qr(config_file, qr_file):
    with open(config_file, 'rt', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    cuabot = CUABot(config)
    bot_url = cuabot.generate_qr(qr_file)
    click.echo('QR generated on file: {0} - Bot url: {1}'.format(qr_file, bot_url))

@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
def list_commands(config_file):
    with open(config_file, 'rt', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    cuabot = CUABot(config)
    click.echo('Enter these commands in BotFather:')
    click.echo(cuabot.get_commands())

@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
def show_schedule(config_file):
    with open(config_file, 'rt', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    cuabot = CUABot(config)
    click.echo(cuabot.show_schedule())

