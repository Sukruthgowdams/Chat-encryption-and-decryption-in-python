import socket
import threading

public_key = None
private_key = None
public_patner = None

def start_chat(choice):
    global public_patner
    
    if choice == "1":
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("192.168.156.106", 9999))
        server.listen()
        print("Waiting for a connection...")
        client, _ = server.accept()
        print("Connected to partner.")
    elif choice == "2":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("192.168.156.106", 9999))
        print("Connected to partner.")
    else:
        print("Invalid choice.")
        return

    def send_messages(c):
        while True:
            message = input("You: ")
            if message.lower() == "exit":
                c.send(message.encode())
                break
            c.send(message.encode())
            print("Partner is typing...")

    def receive_messages(c):
        while True:
            message = c.recv(1024).decode()
            if not message:
                break
            if message.lower() == "exit":
                break
            print("\nPartner:", message)
            print("You:", end=" ")  

    send_thread = threading.Thread(target=send_messages, args=(client,))
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    client.close()

if __name__ == "__main__":
    choice = input("Do you want to host(1) or connect(2): ")
    start_chat(choice)
