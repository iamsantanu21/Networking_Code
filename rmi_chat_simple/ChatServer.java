import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

public class ChatServer {
    public static void main(String[] args) {
        try {
            // Start the RMI registry
            LocateRegistry.createRegistry(7099);
            System.out.println("RMI Registry started.");

            // Create and bind the remote object
            ChatService chatService = new ChatServiceImpl();
            Naming.rebind("ChatService", chatService);
            System.out.println("Chat server is ready.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
