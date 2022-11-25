# Flag Analysis

Quick and dirty analysis of the flags of the world.
It produces as output an image showing the relative quantity of each flag color.

Before running the script, place the flag `png` images from [this repo](https://github.com/hampusborgos/country-flags) (or any folder containing the flags of the world in png format, really) in the `flags` folder.

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
| #000000 | 27.36%   |
| #ffffff | 24.21%   |
| #0000ff | 5.57%    |
| #00ff00 | 6.08%    |
| #00ffff | 3.46%    |
| #ff0000 | 15.19%   |
| #ff00ff | 0.49%    |
| #ffff00 | 17.64%   |

![flag_analysis](out.png)
