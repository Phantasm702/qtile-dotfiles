#!/bin/bash

git_url="https://github.com/Phantasm702/qtile-dotfiles.git"
folder_name="qtile-dotfiles/qtile"
depends=("qtile" "git" "brightnessctl")

cfg_dir=".config/qtile" # DOTFILES SPECIFC
now=$(date +%m-%d_%H-%M-%S) # DOTFILES SPECIFC


satisfied=0
for depend in "${depends[@]}"; do
    if ! (command -v "$depend" &> /dev/null); then
        echo "$depend not installed"
    else
        satisfied=$((satisfied + 1))
    fi
done


if [ $satisfied == ${#depends[@]} ]; then
    echo "Dependencies satisfied... starting installation"
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

echo "Setting permissions"
cd "$HOME/$cfg_dir" || echo "cd failed"
pwd
chmod -R +x ./*

echo "Done, enjoy my rice :)"