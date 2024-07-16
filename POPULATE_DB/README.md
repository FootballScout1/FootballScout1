# Quickly Populate the db

A quick brute force method to populate the database with everything


## POPULATE

Ensure to change value of ```py engine ```variable in create_Players
And export your environment variables

```sh
. venv/bin/activate && export FOOTBALL_SCOUT_TYPE_STORAGE=db && cd .. && cat ../master_populate | ./console.py && ./create_Players.py
```
