import hashlib
BLOCKSIZE = 65536

def hash_file(filename, algorithm='sha1', block_size=BLOCKSIZE):
    try:
        hasher =  getattr(hashlib, algorithm)()
    except AttributeError:
        raise ValueError('{} is not a valid hashing algorithm'.format(algorithm))

    with open(filename, 'rb') as afile:
        buf = afile.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(block_size)
    return hasher.hexdigest()
