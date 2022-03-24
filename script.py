import sys
import os
import shutil
from jsmin import jsmin

is_release = False


def minifie(src, dest):
    if is_release:
        with open(src) as input:
            minified = jsmin(input.read())
            output = open(dest, 'w+')
            output.write(minified)
            output.close()
    else:
        shutil.copy2(src, dest)

def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)


# builds the editor
def main():
    global is_release

    if len(sys.argv) == 2:
        # set release
        if sys.argv[1] == "release":
            is_release = True
        # test then exit
        elif sys.argv[1] == "test":
            # test editor
            os.system("cd rust && cargo test && wasm-pack test --node")
            return

    # create build dir
    if not os.path.exists("build"):
        os.makedirs("build")


    # compile to wasm
    os.system("cd rust && wasm-pack build --target no-modules --no-typescript " +
              ("--release" if is_release else ""))

    makedir("build")

    # copy vs is not exists
    if not os.path.exists("build/vs"):
        os.system("cp -r vs build/vs")

    # copy html css and js
    minifie("web/script.js", "build/script.js")
    shutil.copy2("web/index.html", "build/index.html")

    # make rust
    shutil.copy2("rust/pkg/rust_bg.wasm",
                 "build/rust_bg.wasm")
    minifie("rust/pkg/rust.js", "build/rust.js")

if __name__ == "__main__":
    main()