#!/bin/bash
if [[ $# < 2 ]] || [[ $# > 3 ]]; then
    echo "Usage: minishell_tester <absolute_path_to_minishell> '<prompt_in_single_quotes>' [testnumber]"
    echo
    echo "Example: Execute All Tests"
    echo "minishell_tester /home/francisrafal/minishell/minishell 'minishell$ '"
    echo
    echo "Example: Execute Only Test No. 5"
    echo "minishell_tester /home/francisrafal/minishell/minishell 'minishell$ ' 5"
fi

if [[ $# == 2 ]]; then
    python3 $HOME/minishell_tester/minishell_tester.py $1 $2
fi

if [[ $# == 3 ]]; then
    python3 $HOME/minishell_tester/minishell_tester.py $1 $2 $3 
fi