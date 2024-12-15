import java.rmi.Remote;
import java.rmi.RemoteException;

public interface AuthService extends Remote {
    boolean verifyEmail(String email) throws RemoteException;
    boolean verifyPassword(String email, String password) throws RemoteException;
    String verifyCredentials(String email, String password) throws RemoteException;

    // Chat-related methods
    void registerClient(String email, ClientInterface client) throws RemoteException;
    void sendMessage(String sender, String receiver, String message) throws RemoteException;
}
