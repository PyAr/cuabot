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





if __name__ == "__main__":
    cli()