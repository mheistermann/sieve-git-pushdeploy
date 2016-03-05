#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2016 Martin Heistermann <github[]mheistermann.de>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import logging
import configparser
import subprocess
from managesieve3 import Managesieve


CONFIG_FILENAME = "~/.config/sieve-git-pushdeploy/sieve.conf"

class MessageException(Exception):
    def __init__(self, message):
        super(MessageException, self).__init__(self, message)
        self.message = message

class ConfigError(MessageException):
    pass


class SieveError(MessageException):
    pass


def read_config(git_path):
    defaults = {
        "scriptname": "main",
        "file": "main.sieve",
        "branch": "refs/heads/master",
    }
    config = configparser.SafeConfigParser(defaults)
    config_path = os.path.expanduser(CONFIG_FILENAME)
    with open(config_path) as fp:
        config.readfp(fp)
    if git_path not in config.sections():
        raise ConfigError("Section [{}] missing".format(git_path))

    conf = {k: config.get(git_path, k) for k in [
        "host", "user", "pass", "file", "scriptname", "branch"]}

    return conf


def get_script(refname, filename):
    try:
        content =  subprocess.check_output(["git", "show",
                                            refname + ":" + filename])
        return content.decode('utf-8') # for managesieve3 API
    except subprocess.CalledProcessError:
        raise ConfigError("Can't find file '{}' in '{}'".format(
            filename, refname))


def connect(config):
    conn = Managesieve(config["host"])
    # TODO 2016-03-05:
    # when a new version of managesieve3 is released that supports cert_reqs,
    # update this to make sure the cert gets verified.
    #conn.cmd_starttls()
    conn.login_plain(username=config["user"],
                     authuser=config["user"],
                     password=config["pass"])
#        raise SieveError(
#                ("Login unsuccessful for %(user)s:***@%(host)s," +
#                 " starttls=%(starttls)s, authmech=%(authmech)s") % config)
    logging.info("current scripts; %s", conn.cmd_listscripts())
    return conn


def hook_update(config, branch, old_hash, new_hash):
    """Check sieve script validity, reject updates with invalid scripts."""
    script = get_script(new_hash, config["file"])
    conn = connect(config)

    is_okay, code, text = conn.cmd_checkscript(script)
    if not is_okay:
        raise SieveError("script invalid.: {}: {}".format(code, text))

    if branch == config["branch"]:
        conn.cmd_putscript(config["scriptname"], script)
        conn.cmd_setactive(config["scriptname"])
        print("Successfully uploaded sieve script.")
        return 0
    print("not uploading script in non-deployment branch {}".format(branch))
    return 0

hooks = {
    'update': hook_update,
    }

def usage():
    print("Usage: call this script with no arguments by symlinking" +
          " it from .git/hooks/ (argv[0] must be the hook name)")
    print("Implemented hooks:")
    for name, func in hooks.items():
        print("{}: {}".format(name, func.__doc__))


def main():
    name = os.path.split(sys.argv[0])[-1]
    hook_args = sys.argv[1:]

    try:
        hook = hooks[name]
    except KeyError:
        print("Can't handle hook '{}'.".format(name))
        usage()
        sys.exit(1)

    git_path = os.getcwd()
    config = read_config(git_path)
    logging.debug("config: {}", config)

    try:
        retval = hook(config, *hook_args)
    except (ConfigError, SieveError) as e:
        logging.error(e.message)
        retval = 1
    sys.exit(retval)


if __name__ == "__main__":
    main()
