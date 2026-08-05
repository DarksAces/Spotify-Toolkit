# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_build.py'],
    pathex=[],
    binaries=[],
    datas=[('utils', 'utils'), ('delete_duplicates', 'delete_duplicates'), ('metadata_export', 'metadata_export'), ('library_backup', 'library_backup'), ('smart_shuffle', 'smart_shuffle'), ('separate_genres', 'separate_genres'), ('separate_artists', 'separate_artists'), ('top_tracks_generator', 'top_tracks_generator'), ('trend_reports', 'trend_reports'), ('mood_mixer', 'mood_mixer'), ('dead_tracks_detector', 'dead_tracks_detector'), ('discovery_engine', 'discovery_engine'), ('C:\\Users\\danie\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\customtkinter', 'customtkinter')],
    hiddenimports=['spotipy', 'customtkinter', 'difflib', 'PIL.Image', 'PIL.ImageTk', 'darkdetect', 'tqdm', 'dotenv'],
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
