import pexpect
import sys
import os
import pty
import subprocess
import random

TESTLOGPATH = os.path.expandvars("$HOME") + "/minishell_tester/testlogs/"
MINISHELLPATH = "./minishell"
# Check if the minishell file exists
if not os.path.isfile(MINISHELLPATH):
    print("Error: minishell file not found in directory")
    exit(1)

ARGC = len(sys.argv)
if (ARGC > 1):
    PROMPT = sys.argv[1]
else:
    print("Error: No prompt specified")
    print("Usage: python3 interactive.py '<your_minishell_prompt_in_single_quotes>'")
    exit(1)

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

def run_command(cmd):
    PROMPT = get_minishell_prompt([MINISHELLPATH])
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    testnum = random.randint(100, 150)
    minishell = pexpect.spawn(MINISHELLPATH)
    minishell_logfile = TESTLOGPATH + str(testnum).zfill(3) + "_testoutput_minishell.log"
    minishell.logfile_read = open(minishell_logfile, "wb")

    bash = pexpect.spawn("bash")
    bash_logfile = TESTLOGPATH + str(testnum).zfill(3) + "_testoutput_bash.log"
    bash.logfile_read = open(bash_logfile, "wb")

    print(bcolors.HEADER + bcolors.BOLD + f"\nTest {testnum:03d}" + bcolors.ENDC)
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
    return process.returncode

def main():
    print("Entering interactive session. Type 'exit' to exit.")
    while True:
        command = input("$ ")
        if command == 'exit':
            break
        run_command(command)

if __name__ == "__main__":
    main()
