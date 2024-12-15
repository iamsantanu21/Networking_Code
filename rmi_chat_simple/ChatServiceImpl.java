import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.Scanner;

public class ChatServiceImpl extends UnicastRemoteObject implements ChatService {
    private static final long serialVersionUID = 1L;

    protected ChatServiceImpl() throws RemoteException {
        super();
    }

    @Override
    public String sendMessage(String message) throws RemoteException {
        System.out.println("Client: " + message);
        @SuppressWarnings("resource")
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter your message: ");
        return scanner.nextLine();
    }
}
