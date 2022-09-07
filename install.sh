#!/bin/bash

git_url="https://github.com/Phantasm702/qtile-dotfiles.git"
folder_name="qtile-dotfiles"
root_dir="$(pwd)/$folder_name"
depends=("qtile" "git" "brightnessctl" "picom")

qtile_cfg_dir=".config/qtile" # DOTFILES SPECIFC
picom_cfg_dir=".config/picom"
now=$(date +%m-%d_%H-%M-%S) # DOTFILES SPECIFC


satisfied=0

echo "Checking if dependencies are installed"
for depend in "${depends[@]}"; do
    if ! (command -v "$depend" &> /dev/null); then
        echo "$depend not installed, if it is, is it on \$PATH?"
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

echo ""

## DOTFILES SPECIFIC
cd "$root_dir" || (echo "git did not clone into $root_dir, correct \$folder_name variable and rerun" exit 1)

echo "Backing up current qtile config as ""$HOME/$qtile_cfg_dir""_bak_$now"
mv "$HOME/$qtile_cfg_dir" "$HOME/$qtile_cfg_dir""_bak_$now" 

echo "Copying qtile config to $HOME/$qtile_cfg_dir"
cd "$root_dir/qtile"
mkdir "$HOME/$qtile_cfg_dir"
cp -r ./* "$HOME/$qtile_cfg_dir"

echo -e "Setting permissions\n"
cd "$HOME/$qtile_cfg_dir" || (echo "cd failed, $HOME/$qtile_cfg_dir does not exist." && exit 1)
chmod -R +x ./*

echo "Backing up current picom config as ""$HOME/$picom_cfg_dir""_bak_$now"
mv "$HOME/$picom_cfg_dir" "$HOME/$picom_cfg_dir""_bak_$now"

echo "Copying picom config to $HOME/$picom_cfg_dir"
cd "$root_dir/picom"
mkdir "$HOME/$picom_cfg_dir"
cp -r ./* "$HOME/$picom_cfg_dir"

echo ""

echo "Cleaning up"
cd
rm -rf "$root_dir"

echo ""

echo "Done, enjoy my rice :)"
