import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.sql.*;
import java.util.concurrent.ConcurrentHashMap;

public class AuthServiceImpl extends UnicastRemoteObject implements AuthService {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/userdb";
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "Sm210899@";

    // Map to store registered clients
    private ConcurrentHashMap<String, ClientInterface> onlineClients;

    public AuthServiceImpl() throws RemoteException {
        super();
        onlineClients = new ConcurrentHashMap<>();
    }

    @Override
    public String verifyCredentials(String email, String password) throws RemoteException {
        try (Connection connection = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD)) {
            String query = "SELECT * FROM users WHERE email = ? AND password = ?";
            try (PreparedStatement stmt = connection.prepareStatement(query)) {
                stmt.setString(1, email);
                stmt.setString(2, password);

                try (ResultSet rs = stmt.executeQuery()) {
                    if (rs.next()) {
                        return "Login Successful";
                    } else {
                        return "Invalid email or password.";
                    }
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
            return "Internal Server Error";
        }
    }

    @Override
    public void registerClient(String email, ClientInterface client) throws RemoteException {
        onlineClients.put(email, client);
        System.out.println(email + " has joined the chat.");
    }

    @Override
    public void sendMessage(String sender, String receiver, String message) throws RemoteException {
        ClientInterface receiverClient = onlineClients.get(receiver);
        if (receiverClient != null) {
            receiverClient.receiveMessage(sender, message);
        } else {
            System.out.println("User " + receiver + " is not online.");
        }
    }

    @Override
    public boolean verifyEmail(String email) throws RemoteException {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'verifyEmail'");
    }

    @Override
    public boolean verifyPassword(String email, String password) throws RemoteException {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'verifyPassword'");
    }
}
