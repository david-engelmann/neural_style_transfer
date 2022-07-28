#!/bin/bash
apt-get update && export DEBIAN_FRONTEND=noninteractive \
	&& apt-get -y install --no-install-recommends \
        vim \
        fonts-powerline \
	&& apt-get update && apt-get -y upgrade

if type vim &>/dev/null
then
    PLUG_FILE="~/.vim/'autoload/plug.vim"
    if [ -f "$PLUG_FILE" ]
    then
        curl -fLo $PLUG_FILE --create-dirs \
            https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
    fi
    vim -E +PlugInstall +qall
else
    echo "VIM not found in container"
fi
exec "$@"