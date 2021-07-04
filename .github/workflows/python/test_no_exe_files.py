import sys, os

def test_no_exe_files():
    print("Searching for exe files in ", os.getcwd())
    for fname in os.listdir('.'):
        # non recursive search
        if fname.endswith('.exe'):
            sys.exit(1)
            break
    else:
        sys.exit(0)

test_no_exe_files()