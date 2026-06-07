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
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyAppExeName}
; Preserva os .json de configuração ao desinstalar
UninstallDisplayName={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startmenuicon"; Description: "Criar atalho no Menu Iniciar"; GroupDescription: "{cm:AdditionalIcons}"
Name: "quicklaunchicon"; Description: "Fixar na barra de tarefas"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\Hammerfy.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\locales\*"; DestDir: "{app}\locales"; Flags: ignoreversion recursesubdirs
Source: "..\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startmenuicon
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

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