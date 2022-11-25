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

|  color  |      frequency       | count |
| :-----: | :------------------: | :---: |
| #000000 |  0.2736397170642688  | 35088 |
| #ffffff |  0.2420629040685659  | 31039 |
| #ffff00 |  0.1763669118048461  | 22615 |
| #ff0000 | 0.15193368011417252  | 19482 |
| #00ff00 | 0.060790629118672355 | 7795  |
| #0000ff | 0.05565130588721564  | 7136  |
| #00ffff | 0.03462609278857027  | 4440  |
| #ff00ff | 0.004928759153688381 |  632  |

![flag_analysis](out.png)
