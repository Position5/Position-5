# Position-5

[![Pylint](https://github.com/appi147/Position-5/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/appi147/Position-5/actions/workflows/pylint.yml)

Dedicated to best position 5 support.

## Setting Up

- Install Python 3.8+
- Install `poetry`
- Install dependencies: `poetry install`
- Create a `.env` file in root directory, and place following tokens:
```
DISCORD_BOT_TOKEN=token-goes-here
CRIC_API=token-goes-here
REDDIT_ID=token-goes-here
REDDIT_SECRET=token-goes-here
```

### Linting

Use `poetry` to lint and format code:

- `poetry run pylint position5`
- `poetry run black position5`

### Run the bot

Poetry automatically runs on virtualenv

- `poetry run py position5`
