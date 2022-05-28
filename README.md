# Auto Commit

Automatically and periodically run `git commit`.

## Requirement

1. Python 3.10+
2. [GitPython](https://github.com/gitpython-developers/GitPython): `pip install GitPython`

## Usage

```sh
./autocommit.py -h
./autocommit.py -d <path-to-git-repo> -i <interval-in-seconds>
```

## Daemon on macOS

For running auto commit as a daemon on macOS (Darwin), config `org.tisonkun.git.autocommit.plist` and execute:

```sh
launchctl load org.tisonkun.git.autocommit.plist
# launchctl unload org.tisonkun.git.autocommit.plist # unload service
```
