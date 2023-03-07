# minishell_tester
Testing Suite For The minishell Project Of The 42 Core Curriculum
minishell_tester provides a list of test commands in a Python script and executes them simultaenously with your minishell and bash to compare the results.
The test outputs of each command are saved in separate log files.

# Installation
```
bash -c "$(curl -fsSL https://raw.github.com/francisrafal/minishell_tester/main/install.sh)"
```
This script installs minishell_tester in $HOME/minishell_tester

## Usage
```
minishell_tester <absolute_path_to_minishell> "<prompt_in_quotes>" [testnumber]
```

Example: Execute All Tests
```
minishell_tester /home/francisrafal/minishell/minishell "minishell$ "
```

Example: Execute Only Test No. 5
```
minishell_tester /home/francisrafal/minishell/minishell "minishell$ " 5
```

## Adding Tests
Add commands in the `$HOME/minishell_tester/linishell_tester.py` file to the list `testcmds`
