# minishell_tester
Testing Suite For The minishell Project Of The 42 Core Curriculum

## Features
minishell_tester provides a list of test commands in a Python script and executes them simultaenously with your minishell and bash to compare the results.
The test outputs of each command are saved in separate log files in $HOME/minishell_tester/testlogs.

## Installation
```
bash -c "$(curl -fsSL https://raw.github.com/francisrafal/minishell_tester/main/install.sh)"
```
This script installs minishell_tester in $HOME/minishell_tester

## Usage
```
minishell_tester '<your_minishell_prompt_in_single_quotes>' [testnumber]
```

Example: Execute All Tests
```
minishell_tester 'minishell$ '
```

Example: Execute Only Test No. 5
```
minishell_tester 'minishell$ ' 5
```

## Adding Tests
You can easily add new tests:
Add new commands you want to test in the `$HOME/minishell_tester/linishell_tester.py` file to the list `TESTCMDS`
