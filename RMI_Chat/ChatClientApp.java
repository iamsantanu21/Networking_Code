import java.rmi.Naming;
import java.util.Scanner;

public class ChatClientApp {
    public static void main(String[] args) {
        try {
            // Connect to the chat server
            ChatServer chatServer = (ChatServer) Naming.lookup("rmi://localhost:6080/ChatServer");

            try (// Register the client
            Scanner scanner = new Scanner(System.in)) {
                System.out.print("Enter your name: ");
                String clientName = scanner.nextLine();

                ChatClientImpl chatClient = new ChatClientImpl(clientName);
                chatServer.registerClient(clientName, chatClient);

                // Start a thread for sending messages
                Thread sendThread = new Thread(() -> {
                    try {
                        while (true) {
                            String message = scanner.nextLine();
                            chatServer.sendMessage(message, clientName);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                });
                sendThread.start();
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
