# decora_bleak

Python module for interacting with Leviton bluetooth switches and dimmers via BLE (Bluetooth Low Energy). There is prior art in this space, namely https://github.com/mjg59/python-decora and https://github.com/lucapinello/pydecora_ble, both of which primarily use the bluepy module. This project aims to provide the same support using Bleak which is used for interacting with BLE devices in Home Assistant.

## Using

Once the package is installed (and assuming the repo was cloned to make changes) using `python -m pip install -e .`:

```
decora scan
```

```
decora connect -a "C84441EE-5C57-2681-1BD5-82AF18C58F5D"
```

```
decora connect -a "C84441EE-5C57-2681-1BD5-82AF18C58F5D" -k "8c4c89fa00"
```

## Releasing

One of

```
bumpver update --commit --tag-commit --push --major
bumpver update --commit --tag-commit --push --minor
bumpver update --commit --tag-commit --push --patch
```
