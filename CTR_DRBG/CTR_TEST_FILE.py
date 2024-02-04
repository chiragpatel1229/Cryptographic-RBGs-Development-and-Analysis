i = b'This is a test string.'
IV = len(i).to_bytes(4, 'big')
print(IV, len(IV))

K = bytes([x for x in range(1, 64 + 1)])
print(K)


def pad_data(data, outlen):
    # Calculate the remainder of the length of data divided by outlen
    remainder = len(data) % outlen

    # If the length of data is not a multiple of outlen
    if remainder != 0:
        # Calculate how many bytes need to be added
        padding_len = outlen - remainder

        # Pad the data with null bytes
        data += b'\x00' * padding_len

    return data


# Your data
data = b'Test String to check the Block Cipher.Test String to check the Block Cipher.Test String to check the Block Cipher.'

# The desired output length
outlen = 64

# Pad the data
padded_data = pad_data(data, outlen)

print(len(padded_data))
