import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.HashMap;
import java.util.Map;

public class ChatServerImpl extends UnicastRemoteObject implements ChatServer {
    private Map<String, ChatClient> clients;

    public ChatServerImpl() throws RemoteException {
        super();
        clients = new HashMap<>();
    }

    @Override
    public synchronized void registerClient(String clientName, ChatClient client) throws RemoteException {
        clients.put(clientName, client);
        System.out.println(clientName + " has joined the chat.");
    }

    @Override
    public synchronized void sendMessage(String message, String clientName) throws RemoteException {
        for (Map.Entry<String, ChatClient> entry : clients.entrySet()) {
            if (!entry.getKey().equals(clientName)) {
                entry.getValue().receiveMessage(clientName + ": " + message);
            }
        }
    }
}
