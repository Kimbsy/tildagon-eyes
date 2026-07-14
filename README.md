# tildagon-eyes

Some cute animated eyes for your Tildagon badge, lots of colours to choose from.

Available form the badge app store as `Tildagon Eyes`

## contributing

Please feel free to make a pull request to add a colour theme.

All you need to do is define your colours (either as an `[R, G, B]` tuple or with a hex string using the `parse_hex` helper function).

Then add an entry into the `THEMES` dictionary keyed by display name and with a `[FACE_COLOUR, EYE_COLOUR]` tuple as the value.

## Setup and run on badge

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
> Note to self: Update app version in `tildagon.toml` before we make a release!
