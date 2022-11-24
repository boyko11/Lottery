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

Build as docker flask container from the project root dir(not from the docker subdir)
```bash
docker build . -t lottery_web:latest -f docker/Dockerfile
```

Then run on whatever port you like:
```bash
docker run -p 8000:4637 -d lottery_web
# if you want to map logs directory to a local host directory:
docker run -v /Users/btodorov/lottery_logs_1:/app/logs -p 8000:4637 -d lottery_web
```
```
# one sample powerball
http://localhost:8000/pb?num_samples=1

# seven samples of mega millions
http://localhost:8000/mm?num_samples=7

# default num_samples is 5
# ie, if num_samples isn't specified, the API will return five samples:
http://localhost:8000/pb

```

Running as script:

```bash
# Examples:
# sample 5 draws of MegaMillions
python -m test.lottery 5

# sample 1 draw of Powerball
python -m test.lottery power 1

# sample 3 draws of Powerball
python -m test.lottery power 3

```



## License
Feel free to use anyway you like. Cheers!