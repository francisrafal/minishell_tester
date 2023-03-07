### How to use:
### python3 minishell_tester.py <absolute path to your minishell executable>

import pexpect
import sys
import os

### ADD NEW TESTS HERE ###
TESTCMDS = [
    ["/bin/ls"],
    [""],
    ["/bin/uname"],
    ["/bin/uname -a"],
    ["     "],
    ["abc"],
    ["echo hello world    how are you??"],
    [" echo -n hello"],
    ["echo \"cat lol.c | cat > lol.c\""],
    ["ls \"\""],
    ["echo $"],
    ["$"],
    ["echo $US"],
    ["echo $USER"],
    ["echo $USER:$USER"],
    ["echo \"$USER:$USER\""]
    ]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

PROMPT = sys.argv[1]
TESTLOGPATH = os.path.expandvars("$HOME") + "/minishell_tester/testlogs/"
MINISHELLPATH = "./minishell"
ARGC = len(sys.argv)

def referenceresult(minishell, bash_result):
    try:
        minishell.expect_exact(PROMPT, timeout=1)
        if (minishell.before.decode() == bash_result):
            return bcolors.OKGREEN + "OK" + bcolors.ENDC
        return bcolors.FAIL + "KO" + bcolors.ENDC
    except:
        return bcolors.FAIL + "KO" + bcolors.ENDC

def get_bash_result(bash, cmd):
    bash.sendline("export PS1='" + PROMPT + "'")
    bash.expect_exact("\r\n")
    bash.expect_exact(PROMPT)
    bash.sendline(cmd)
    bash.expect_exact(cmd + "\r\n")
    bash.expect_exact(PROMPT)
    return bash.before.decode()

def test(cmdlist, testnum):
    minishell = pexpect.spawn(MINISHELLPATH)
    minishell_logfile = TESTLOGPATH + str(testnum).zfill(3) + "_testoutput_minishell.log"
    minishell.logfile_read = open(minishell_logfile, "wb")

    bash = pexpect.spawn("bash")
    bash_logfile = TESTLOGPATH + str(testnum).zfill(3) + "_testoutput_bash.log"
    bash.logfile_read = open(bash_logfile, "wb")

    print(bcolors.HEADER + bcolors.BOLD + f"\nTest {testnum:03d}" + bcolors.ENDC)
    for i, cmd in enumerate(cmdlist):
        bash_result = get_bash_result(bash, cmd)
        print(f"{'Command:':10}{cmd}")
        print(f"{'Expected:':10}{bash_result}")
        minishell.sendline(cmd)
        minishell.expect_exact(cmd + "\r\n")
        print(referenceresult(minishell, bash_result)) 
    minishell.logfile_read.close()
    bash.logfile_read.close()
    minishell.sendline("exit")
    bash.sendline("exit")

def print_welcome():
    print(bcolors.UNDERLINE + bcolors.BOLD + bcolors.OKBLUE + "\nminishell Tester\n" + bcolors.ENDC)
    print("All results will be compared to your machine's bash")
    print("Test logs can be found in $HOME/minishell_tester/testlogs")

def print_usage():
    print("Usage: minishell_tester '<prompt_in_single_quotes>' [testnumber]")
    print("Example: Execute All Tests")
    print("minishell_tester 'minishell$ '")
    print("Example: Execute Only Test No. 5")
    print("minishell_tester 'minishell$ ' 5")

def build_minishell():
    pexpect.run("pwd")
    # print(bcolors.HEADER + "Executing your Makefile..." + bcolors.ENDC)
    # pexpect.run("make")
          
def main():
    if ARGC == 1 or ARGC > 3:
        print_usage()
    print_welcome()
    build_minishell()
    os.makedirs(TESTLOGPATH, exist_ok=True)
    if ARGC > 2:
        test(TESTCMDS[int(sys.argv[2])], int(sys.argv[2]))
    else:
        for testnum, cmdlist in enumerate(TESTCMDS):
            test(cmdlist, testnum)

if __name__ == "__main__":
    main()
