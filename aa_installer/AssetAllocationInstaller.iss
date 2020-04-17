; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "AssetAllocation_Arp"
#define MyAppVersion "0.1"
#define MyAppPublisher "LGIM"
#define MyAppExeName "C:\Program Files (x86)\Microsoft Office\Office14\EXCEL.exe"
//#define MyAppExeName "{reg:HKCR\Applications\EXCEL.EXE\shell\open\command,default|EXCEL.EXE}"


[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{216C3833-AD3F-45A2-BFC3-13EEF046FBD5}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName=H:\AssetAllocation_Installer\
DisableProgramGroupPage=yes
InfoBeforeFile=S:\Shared\IT\Nexus\aa_installer\Scripts\README.md
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputDir=S:\Shared\IT\Nexus\aa_installer
OutputBaseFilename=assetallocation_arp-0.0.10
Compression=lzma
SolidCompression=yes
WizardStyle=modern
CloseApplications=force

; attempt to remove previous versions' icons
[InstallDelete]
Type: filesandordirs; Name: {app}\*;

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[InstallDelete]
Type: files; Name: "{app}\*"

[Files]
Source: "S:\Shared\IT\Nexus\aa_installer\Scripts\arp_strategies.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "S:\Shared\IT\Nexus\aa_installer\Scripts\arp_dashboard.xlsm"; DestDir: "{app}"; Flags: ignoreversion
Source: "S:\Shared\IT\Nexus\aa_installer\Scripts\xlwings.xlam"; DestDir: "{app}"; Flags: ignoreversion
Source: "S:\Shared\IT\Nexus\aa_installer\Scripts\installer.ps1"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files
Source: "S:\Shared\IT\Nexus\aa_installer\assetallocation_arp-0.0.10-py3-none-any.whl"; DestDir: "{app}";
Source: "S:\Shared\IT\Nexus\aa_installer\Scripts\installer.exe.lnk"; DestDir: "{app}"; AfterInstall: RunOtherInstaller  

[Code]
procedure RunOtherInstaller;
var
  ErrorCode: Integer;
begin
  ShellExecAsOriginalUser('', ExpandConstant('{app}\installer.exe.lnk'), '', '',
    SW_SHOWNORMAL, ewWaitUntilTerminated, ErrorCode);
end;


[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Parameters: """{app}\arp_dashboard.xlsm""";Flags: nowait postinstall skipifsilent

