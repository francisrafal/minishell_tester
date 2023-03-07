#!/bin/bash

cd $HOME || exit

mkdir minishell_tester_tmp

cd minishell_tester_tmp || exit
rm -rf minishell_tester

git clone https://github.com/francisrafal/minishell_tester.git

cp -r minishell_tester $HOME

cd $HOME || exit
rm -rf minishell_tester_tmp

cd $HOME/minishell_tester || exit

if ! pip3 install -r requirements.txt ; then
	echo "Installation Failed. Open An Issue On GitHub"
	exit 1
fi

RC_FILE=$HOME/.zshrc

if [ "$(uname)" != "Darwin" ]; then
	RC_FILE=$HOME/.bashrc
	if [[ -f $HOME/.zshrc ]]; then
		RC_FILE=$HOME/.zshrc
	fi
fi

echo "try to add alias in file: $RC_FILE"

if ! grep "minishell_tester=" $RC_FILE &> /dev/null; then
	echo "minishell_tester alias not present"
	echo "" >> $RC_FILE
	echo "alias minishell_tester=$HOME/minishell_tester/execute_tests.sh" >> $RC_FILE
	echo "" >> $RC_FILE
fi

exec "$SHELL"
minishell_tester
