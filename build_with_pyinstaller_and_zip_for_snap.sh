rm -rf ./build/
rm -rf ./dist/
# pyinstaller -F -w -n multimanage --hidden-import=pkg_resources.py2_warn --onefile --windowed --icon=MultiManage-Logo.ico multimanage.py
pyinstaller -F -w -n multimanage --onefile --windowed --icon=MultiManage-Logo.ico multimanage.py
mkdir ./bin -p
cp ./dist/multimanage ./bin/
zip -FSr snap_binary.zip ./bin/*
rm -rf ./bin
snapcraft -v
snap remove multimanage
snap install multimanage_0.1_amd64.snap  --devmode --dangerous