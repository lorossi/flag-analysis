# Flag Analysis

Quick and dirty analysis of the flags of the world.
It produces as output an image showing the relative quantity of each flag color.

Before running the script, place the flag `png` images from [this repo](https://github.com/hampusborgos/country-flags) (or any repo containing the flags of the world in png format) in the `flags` folder.

## Usage

```bash
python3 -m venv venv # create the virtual environment
source venv/bin/activate # activate the virtual environment
pip install -r requirements.txt # install the dependencies
python3 flag_analysis.py # run the script
```

## Results

| color   | quantity |
| :------ | :------- |
| #000000 | 16.48%   |
| #ffffff | 29.1%    |
| #0000ff | 9.93%    |
| #00ff00 | 2.82%    |
| #00ffff | 8.9%     |
| #ff0000 | 18.08%   |
| #ff00ff | 1.22%    |
| #ffff00 | 13.47%   |

![flag_analysis](out.png)
