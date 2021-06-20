import sys, os

def test_no_exe_files():
    for fname in os.listdir('.'):
        if fname.endswith('.exe'):
            sys.exit(1)
            break
    else:
        sys.exit(0)

test_no_exe_files()