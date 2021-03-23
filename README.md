# Position-5

[![Pylint](https://github.com/appi147/Position-5/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/appi147/Position-5/actions/workflows/pylint.yml)

Dedicated to best position 5 support.

## Setting Up

- Install Python 3.5+
- Install pip packages: `pip install -r requirements.txt`
- Create a `.env` file in this directory, and place token `DISCORD_BOT_TOKEN=token-goes-here`
	and place cricapi token `CRIC_API=token-goes-here`
- Run `python position5`

### Linting

Use `pylint` and `black`:

- `python -m pylint position5`
- `python -m black -S --check position5`
