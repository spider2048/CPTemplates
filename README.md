# CP Templates

> Sp1d3R | 2024

A collection of CP Templates.

## Python

Features:

* Supports hot-reload (responds to changes in specified files)
* Supports timers
* Copies code on save to clipboard
* Code is fully pastable anywhere
* Responds to Ctrl+C
* Tested on Windows 11 and Linux

Usage:

* Declare the `LOCAL` environment variable
* Correct the constructor

```python
ProcessHandler(
    main=main,
    props={"input": "input.txt", "code": __file__},
    monitor=["Code.py", "input.txt"],
    timeout=1,
)
```

* Install requirements from `requirements.txt`
* Use [instructions](https://sp1d3r.vercel.app/posts/pycompile/) to compile the `local.py`.
