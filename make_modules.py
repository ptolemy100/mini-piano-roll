import json

report = json.load(open('/tmp/r.json'))
items = {i['metadata']['name'].lower().replace('_', '-'): i for i in report['install']}

def source(name):
    info = items[name]['download_info']
    return {
        "type": "file",
        "url": info['url'],
        "sha256": info['archive_info']['hash'].split('=', 1)[1],
    }

def module(label, names):
    cmd = ('pip3 install --verbose --exists-action=i --no-index '
           '--find-links="file://${PWD}" --prefix=${FLATPAK_DEST} '
           + ' '.join(f'"{n}"' for n in names) + ' --no-build-isolation')
    return {
        "name": f"python3-{label}",
        "buildsystem": "simple",
        "build-commands": [cmd],
        "sources": [source(n) for n in names],
    }

modules = [
    module("pygame-ce", ["pygame-ce"]),
    module("numpy", ["numpy"]),
    module("scipy", ["scipy"]),
    module("sounddevice", ["pycparser", "cffi", "sounddevice"]),
]

out = {"name": "python3-modules", "buildsystem": "simple",
       "build-commands": [], "modules": modules}
json.dump(out, open('python3-modules.json', 'w'), indent=4)
print("wrote python3-modules.json")
