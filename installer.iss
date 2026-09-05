[Setup]
AppName=Dead Focused
AppVersion=1.0.0
DefaultDirName={autopf}\Dead Focused
DefaultGroupName=Dead Focused
OutputBaseFilename=DeadFocusedSetup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\Dead Focused\*"; DestDir: "{app}"; Flags: recursesubdirs

[Tasks]
Name: "startmenuicon"; Description: "Create a Start Menu shortcut"; GroupDescription: "Additional shortcuts:"

[Icons]
Name: "{group}\Dead Focused"; Filename: "{app}\Dead Focused.exe"; Tasks: startmenuicon
Name: "{autodesktop}\Dead Focused"; Filename: "{app}\Dead Focused.exe"