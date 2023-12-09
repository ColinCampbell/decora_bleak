# Releasing

## Bump Version

One of

```
bumpver update --commit --tag-commit --push --major
bumpver update --commit --tag-commit --push --minor
bumpver update --commit --tag-commit --push --patch
```

## Publish PyPi Package

```
python -m pip install build twine
python -m build
twine check dist/*
twine upload dist/*
```
