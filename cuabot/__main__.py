import click
import yaml
from cuabot.cuabot import CUABot


@click.group()
def cli():
    pass

@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
def run(config_file):
    with open(config_file, "rt", encoding='utf-8') as f:
        config = yaml.safe_load(f)
    cuabot = CUABot(config)
    cuabot.run()

@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.argument('qr_file', type=click.Path())
def generate_qr(config_file, qr_file):
    with open(config_file, "rt", encoding='utf-8') as f:
        config = yaml.safe_load(f)
    cuabot = CUABot(config)
    bot_url = cuabot.generate_qr(qr_file)
    click.echo("QR generated on file: %s - Bot url: %s" % (qr_file, bot_url))





if __name__ == "__main__":
    cli()