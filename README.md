# timelock
This tool encrypts files so that they can only be decrypted after an approximate amount of time. It uses the time lock puzzle written about [here](https://people.csail.mit.edu/rivest/pubs/RSW96.pdf).

# Usage
## To encrypt
`python3 timelock.py --num-squarings 1000000 encrypt file.txt encrypted.txt`

Set the `--num-squarings` parameter according to approximately how long you want the decryption to take. You can calculate this value by finding how many squarings per second your computer can calculate, and then multiplying by how many seconds you want the decryption to take. See [benchmarking](/benchmark)

## To decrypt
`python3 timelock.py decrypt encrypted.txt decrypted.txt`

Note that decryption in Python will take a long time compared to an optimized native program. In the future, the benchmarking program can be developed into a full decryption program.
