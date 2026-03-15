# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('Delete Duplicates', 'Delete Duplicates'), ('Artist Extractor', 'Artist Extractor'), ('Reorder', 'Reorder'), ('Separate Artists', 'Separate Artists'), ('Separate Genres', 'Separate Genres'), ('Shuffle', 'Shuffle'), ('Playlist Time', 'Playlist Time'), ('Top Tracks Generator', 'Top Tracks Generator'), ('Mood Mixer', 'Mood Mixer'), ('utils', 'utils')],
    hiddenimports=['spotipy', 'customtkinter', 'difflib'],
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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
