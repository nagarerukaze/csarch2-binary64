import struct

def base10_to_binary64(decimal):
    # Split the decimal into its mantissa and exponent parts
    parts = decimal.split(' x ')
    mantissa = float(parts[0])
    sign_bit = '0' if mantissa >= 0 else '1'
    exponent = int(parts[1].replace('10^', ''))
    
    
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
    
    mantissa_str = str(binary_mantissa)
    
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
    
    binary_fractional_part = mantissa_str[mantissa_str.index('.') + 1:]
    binary_fractional_part = binary_fractional_part.ljust(52, '0')
        
    exponent_prime = exponent + 1023
    exponent_prime_bin = bin(exponent_prime)[2:].zfill(11)
    
    print("Sign bit: ", sign_bit)
    print("E': ", exponent_prime_bin)
    print("Mantissa: ", binary_fractional_part)
    
    # Combine the sign bit, exponent and mantissa
    binary64 = sign_bit + exponent_prime_bin + binary_fractional_part
    
    # make sure binary64 is 64 characters long
    return binary64

# Example usage
decimal = "-5.75 x 10^0"
print(decimal)
binary = base10_to_binary64(decimal)
print(binary)
# print hex
print(hex(int(binary, 2)))