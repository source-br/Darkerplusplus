#define MyAppName "Hammerfy"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "kenned-candido"
#define MyAppURL "https://github.com/kenned-candido/hammerfy"
#define MyAppExeName "Hammerfy.exe"

[Setup]
AppId={{E4A2B3C1-1234-5678-ABCD-9F0E1D2C3B4A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=output
OutputBaseFilename=Hammerfy-Setup-{#MyAppVersion}
SetupIconFile=..\assets\icons\hammerfy-icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
RestartApplications=yes

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
brazilianportuguese.TaskDesktopIcon=Criar atalho na Área de Trabalho
brazilianportuguese.TaskStartMenuIcon=Criar atalho no Menu Iniciar
brazilianportuguese.TaskQuickLaunchIcon=Fixar na barra de tarefas

english.TaskDesktopIcon=Create a Desktop shortcut
english.TaskStartMenuIcon=Create a Start Menu shortcut
english.TaskQuickLaunchIcon=Pin to Taskbar

[Tasks]
Name: "desktopicon"; Description: "{cm:TaskDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startmenuicon"; Description: "{cm:TaskStartMenuIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "quicklaunchicon"; Description: "{cm:TaskQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\Hammerfy.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\HammerfyUpdater.exe"; DestDir: "{app}"; Flags: ignoreversion; Check: FileExists('..\dist\HammerfyUpdater.exe')
Source: "..\locales\*"; DestDir: "{app}\locales"; Flags: ignoreversion recursesubdirs
Source: "..\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startmenuicon
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall

[UninstallDelete]
; Remove arquivos gerados pelo app MAS preserva os .json de configuração
Type: files; Name: "{app}\hammerplusplus_versions.json"
; NÃO listamos hammerfy_settings.json — ele é preservado na atualização

[Code]
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  SettingsFile: String;
  VersionsFile: String;
  TempDir: String;
begin
  if CurUninstallStep = usUninstall then
  begin
    TempDir := ExpandConstant('{userappdata}\HammerfyBackup');
    SettingsFile := ExpandConstant('{app}\hammerfy_settings.json');
    VersionsFile := ExpandConstant('{app}\hammerplusplus_versions.json');

    // Cria pasta de backup temporária
    CreateDir(TempDir);

    // Faz backup dos JSONs antes de desinstalar
    if FileExists(SettingsFile) then
      FileCopy(SettingsFile, TempDir + '\hammerfy_settings.json', False);
    if FileExists(VersionsFile) then
      FileCopy(VersionsFile, TempDir + '\hammerplusplus_versions.json', False);
  end;

  if CurUninstallStep = usPostUninstall then
  begin
    TempDir := ExpandConstant('{userappdata}\HammerfyBackup');
    // Restaura JSONs após desinstalar (para atualização)
    // Na próxima instalação o app vai encontrá-los em AppData
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  TempDir: String;
  AppDir: String;
begin
  if CurStep = ssPostInstall then
  begin
    TempDir := ExpandConstant('{userappdata}\HammerfyBackup');
    AppDir := ExpandConstant('{app}');

    // Restaura JSONs do backup se existirem (vindo de uma atualização)
    if FileExists(TempDir + '\hammerfy_settings.json') then
      FileCopy(TempDir + '\hammerfy_settings.json', AppDir + '\hammerfy_settings.json', False);
    if FileExists(TempDir + '\hammerplusplus_versions.json') then
      FileCopy(TempDir + '\hammerplusplus_versions.json', AppDir + '\hammerplusplus_versions.json', False);

    // Remove backup temporário
    DeleteFile(TempDir + '\hammerfy_settings.json');
    DeleteFile(TempDir + '\hammerplusplus_versions.json');
    RemoveDir(TempDir);
  end;
end;