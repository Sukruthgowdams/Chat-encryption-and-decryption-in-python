import socket
import threading
import rsa

public_key, private_key = rsa.newkeys(1024)
public_partner = None  

def start_chat(choice):
    global public_partner  

    if choice == "1":
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("192.168.156.106", 9999))
        server.listen()
        print("Waiting for a connection...")
        client, _ = server.accept()
        client.send(public_key.save_pkcs1("PEM"))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
        print("Connected to partner.")
        connection = client
    elif choice == "2":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("192.168.156.106", 9999))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
        client.send(public_key.save_pkcs1("PEM"))
        print("Connected to partner.")
        connection = client
    else:
        print("Invalid choice.")
        return

    def send_messages(c):
        while True:
            try:
                message = input("You: ")
                if message.lower() == "exit":
                    c.send(rsa.encrypt(message.encode(), public_partner))
                    break
                c.send(rsa.encrypt(message.encode(), public_partner))
                print("Partner is typing...")
            except Exception as e:
                print("Error sending message:", e)
                break

    def receive_messages(c):
        while True:
            try:
                encrypted_message = c.recv(1024)
                if not encrypted_message:
                    break
                message = rsa.decrypt(encrypted_message, private_key).decode()
                if message.lower() == "exit":
                    break
                print("\nPartner:", message)
                print("You:", end=" ")  
            except rsa.pkcs1.DecryptionError as e:
                print("Decryption error:", e)
                break
            except Exception as e:
                print("Error receiving message:", e)
                break
    send_thread = threading.Thread(target=send_messages, args=(connection,))
    receive_thread = threading.Thread(target=receive_messages, args=(connection,))
    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    connection.close()

if __name__ == "__main__":
    choice = input("Do you want to host(1) or connect(2): ")
    start_chat(choice)
