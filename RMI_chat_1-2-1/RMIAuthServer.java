import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

public class RMIAuthServer {
    public static void main(String[] args) {
        try {
            // Start the RMI registry on port 9080
            LocateRegistry.createRegistry(9080);
            // Create and bind the remote object
            AuthService authService = new AuthServiceImpl();
            Naming.rebind("rmi://localhost:9080/AuthService", authService);
            System.out.println("RMI Authentication Server is ready.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
