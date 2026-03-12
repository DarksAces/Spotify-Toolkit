# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_menu.py'],
    pathex=[],
    binaries=[],
    datas=[('Delet Duplicates', 'Delet Duplicates'), ('Extraer Artistas', 'Extraer Artistas'), ('Reorder', 'Reorder'), ('Separate Artists', 'Separate Artists'), ('Separate Genres', 'Separate Genres'), ('Shufle', 'Shufle'), ('Time', 'Time'), ('Top Tracks', 'Top Tracks')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SpotifyToolkit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
