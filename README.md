# Sieve git push deployment
[![Build Status](https://travis-ci.org/mheistermann/sieve-git-pushdeploy.svg?branch=master)](https://travis-ci.org/mheistermann/sieve-git-pushdeploy)

## Introduction

Keep your sieve scripts in a git repos (e.g. on your mailserver), push
to them to deploy a new version.

Warning: experimental, use at your own risk. Probably quite buggy, just hacked
this together quickly.

## Installation

### Installation with pip

```pip3 install sieve-git-pushdeploy
HOOK=/usr/local/bin/sieve_git_pushdeploy
```

### Installation without pip

```
virtualenv -p python2 .venv
source .venv/bin/activate
pip install -r requirements.txt
HOOK=$(pwd)/.venv/bin/sieve_git_pushdeploy
```
Copy the provided example copy to `~/.config/sieve-git-pushdeploy/sieve.conf`
and adjust the values.

### Setup a sieve repository

Somewhere,
```
git init --bare sieve.git
cd sieve.git/hooks
ln -s $HOOK update
```
You can also opt to only use a subset of the hooks.

Now if you clone that repo and push your configs to it, they will be checked
and uploaded automatically.

## License

sieve-git-pushdeploy was written by Martin Heistermann <github()mheistermann.de>
and is available under the terms of the GPL v3.

## Ideas

* Colored output that stands out from the rest of the git output


## Contributing

Send me a pull request on github or [email me a patch](mailto:github[]mheistermann.de).

