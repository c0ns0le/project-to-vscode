#!/usr/bin/env bash


if [ ! -d $(dirname $0)/.venv ]; then
    python3 -m venv $(dirname $0)/.venv
    source $(dirname $0)/.venv/bin/activate
    pip install -U pip
    pip install -r $(dirname $0)/requirements.txt
fi

if [ ! -d $HOME/.local/bin/ ]; then
    mkdir $HOME/.local/bin/
fi

cat > $HOME/.local/bin/projeto-para-vscode << EOL
#!/usr/bin/env bash


source $(dirname $PWD/$0)/.venv/bin/activate
python3 $(dirname $PWD/$0)/core/run.py \$1
EOL

chmod u+x $HOME/.local/bin/projeto-para-vscode
