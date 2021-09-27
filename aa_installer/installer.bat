SET InputDir=S:\Shared\IT\Nexus\aa_installer_win10
SET OutputDir=C:\Users\%USERNAME%\aa_installer\
SET InfoBeforeFile=S:\Shared\IT\Nexus\aa_installer\Scripts\README.md
SET ExcelPath=C:\Program Files\Microsoft Office\root\Office16\EXCEL.exe
SET InstallerExe=H:\aa_installer\Scripts\installer.exe.lnk
SET ExcelFile=H:\aa_installer\Scripts\arp_dashboard.xlsm

IF exist %OutputDir% ( rmdir /s /q %OutputDir% )
mkdir %OutputDir%
xcopy %InputDir% %OutputDir% /E

cd /d %OutputDir%
for %%f in (*.whl) do (
     echo %%f
     set file_name=%%f
)

call virtualenv venv
call venv\Scripts\activate.bat
call pip install %file_name%
