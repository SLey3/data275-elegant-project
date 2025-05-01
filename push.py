from subprocess import run, PIPE 
import sys


def main():
    commit_msg: str = sys.argv[1]
    
    print("adding project to git stage")
    run(["git", "add", "."], stdin=sys.stdin, stderr=sys.stderr, stdout=PIPE)
    
    print("committing changes...")
    run(["git", "commit", "-m", f'"{commit_msg}"'], stdin=sys.stdin, stderr=sys.stderr, stdout=PIPE)
    
    print("pushing changes. If any error pops up run 'git pull' else if you cant figure it out check out your error online or with sergio")
    run(["git", "push"], stdin=sys.stdin, stderr=sys.stderr, stdout=PIPE)
    
if __name__ == '__main__':
    main()