#!/bin/sh
set -x #echo on

bumpversion.exe patch --allow-dirty
rm -rf dist/ build/ assetallocation_arp.egg-info/ assetallocation_arp_*.zip aa_installer/installer_config/*.whl
python setup.py bdist_wheel
wheel_file='ls -ll dist/*.whl'
echo ${wheel_file}
build_version=`echo $wheel_file | awk -F'[--]' '{print $3}'`
cp dist/assetallocation_arp-${build_version}-py3-none-any.whl /s/Shared/IT/Nexus/aa_installer/.
cp -f assetallocation_arp/arp_dashboard.xlsm aa_installer/installer_config/.
cp -f assetallocation_arp/arp_strategies.py aa_installer/installer_config/.
cp -f aa_installer/installer_config/*.* /s/Shared/IT/Nexus/aa_installer/Scripts/.
cp -f aa_installer/*.* /s/Shared/IT/Nexus/aa_installer/Scripts/.
cp -f README.md /s/Shared/IT/Nexus/aa_installer/Scripts/.
rm -f /s/Shared/IT/Nexus/aa_installer/Scripts/AssetAllocationInstaller.iss
git commit -m "modify the version in git" setup.py .bumpversion.cfg
git push
