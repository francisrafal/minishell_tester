#!/bin/bash

cd $HOME
rm -rf minishell_tester

mkdir minishell_tester_tmp

rm -rf minishell_tester
cd minishell_tester_tmp

git clone https://github.com/francisrafal/minishell_tester.git

cp -r minishell_tester $HOME

cd $HOME
rm -rf minishell_tester_tmp

cd $HOME/minishell_tester

#pip3 install -r requirements.txt

RC_FILE=$HOME/.zshrc

if [ "$(uname)" != "Darwin" ]; then
	RC_FILE=$HOME/.bashrc
	if [[ -f $HOME/.zshrc ]]; then
		RC_FILE=$HOME/.zshrc
	fi
fi

if ! grep "minishell_tester=" $RC_FILE &> /dev/null; then
	echo "minishell_tester alias not present"
	echo "Adding alias in file: $RC_FILE"
	echo -e "\nalias minishell_tester=\"python3 $HOME/minishell_tester/minishell_tester.py\"\n" >> $RC_FILE
fi

exec $SHELL
