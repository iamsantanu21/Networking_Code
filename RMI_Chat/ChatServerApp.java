import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

public class ChatServerApp {
    public static void main(String[] args) {
        try {
            LocateRegistry.createRegistry(6080);
            ChatServer chatServer = new ChatServerImpl();
            Naming.rebind("rmi://localhost:6080/ChatServer", chatServer);
            System.out.println("Chat server is ready.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
