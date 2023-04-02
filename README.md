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


## Update
To update minishell_tester to the latest version, run the following command:
```
minishell_tester -u
```

## Usage
```
cd <path to your local minishell repo with your Makefile>
minishell_tester [testnumber]
```
*testnumber is Optional

Example: Execute All Tests
```
minishell_tester 'minishell$ '
```

Example: Execute Only Test No. 5
```
minishell_tester 'minishell$ ' 5
```

## Interactive Mode
To open interactive Mode, in which you can test any command:
```
minishell_tester -addtest
```


Options:
```
  -h, --help    print help
  -u, --update  update minishell_tester
```

## Adding Tests
You can easily add new tests:
Add new commands you want to test in the `$HOME/minishell_tester/minishell_tester.py` file to the list `TESTCMDS`

## Contributing
If you want to help on this project, feel free to look in the Projects tab and comment on an issue that you want to take on.
Or add a new issue in the Project and describe it.
Once your done working on it, please open a pull request, so I can review it.
