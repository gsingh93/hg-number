hg-number
=========

`hg-number` is a python script that allows you to use numbers instead of file names in mercurial commands. Inspired by [git-number](https://github.com/holygeek/git-number).

Usage
-----

Example:

```
$ mkdir tmp && cd tmp
$ hg init
$ touch foo
$ touch bar
$ hgn

1 ? bar
2 ? foo

$ hgn add 1 2

hg add bar foo

$ hgn

1 A bar
2 A foo
```

You can use the `-c` flag to execute shell commands instead of mercurial commands

```
$ hgn -c echo filename: 1
echo filename: bar
filename: bar
```

Any arguments that should not be replaced should go after a double dash (`--`):

```
$ hgn -c -- echo filename: 1
echo filename: 1
filename: 1
```

Installation
------------

```
pip install hg-number
```

To alias `hg-number` to `hgn`, add the following to your `.bashrc`:

```
alias hgn='hg-number'
alias hgc='hg-number -c'
```

Configuration
-------------

Add `.hgnrc` to your home directory:

```
touch ~/.hgnrc
```

To enable colored output (assuming the mercurial color extension is enabled), add the following to the file:

```
[main]
color = true
```

TODO
----

- The script currently works by parsing the output of the mercurial binary, but mercurial provides an extension API that may be a better way of doing this.

- Ranges like `hg add 1-4` are not supported.
