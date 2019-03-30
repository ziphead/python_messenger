from settings import ENCODING
try:
        
    while True:
        value = input('your text here')
        bvalue = value.encode(ENCODING)
        print('*'*15, 'data send operation'.upper(), '*'*15)
        print('*'*15, 'data recieve operation'.upper(), '*'*15)

except(KeyboardInterrupt):
    print('client exit')