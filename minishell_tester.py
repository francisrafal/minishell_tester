#!/usr/bin/env python3
import pexpect
import sys
import os
import pty
import subprocess

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
    try:
        minishell = pexpect.spawn(MINISHELLPATH)
    except:
        print("Couldn't open minishell. Make sure to execute the tester in the folder where your Makefile and minishell binary are located.")
        exit(1)
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

def print_usage():
    print("Usage: minishell_tester [testnumber]")
    print("(Execute in the root directory of your minishell repo)\n")
    print("Example: Execute All Tests")
    print("minishell_tester \n")
    print("Example: Execute Only Test No. 5")
    print("minishell_tester 5\n")
    print("Options:")
    print("  -h, --help\tprint this help essage")
    print("  -u, --update\tupdate minishell_tester")

def build_minishell():
    print("")
    print(bcolors.HEADER + "Executing your Makefile..." + bcolors.ENDC)
    try:
        subprocess.run(["make"])
        print("")
    except:
        print("Couldn't execute Makefile. Make sure to execute the tester in the folder where your Makefile and minishell binary are located.")
        exit(1)

def print_logfile_info():
    print(bcolors.WARNING + "Test logs can be found in $HOME/minishell_tester/testlogs" + bcolors.ENDC)

          
def strip_escape_chars(output):
    """
    Removes escape characters from the output.
    """
    i = 0
    while i < len(output):
        if output[i:i+2] == b"\x1b[":
            j = i + 2
            while j < len(output) and not output[j:j+1].isalpha():
                j += 1
            output = output[:i] + output[j+1:]
        else:
            i += 1
    return output

def get_minishell_prompt(shell_command):
    # start the shell in a pseudo-terminal
    master, slave = pty.openpty()
    p = subprocess.Popen(shell_command, stdin=slave, stdout=slave, stderr=slave)

    # read output until we get the shell prompt
    output = b""
    while not b"$" in output and not b">" in output:
        output += os.read(master, 1024)

    # strip escape characters from the output
    output = strip_escape_chars(output)

    # find the prompt start index, ignoring any escape characters before the $ or >
    prompt_start_index = -1
    prompt_chars = [b"$", b">"]
    for prompt_char in prompt_chars:
        prompt_start_index = output.find(prompt_char)
        if prompt_start_index > 0:
            # backtrack to find the first escape character before the $ or >
            for i in range(prompt_start_index-1, -1, -1):
                if output[i:i+2] == b"\x1b[":
                    continue
                else:
                    prompt_start_index = i
                    break
            break

    # find the prompt end index
    prompt_end_index = output.find(b"\n", prompt_start_index)
    if prompt_end_index == -1:
        prompt_end_index = len(output)

    # extract the prompt substring and remove escape characters
    prompt = output.decode().lstrip()
    prompt = prompt.replace("\x1b[", "")

    # close the pseudo-terminal
    os.close(master)
    os.close(slave)

    return prompt

# Check if the minishell file exists
if not os.path.isfile(MINISHELLPATH):
    print("Error: minishell file not found in directory")
    print_usage()
    exit(1)
PROMPT = get_minishell_prompt([MINISHELLPATH])
print(f"Detected Prompt: ", PROMPT)

def execute_tests():
    os.makedirs(TESTLOGPATH, exist_ok=True)
    PROMPT = get_minishell_prompt([MINISHELLPATH])
    if ARGC > 1:
        print(bcolors.HEADER + "Executing Test..." + bcolors.ENDC)
        test(TESTCMDS[int(sys.argv[1])], int(sys.argv[1]))
    else:
        print(bcolors.HEADER + "Executing Tests..." + bcolors.ENDC)
        for testnum, cmdlist in enumerate(TESTCMDS):
            test(cmdlist, testnum)

def main():
    if PROMPT == "":
            print("Error: Could not get the prompt from minishell.")
            print_usage()  
            exit(1)
    os.environ['PROMPT'] = PROMPT
    if "-addtest" in sys.argv or "--addtest" in sys.argv:
    # Use subprocess to run the update script
        subprocess.run(["python3", os.path.expandvars("$HOME") + "/minishell_tester/interactive.py", PROMPT])
        exit(0)
    if "-u" in sys.argv or "--update" in sys.argv:
    # Use subprocess to run the update script
        subprocess.run(["python3", os.path.expandvars("$HOME") + "/minishell_tester/check_for_update.py"])
        exit(0)
    if "-h" in sys.argv or "--help" in sys.argv:
        print_usage()
        exit(0)
    print_welcome()
    build_minishell()
    execute_tests()
    print_logfile_info()

if __name__ == "__main__":
    main()
