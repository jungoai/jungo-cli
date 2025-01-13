<div align="center">

# Jungoai CLI <!-- omit in toc -->
[![Discord Chat](https://img.shields.io/discord/308323056592486420.svg)](https://discord.gg/todo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 
<!-- [![PyPI version](https://badge.fury.io/py/bittensor_cli.svg)](https://badge.fury.io/py/bittensor_cli) -->

---

</div>

## installation

[Install rye](https://rye.astral.sh/guide/installation/):

```bash
curl -sSf https://rye.astral.sh/get | bash
```

Then install Jungo-cli via `rye`:

``` bash
rye install jungo-cli --git https://github.com/jungoai/jungo-cli.git
```

## Verify the installation

```bash
jucli --version
```

The above command will show you the version of the `jucli` you just installed.

---

## Configuration

You can set the commonly used values, such as your hotkey and coldkey names, the default chain URL or the network name you use, and more, in `config.yml`. You can override these values by explicitly passing them in the command line for any `jucli` command.

### Example config file

The default location of the config file is: `~/.jungoai/config.yml`. An example of a `config.yml` is shown below:

```yaml
chain: ws://127.0.0.1:9945
network: local
no_cache: False
wallet_hotkey: hotkey-user1
wallet_name: coldkey-user1
wallet_path: ~/.jungoai/wallets
metagraph_cols:
  ACTIVE: true
  AXON: true
  COLDKEY: true
  CONSENSUS: true
  DIVIDENDS: true
  EMISSION: true
  HOTKEY: true
  INCENTIVE: true
  RANK: true
  STAKE: true
  TRUST: true
  UID: true
  UPDATED: true
  VAL: true
  VTRUST: true
```

**For more help:**

```bash
jucli config --help
```

---

## License
The MIT License (MIT)
Copyright © 2024 The Opentensor Foundation

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
