import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class ClientImpl extends UnicastRemoteObject implements ClientInterface {
    @SuppressWarnings("unused")
    private String email;

    public ClientImpl(String email) throws RemoteException {
        this.email = email;
    }

    @Override
    public void receiveMessage(String sender, String message) throws RemoteException {
        System.out.println(sender + ": " + message);
    }
}
