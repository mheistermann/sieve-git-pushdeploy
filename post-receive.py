#!/usr/bin/env python2
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
import ConfigParser
import subprocess

from sievelib.managesieve import Client


class ConfigError(Exception):
    pass

class SieveError(Exception):
    pass

def read_config(git_path):
    defaults = {
            "starttls": "False",
            "scriptname": "main",
            "file": "main.sieve",
            "authmech": None,
            "refname": "refs/heads/master",
            }
    config = ConfigParser.SafeConfigParser(defaults)
    config_path = os.path.expanduser("~/.config/sieve-git-pushdeploy/sieve.conf")
    with open(config_path) as fp:
        config.readfp(fp)
    if git_path not in config.sections():
        raise ConfigError("Section [{}] missing".format(git_path))

    conf = {k: config.get(git_path, k) for k in [
        "host", "user", "pass", "file", "authmech", "scriptname", "refname"]}
    conf["starttls"] = config.getboolean(git_path, "starttls")

    return conf

def get_script(refname, filename):
    try:
        return subprocess.check_output(["git","show", refname + ":" + filename])
    except subprocess.CalledProcessError:
        raise ConfigError("Can't find file '{}' in '{}'".format(
            filename, refname))

def connect(config):
    conn = Client(config["host"])
    res = conn.connect(config["user"],
              config["pass"],
              starttls=config["starttls"],
              authmech=config["authmech"])
    if not res:
        raise SieveError(("Login unsuccessful for %(user)s:***@%(host)s,"
                   +" starttls=%(starttls)s, authmech=%(authmech)s") % config)
    return conn

def main():
    git_path = os.getcwd()
    config = read_config(git_path)
    logging.debug("config: {}", config)

    script = get_script(config["refname"], config["file"])

    conn = connect(config)

    logging.info("current scripts; %s", conn.listscripts())

    if not conn.checkscript(script):
        raise SieveError("script invalid.")

    if not conn.putscript(config["scriptname"], script):
        raise SieveError("could not upload script.")

    if not conn.setactive(config["scriptname"]):
        raise SieveError("could not set script active")
    print("Successfully uploaded sieve script.")


if __name__ == "__main__":
    try:
        ret = main()
    except (ConfigError, SieveError), e:
        logging.error(e.message)
        sys.exit(1)
