from PyInstaller.building.build_main import Analysis, PYZ, EXE
from PyInstaller.building.datastruct import TOC
from PyInstaller.utils.win32 import VersionInfo

# Ler e compilar o version_info.txt
with open('version_info.txt', 'r') as f:
    version_info_str = f.read()

version_info = eval(version_info_str)

block_cipher = None

a = Analysis(
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
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'PySide6.QtSvg',
        'winreg',
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

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
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
    version_info=version_info,
)

VSVersionInfo(
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
        [StringStruct(u'CompanyName', u'kenned-candido'),
         StringStruct(u'FileDescription', u'Hammerfy — Hammer++ Manager'),
         StringStruct(u'FileVersion', u'0.1.0.0'),
         StringStruct(u'InternalName', u'Hammerfy'),
         StringStruct(u'LegalCopyright', u'GPL-3.0'),
         StringStruct(u'OriginalFilename', u'Hammerfy.exe'),
         StringStruct(u'ProductName', u'Hammerfy'),
         StringStruct(u'ProductVersion', u'0.1.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [0x0409, 1200])])
  ]
)