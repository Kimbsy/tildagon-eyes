# tildagon-eyes

Some cute animated eyes for your Tildagon badge, lots of colours to choose from.

# Setup and run on badge

https://tildagon.badge.emfcamp.org/tildagon-apps/development/

install pipx
``` shell
sudo apt install pipx
```

install mpremote with pipx
``` shell
# in tildagon-eyes/ dir
pipx install mpremote
```
create metadata.json

connect badge

create folders

``` shell
mpremote mkdir apps
mpremote mkdir apps/eyes
```

copy app files over and connect to the badge

``` shell
./upload.sh
```

`ctrl-d` to reboot while connected

> [!CAUTION]
> Update app version in `tildagon.toml` before we make a release!
