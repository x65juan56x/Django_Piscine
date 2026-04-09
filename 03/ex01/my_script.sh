#!/bin/sh

echo "Pip version:"
python3 -m pip --version

echo "Removing previous installation..."
rm -rf "local_lib"
mkdir -p "local_lib"

echo "Upgrading build tools to prevent dependency conflicts..."
python3 -m pip install --user --upgrade pip setuptools wheel > /dev/null 2>&1

echo "Installing 'path' library..."

if python3 -m pip install --upgrade --force-reinstall \
    "git+https://github.com/jaraco/path.git" \
    --target local_lib \
    > path_install.log 2>&1; then

    echo "Library successfully installed. Running my_program.py..."
    python3 my_program.py
    exit 0
else
    echo "Error during library installation, check path_install.log"
    exit 1
fi