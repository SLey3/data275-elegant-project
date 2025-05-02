"""
USAGE: in the terminal, make sure your in the root directory of the project and run the following command:
python3 push.py "<insert commit message>"
"""

from subprocess import run, PIPE
from time import sleep
import sys


def main():
    try:
        commit_msg: str = sys.argv[1]
    except IndexError:
        print('Commit message is required! \n\nUSAGE: python3 push.py "<insert commit message>"')
        sys.exit(1)
    
    print("adding project to git stage...")
    sleep(1)
    run(["git", "add", "."], stdin=sys.stdin, stderr=sys.stderr, stdout=PIPE)
    
    print("committing changes...")
    sleep(1)
    run(["git", "commit", "-m", f'"{commit_msg}"'], stdin=sys.stdin, stderr=sys.stderr, stdout=PIPE)
    
    print("pushing changes. If any error pops up run 'git pull' else if you cant figure it out reach out for support!")
    sleep(1)
    run(["git", "push"], stdin=sys.stdin, stderr=sys.stderr, stdout=PIPE)
    
    print("Changes were pushed successfully! Exiting program...")
    sleep(1)
    
if __name__ == '__main__':
    main()