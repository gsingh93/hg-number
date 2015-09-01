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

Installation
------------

```
pip install hg-number
```

To alias `hg-number` to `hgn`, add the following to your `.bashrc`:

```
alias hgn='hg-number'
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

- Don't replace numbers after a bare `--`. This will allow numeric arguments to be passed to mercurial without being replaced.

- Allow arbitrary commands to be executed instead of only mercurial commands. For example, `hgn -c rm 1` could execute `rm foo` instead of `hg rm foo`.
