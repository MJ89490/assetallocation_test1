write-host "Ready to install AssetAllocation in site-packages!"
write-host "copy the installer from shared folder !"
write-host "Install AssetAllocation and its dependencies"
$file_name = Get-ChildItem *.whl
pip install $file_name
Sleep 60                      
write-host "Installed AssetAllocation successfully!"