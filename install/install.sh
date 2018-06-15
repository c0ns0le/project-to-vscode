#!/usr/bin/env bash


if [ ! -d $1/.venv ]; then
    python3 -m venv $1/.venv
fi

source $1/.venv/bin/activate
pip install -U pip
pip install -r $1/requirements.txt

if [ ! -d $HOME/.local/bin/ ]; then
    mkdir --parents $HOME/.local/bin/
fi

cat > $HOME/.local/bin/projeto-para-vscode << EOL
#!/usr/bin/env bash


source $1/.venv/bin/activate
python3 $1/core/run.py \$1

EOL

chmod u+x $HOME/.local/bin/projeto-para-vscode

$HOME/.local/bin/projeto-para-vscode $(basename $1)

rm -rf $HOME/.config/Code $HOME/.vscode

code --install-extension ms-python.python

if [ ! -d $HOME/.config/Code/User/ ]; then
    mkdir --parents $HOME/.config/Code/User/
fi

if [ ! -d $HOME/.config/Code/Local\ Storage/ ]; then
    mkdir --parents $HOME/.config/Code/Local\ Storage/
fi

cp -f $1/install/settings.json $HOME/.config/Code/User/
cp -f $1/install/file__0.localstorage $HOME/.config/Code/Local\ Storage/

code

exit
