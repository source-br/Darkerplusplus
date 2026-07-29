from PyInstaller.building.build_main import Analysis, PYZ, EXE
from PyInstaller.utils.win32.versioninfo import (
    VSVersionInfo, FixedFileInfo, StringFileInfo,
    StringTable, StringStruct, VarFileInfo, VarStruct
)

block_cipher = None

version_info = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(0, 1, 0, 0),
        prodvers=(0, 1, 0, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo([
            StringTable(
                u'040904B0',
                [StringStruct(u'CompanyName',      u'kenned-candido'),
                 StringStruct(u'FileDescription',  u'Hammerfy — Gerenciador Hammer++'),
                 StringStruct(u'FileVersion',      u'0.1.0.0'),
                 StringStruct(u'InternalName',     u'Hammerfy'),
                 StringStruct(u'LegalCopyright',   u'GPL-3.0'),
                 StringStruct(u'OriginalFilename', u'Hammerfy.exe'),
                 StringStruct(u'ProductName',      u'Hammerfy'),
                 StringStruct(u'ProductVersion',   u'0.1.0.0')])
        ]),
        VarFileInfo([VarStruct(u'Translation', [0x0409, 1200])])
    ]
)

# 1. Main Hammerfy Executable
a1 = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('assets/icons',   'assets/icons'),
        ('assets/banners', 'assets/banners'),
        ('styles',         'styles'),
        ('locales',        'locales'),
    ],
    hiddenimports=[
        'winreg',
        'urllib',
        'urllib.request',
        'urllib.error',
        'http.client',
        'ssl',
        'certifi',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz1 = PYZ(a1.pure, a1.zipped_data, cipher=block_cipher)

exe1 = EXE(
    pyz1,
    a1.scripts,
    a1.binaries,
    a1.zipfiles,
    a1.datas,
    [],
    name='Hammerfy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/hammerfy-icon.ico',
    onefile=True,
)

# 2. Companion HammerfyUpdater Executable
a2 = Analysis(
    ['updater_app.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'urllib',
        'urllib.request',
        'urllib.error',
        'http.client',
        'ssl',
        'certifi',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz2 = PYZ(a2.pure, a2.zipped_data, cipher=block_cipher)

exe2 = EXE(
    pyz2,
    a2.scripts,
    a2.binaries,
    a2.zipfiles,
    a2.datas,
    [],
    name='HammerfyUpdater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/hammerfy-icon.ico',
    onefile=True,
)