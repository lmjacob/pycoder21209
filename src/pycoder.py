"""
PyCoder is an RLE compression/decompression tool.

This module launches both the PyCoder GUI and the command line
interfaces. Unlike, gzip/gunzip, pycoder.py acts both as compressor and
decompressor.

It reads command line arguments using the docopt library and using
the following grammar:

    $ python3 pycoder.py (-c [-t TYPE] | -d) [-p PASSWD] FILE

This module is also a script and GUI application. Please see function 
'_main' for instructions on how to use 'pycoder.py' as script or GUI 
app.

(c) João Galamba, 2022
$$LICENSE(GPL)
"""

from datetime import datetime
import rle
from rle import RLEMethod, encode_rle, decode_rle
import encrypt
from encrypt import CryptMethod, encrypt_file, decrypt_file
from docopt import docopt
import string
from utils import cls


doc = """
    PyCoder is an RLE compression/decompression tool

    It reads command line arguments using the docopt library and using
    the following grammar:    

    Usage:
        pycoder.py (-c [-t TYPE] | -d) [-p PASSWD] FILE        

    Options:
        -c , --encode
        -d , --decode
        -t TYPE, --type=TYPE    [default: 2]
        -p PASSWD, --password=PASSWD   [default: none]
        FILE
        -h, --help                              This help message"""

args = docopt(doc)

cls()

if args['--encode'] == True:    
    
    if args['--type'] == '1':
        method = RLEMethod.A
    elif args['--type'] == '2':
        method = RLEMethod.B 
    #:   
    
    in_file_path = args['FILE']
    out_file_path = args['FILE'] + ".rle" 
    encode_rle(method, in_file_path, out_file_path)

    if(str(method) == 'RLEMethod.A'):
        enc = '1 (opcode 33)'
    else:  
        enc = '2 (opcode 138)'     
    print(f"Compressed '{in_file_path}' into '{out_file_path}' using method {enc}")
    #:  
    
    if args['--password'] != 'none':        
        meth = CryptMethod.AES_CRYPTOGRAPHY
        encrypt_file(meth, out_file_path, args['--password'])        
    #:
#:        


if args['--decode'] == True:    
    
    if args['--password'] != 'none':         
        meth = CryptMethod.AES_CRYPTOGRAPHY
        in_file_path = args['FILE']
        decrypt_file(meth, in_file_path, args['--password'])             
    #:
    
    in_file_path = args['FILE']    
    out_file_path = args['FILE'][:-4:]
    values = decode_rle(in_file_path, out_file_path)
   
    ts_to_int = int.from_bytes(values[1], 'big')
    dt = datetime.fromtimestamp(ts_to_int)
    
    if(str(values[0]) == 'RLEMethod.A'):
        values[0] = '1 (opcode 33)'
    else:  
        values[0] = '2 (opcode 138)'    
    #:
    print(f"Decompressed '{in_file_path}' into '{out_file_path}' using method {values[0]}")
    print(f"Compression date/time : {dt}")
#: