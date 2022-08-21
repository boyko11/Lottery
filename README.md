# Lottery

Slightly smarter than random lottery sampler:  
It gets all the drawings in the past and counts how many times each number was drawn.  
Then it gives more weight(probability for next draw) to numbers that were drawn fewer times.  

## Installation

Clone the repo. cd to the repo dir.  

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Examples:
# sample 5 draws of MegaMillions
python lottery.py mega 5

# sample 1 draw of Powerball
python lottery.py power 1

# sample 3 draws of Powerball
python lottery.py power 3

```

## License
Feel free to use anyway you like. Cheers!