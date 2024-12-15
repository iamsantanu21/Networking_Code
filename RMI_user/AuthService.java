import java.rmi.Remote;
import java.rmi.RemoteException;

public interface AuthService extends Remote {
    boolean verifyEmail(String email) throws RemoteException;
    boolean verifyPassword(String email, String password) throws RemoteException;
    String verifyCredentials(String email, String password) throws RemoteException; // Add RemoteException here
}
