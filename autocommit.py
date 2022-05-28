#!/usr/bin/env python3

# Copyright 2022 tison <wander4096@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import logging
import re
import signal
import time
import uuid

import git


class GracefulShutdown:
    def __init__(self) -> None:
        self.is_running = True
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def wait(self, n) -> None:
        while self.is_running and n > 0:
            time.sleep(1)
            n = n - 1

    def shutdown(self, *args) -> None:
        self.is_running = False


def try_commit(repo: git.Repo) -> None:
    id = uuid.uuid4().hex
    status = repo.git.status()
    if re.search('working tree clean', status):
        logging.debug('Repo(%s) nothing to commit, working tree clean.', repo.working_dir)
        return
    logging.debug('Repo(%s) ready to add and commit.', repo.working_dir)
    try:
        repo.git.add('.')
        repo.git.commit('-m', f'autocommit {id}')
    except git.exc.GitCommandError as e:
        logging.warning('Repo(%s) conflict during committing. Error: %s', repo.working_dir, e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='git directories', nargs='+', required=True)
    parser.add_argument('-i', '--interval', help='autocommit interval in seconds', type=int, default=30)
    parser.add_argument('-l', '--level', help='logging level', default='INFO')
    args = parser.parse_args()

    logging.basicConfig(level=args.level.upper())

    interval = args.interval
    assert interval >= 0

    repos = [git.Repo(dir) for dir in args.directory]

    logging.info('Running autocommit for repos: %s', repos)
    guard = GracefulShutdown()
    while guard.is_running:
        for repo in repos:
            try_commit(repo)
        guard.wait(interval)

    logging.info('Shutting down...')
