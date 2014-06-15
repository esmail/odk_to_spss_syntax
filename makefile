SHELL := /bin/bash
.PHONY: doc autodoc

autodoc: .git/hooks/pre-commit doc

.git/hooks/pre-commit: git_hook_pre-commit.sh
	# Symlink the Git pre-commit hook into place
	# TODO: Convert this ugly crap to a multi-liner that actually executes.
	if [ ! -e .git/hooks/pre-commit ] ; then ln -s ../../git_hook_pre-commit.sh .git/hooks/pre-commit ; fi


doc: doc/gh-pages doc/gh-pages/index.html

doc/gh-pages:
	# Set up the directory 'doc/gh-pages' as a git "workdir" that can contain a different branch of the repository.
	# Thanks to: http://raxcloud.blogspot.com/2013/02/documenting-python-code-using-sphinx.html
	bash /usr/share/doc/git/contrib/workdir/git-new-workdir . doc/gh-pages || /usr/local/share/git-core/contrib/workdir/git-new-workdir . doc/gh-pages
	(cd doc/gh-pages && git checkout gh-pages)

doc/gh-pages/index.html: env doc/source doc/source/*.rst doc/source/conf.py
	source env/bin/activate && cd doc && make html

env:
	virtualenv env
	source env/bin/activate && pip install sphinx

doc/source: odk_to_spss_syntax/*.py odk_to_spss_syntax/test/*.py
	source env/bin/activate && sphinx-apidoc --force --no-toc -o doc/source/ odk_to_spss_syntax

