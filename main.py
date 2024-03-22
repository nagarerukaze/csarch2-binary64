import struct

def toBinary64(decimal, base):
    # Split the decimal into its mantissa and exponent parts
    
    try:
        if base == 10:
            parts = decimal.split(' x ')
            mantissa = float(parts[0])
            sign_bit = '0' if mantissa >= 0 else '1'
            exponent = int(parts[1].replace('10^', ''))
            
            mantissa_str = str(mantissa)
            
            for i in range(abs(exponent)):
                # Get the character index of the decimal point
                if exponent < 0:
                    decimal_index = mantissa_str.index('.')
                    new_decimal_index = decimal_index - 1
                    decimal_index += 1
                    
                    # Insert decimal point at the correct index
                    mantissa_str = mantissa_str[:new_decimal_index] + '.' + mantissa_str[new_decimal_index:]
                    
                    # Remove decimal_index from string
                    mantissa_str = mantissa_str[:decimal_index] + mantissa_str[decimal_index + 1:]
                    
                    if(mantissa_str[0] == '.'):
                        mantissa_str = '0' + mantissa_str
                    
                elif exponent > 0:
                    decimal_index = mantissa_str.index('.')
                    mantissa_str = mantissa_str.replace('.', '')

                    # Insert decimal point at the correct index
                    new_mantissa_str = mantissa_str[:decimal_index + 1] + '.' + mantissa_str[decimal_index + 1:]
                    mantissa_str = new_mantissa_str
                    
                    if(mantissa_str[len(mantissa_str) - 1] == '.'):
                        mantissa_str = mantissa_str + '0'
                    
            
            mantissa = float(mantissa_str)
            
            print("Updated Input: ", mantissa)
            
            # Convert mantissa to binary with radix point and fractional part
            binary_mantissa = bin(int(abs(mantissa)))[2:]
            fractional_part = abs(mantissa) - int(abs(mantissa))
            binary_fractional_part = ''

            while fractional_part != 0:
                fractional_part *= 2
                bit = int(fractional_part)
                binary_fractional_part += str(bit)
                fractional_part -= bit

            binary_mantissa += '.' + binary_fractional_part
            
            exponent = 0
            
            mantissa_str = str(binary_mantissa)
        elif base == 2:
            parts = decimal.split(' x ')
            mantissa = float(parts[0])
            sign_bit = '0' if mantissa >= 0 else '1'
            exponent = int(parts[1].replace('2^', ''))
            
            mantissa_str = str(mantissa)
    except:
        print("Invalid input.")
        return None
    
    # normalize binary mantissa
    while(abs(float(mantissa_str)) >= 2):
        # Get the character index of the decimal point
        decimal_index = mantissa_str.index('.')
        new_decimal_index = decimal_index - 1
        decimal_index += 1
        # Insert decimal point at the correct index
        mantissa_str = mantissa_str[:new_decimal_index] + '.' + mantissa_str[new_decimal_index:]
        # Remove decimal_index from string
        mantissa_str = mantissa_str[:decimal_index] + mantissa_str[decimal_index + 1:]
        exponent += 1
    while(abs(float(mantissa_str)) < 1):
        # Get the character index of the decimal point
        decimal_index = mantissa_str.index('.')
        new_decimal_index = decimal_index + 1
        # Insert decimal point at the correct index
        mantissa_str = mantissa_str[new_decimal_index] + '.' + mantissa_str[new_decimal_index + 1:]
        exponent -= 1
    
    # extract fractional part
    binary_fractional_part = mantissa_str[mantissa_str.index('.') + 1:]
    
   
    if mantissa_str[len(mantissa_str) - 1] == '.':
        mantissa_str = mantissa_str + "0"  
            
    exponent_prime = exponent + 1023
    
    # handle special case if exponent is greater than max
    if exponent_prime > 2046:
        exponent_prime_bin = '11111111111'
    else:
        exponent_prime_bin = bin(exponent_prime)[2:].zfill(11)
        
    # handle denormalized special case
    if exponent_prime <= 0: 
        exponent_prime_bin = '00000000000'
        # normalize mantissa again
        difference = abs(abs(exponent) - 1022)
        position = mantissa_str.index('.')
        binary_fractional_part = "0" * (difference - 1)  + str(int(abs(float(mantissa_str.replace('.', '')))))
        
    binary_fractional_part = binary_fractional_part.ljust(52, '0')            
    
    print("Sign bit: ", sign_bit)
    print("Exponent: ", exponent)
    print("E': ", exponent_prime_bin)
    print("Mantissa: ", binary_fractional_part)
    
    # handle special cases infinity and NaN
    
    
    # Combine the sign bit, exponent and mantissa
    binary64 = sign_bit + exponent_prime_bin + binary_fractional_part
    
    # make sure binary64 is 64 characters long
    return binary64

# Example usage
decimal = "25.0 x 10^3"
base = 10
print("Input: ", decimal)
print("Base: ", base)

print("\n")

binary = toBinary64(decimal, base)

print("\n")

if binary != None:
    print("Binary: ", binary) 
    #print hex format
    print("Hex: ", hex(int(binary, 2)))