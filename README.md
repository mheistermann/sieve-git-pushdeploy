# Sieve git push deployment

## Introduction

Keep your sieve scripts in a git repos (e.g. on your mailserver), push
to them to deploy a new version.

Warning: experimental, use at your own risk. Probably quite buggy, just hacked
this together quickly.


## Installation without pip

```
virtualenv -p python2 .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Copy the provided example copy to `~/.config/sieve-git-pushdeploy/sieve.conf`
and adjust the values.

Somewhere,
```
git init --bare sieve.git
cd sieve.git/hooks
ln -s path/to/sieve-git-pushdeploy/.venv/bin/sieve-git-pushdeploy post-receive
```
Now you can clone that repo and push your configs to it, they will be checked
and uploaded automatically.

## License

sieve-git-pushdeploy was written by Martin Heistermann <github()mheistermann.de>
and is available under the terms of the GPL v3.

## Ideas

* when checkscript() fails, report the error - need to improve sievelib
* Proper installation with pip?
* Option to reject pushes with invalid syntax?
* Colored output that stands out from the rest of the git output
* Update sievelib to Python3, use Python3


## Contributing

Send me a pull request on github or [email me a patch](mailto:github[]mheistermann.de).

