# route checker - internal

A simple python script to get `show ip route` from a remote device and save the result in a file.

```shell
poetry install --no-root --sync
cd src
poetry run python {script}

# or
pip install -r requirements.txt
```

# what will be achieved?

- [ ] obtain routing table from a network device
  - [ ] store the raw data with timestamp
    - to go back and find the raw `show ip route` output
  - [ ] store the formatted data with timestamp
- [ ] generate diff summary for the latest and n-1 data
