# Lottery

Slightly smarter than random lottery sampler:  
It gets all the drawings in the past and counts how many times each number was drawn.  
Then it gives more weight(probability for next draw) to numbers that were drawn fewer times.  
  
For now, it just supports MegaMillions, Powerball should be coming up shortly.  

## Installation

Clone the repo. cd to the repo dir.  

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## License
Feel free to use anyway you like. Cheers!