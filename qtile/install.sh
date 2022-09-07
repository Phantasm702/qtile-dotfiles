#!/bin/bash

git_url="https://github.com/Phantasm702/qtile-dotfiles.git"
folder_name="qtile-dotfiles/qtile"
depends=("qtile" "git" "brightnessctl")

cfg_dir=".config/qtile" # DOTFILES SPECIFC
now=$(date +%m-%d_%H-%M-%S) # DOTFILES SPECIFC


satisfied=0

echo "Checking if dependencies are installed"
for depend in "${depends[@]}"; do
    if ! (command -v "$depend" &> /dev/null); then
        echo "$depend Not Installed"
    else
	    echo "$depend Installed"
        satisfied=$((satisfied + 1))
    fi
done


if [ $satisfied == ${#depends[@]} ]; then
    echo -e "Dependencies satisfied... starting installation\n"
else
    echo "Dependencies not satisfied, install them and rerun the script"
    exit 1
fi

## INSTALLATION
git clone $git_url

## DOTFILES SPECIFIC
cd "$folder_name" || (echo "git did not clone into $folder_name, correct \$folder_name variable and rerun" && exit 1)

echo "Backing up current config as ""$HOME/$cfg_dir""_bak_$now"
mv "$HOME/$cfg_dir" "$HOME/$cfg_dir""_bak_$now" 

echo "Copying files to $HOME/$cfg_dir"
mkdir "$HOME/$cfg_dir"
cp -r ./* "$HOME/$cfg_dir"

echo -e "Setting permissions\n"
cd "$HOME/$cfg_dir" || echo "cd failed"
#pwd
chmod -R +x ./*

echo "Done, enjoy my rice :)"
