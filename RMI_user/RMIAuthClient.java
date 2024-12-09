import java.rmi.Naming;
import java.util.Scanner;

public class RMIAuthClient {
    public static void main(String[] args) {
        // String host = "127.0.0.1"; // Server address
        // int port = 5080;

        try {
            // Look up the remote object
            AuthService authService = (AuthService) Naming.lookup("rmi://localhost:5080/AuthService");

            // Get email and password from user
            Scanner scanner = new Scanner(System.in);
            System.out.print("Enter email: ");
            String email = scanner.nextLine();
            System.out.print("Enter password: ");
            String password = scanner.nextLine();

            // Verify credentials (email + password)
            String response = authService.verifyCredentials(email, password);

            // Display server response
            System.out.println("Server Response: " + response);

            // If the password was incorrect, keep asking until successful login
            while (response.equals("Wrong password. Try again")) {
                System.out.print("Enter password again: ");
                password = scanner.nextLine();
                response = authService.verifyCredentials(email, password);
                System.out.println("Server Response: " + response);
            }

            scanner.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
