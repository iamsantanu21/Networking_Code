import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ChatServer extends Remote {
    void sendMessage(String message, String clientName) throws RemoteException;
    void registerClient(String clientName, ChatClient client) throws RemoteException;
}
