#!/bin/bash

git_url="https://github.com/Phantasm702/qtile-dotfiles.git"
folder_name="qtile-dotfiles"
root_dir="$(pwd)/$folder_name"
depends=("qtile" "git" "brightnessctl" "nitrogen")
opt_depends=("alacritty" "picom" "wal")

alacritty_cfg_dir=".config/alacritty" # DOTFILES SPECIFC
qtile_cfg_dir=".config/qtile" # DOTFILES SPECIFC
picom_cfg_dir=".config/picom" # DOTFILES SPECIFC
bg_dir="$(pwd)/$folder_name/qtile/background.jpg"
now=$(date +%d-%m_%H-%M-%S) # DOTFILES SPECIFC


satisfied=true
echo "Checking if dependencies are installed"
for depend in "${depends[@]}"; do
    if ! (command -v "${depend}" &> /dev/null); then
        echo "FATAL: ${depend} not installed, if it is, is it on \$PATH?"
	satisfied=false
    else
        echo "${depend} Installed"
    fi
done


for depend in "${opt_depends[@]}"; do
    if ! (command -v "$depend" &> /dev/null); then
        echo -e "WARNING: optional dependency $depend not installed, if it is, is it on \$PATH? \nRice may not look/work as expected"
    fi
done
echo ""


if ! ${satisfied}; then
    echo -e "Dependencies not satisfied, install them and rerun the script"
    exit 1
fi
echo -e "Dependencies satisfied... starting installation\n"

## INSTALLATION
git clone ${git_url}

echo ""

## DOTFILES SPECIFIC
cd "${root_dir}" || (echo "git did not clone into ${root_dir}, correct \$folder_name variable and rerun" exit 1)


echo "Backing up current qtile config as ${HOME}/${qtile_cfg_dir}_bak_${now}"
mv "${HOME}/${qtile_cfg_dir}" "${HOME}/${qtile_cfg_dir}_bak_${now}" 

echo "Copying qtile config to ${HOME}/${qtile_cfg_dir}"
cd "${root_dir}/qtile" || echo "${root_dir}/qtile doesnt exist"
mkdir "${HOME}/${qtile_cfg_dir}"
cp -r ./* "${HOME}/${qtile_cfg_dir}"

echo -e "Setting permissions\n"
cd "${HOME}/${qtile_cfg_dir}" || (echo "cd failed, ${HOME}/${qtile_cfg_dir} does not exist." && exit 1)
chmod -R +x ./*


echo "Backing up current picom config as ${HOME}/${picom_cfg_dir}_bak_${now}"
mv "${HOME}/${picom_cfg_dir}" "${HOME}/${picom_cfg_dir}_bak_${now}"

echo "Copying picom config to ${HOME}/${picom_cfg_dir}"
cd "${root_dir}/picom" || echo "${root_dir}/picom doesnt exist"
mkdir "${HOME}/${picom_cfg_dir}"
cp -r ./* "${HOME}/${picom_cfg_dir}"
echo ""


echo "Backing up current alacritty config as ${HOME}/${alacritty_cfg_dir}_bak_${now}"
mv "${HOME}/${alacritty_cfg_dir}" "${HOME}/${alacritty_cfg_dir}_bak_${now}"

echo "Copying alacritty config to ${HOME}/${alacritty_cfg_dir}"
cd "${root_dir}/alacritty" || echo "${root_dir}/alacritty doesnt exist"
mkdir "${HOME}/${alacritty_cfg_dir}"
cp -r ./* "${HOME}/${alacritty_cfg_dir}"
echo ""


echo "Setting wallpaper"
nitrogen --set-auto "${bg_dir}" &> /dev/null
echo ""


echo "Cleaning up"
cd "${HOME}" || echo "${HOME} doesnt exist"
rm -rf "${root_dir}"

echo ""

echo "Done, enjoy my rice :)"
