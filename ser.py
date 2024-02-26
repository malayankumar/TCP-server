import socket

def xor_function(arr):
    data = 0
    for y in arr:
        data ^= y  # data= data ^ y
    return data

def process_data(data):
    # Assuming data is received as a list of integers
    recData = data

    messageID = [129, 0]
    identifyByte = 126
    sendHeader = []
    sendBody = []
    terminalNumber = []
    sendSerialNumber = [0, 1]
    authCode = [56,89,12,34,97,88,99]
    completeData = []

    for i in range(6, 16):
        terminalNumber.append(recData[i])

    # Creating header
    sendHeader.extend(messageID)
    sendHeader.append(recData[3])
    sendHeader.append(0) 
    sendHeader.append(1)  # Assuming protocol version is 1
    sendHeader.extend(terminalNumber)
    sendHeader.append(recData[16])
    sendHeader.append(recData[17])

    # Creating message
    sendBody.extend(sendSerialNumber)
    sendBody.append(0)
    sendBody.extend(authCode)

    # Adding length to header
    sendHeader[3] = len(sendBody)
    checkCode = xor_function(sendHeader + sendBody)

    # Creating complete response
    completeData.append(identifyByte)
    completeData.extend(sendHeader)
    completeData.extend(sendBody)
    completeData.append(checkCode)
    completeData.append(identifyByte)

    return bytes(completeData)

def general_Data(data):
    # Assuming data is received as a list of integers
    recData = data

    messageID = [129, 0]
    identifyByte = 126
    sendHeader = []
    sendBody = []
    terminalNumber = []
    sendSerialNumber = [0, 1]
    completeData = []

    for i in range(6, 16):
        terminalNumber.append(recData[i])

    # Creating header
    sendHeader.extend(messageID)
    sendHeader.append(recData[3])
    sendHeader.append(0) 
    sendHeader.append(1)  # Assuming protocol version is 1
    sendHeader.extend(terminalNumber)
    sendHeader.append(recData[16])
    sendHeader.append(recData[17])

    # Creating message
    sendBody.extend(sendSerialNumber)
    sendBody.extend(messageID)
    sendBody.append(0)

    # Adding length to header
    sendHeader[3] = len(sendBody)
    checkCode = xor_function(sendHeader + sendBody)

    # Creating complete response
    completeData.append(identifyByte)
    completeData.extend(sendHeader)
    completeData.extend(sendBody)
    completeData.append(checkCode)
    completeData.append(identifyByte)

    return bytes(completeData)

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.0.5', 8080)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)

print('Server is listening on', server_address)

while True:
    # Wait for a connection
    connection, client_address = server_socket.accept()

    try:
        print('Client connected:', client_address)

        # Receive data from the client
        while True:
            data = connection.recv(1024)
            if not data:
                break
            hex_data = " ".join("{:02x}".format(byte) for byte in data)
            print("Received:", hex_data)

            # Process the received data and send the response back to the client
            response_data = general_Data(list(data))
            hex_response_data = " ".join("{:02x}".format(byte) for byte in response_data)
            print("Response:", hex_response_data)

            connection.sendall(response_data)

    finally:
        # Clean up the connection
        connection.close()