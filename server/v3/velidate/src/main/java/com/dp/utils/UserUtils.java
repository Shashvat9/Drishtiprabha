package com.dp.utils;

import com.dp.doa.AesCreds;
import com.dp.doa.User;
import org.hibernate.Session;
import org.hibernate.SessionFactory;

import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;
import java.util.List;
import java.util.Objects;

public class UserUtils {

    SessionFactory sessionFactory;

    public  UserUtils(SessionFactory sessionFactory) {
        this.sessionFactory = sessionFactory;
    }

    public boolean isUserExists(String email) {
        Session session = sessionFactory.openSession();
        session.beginTransaction();
        // Check if the user already exists in the database
        String emailDigest = AesCrypto.digest(email, "SHA-256");
        System.out.println("digest"+emailDigest);
        String hql = "SELECT 1 FROM User u WHERE u.emailLookup = :emailDigest";
        List<?> users = session.createQuery(hql)
                .setParameter("emailDigest", emailDigest)
                .setMaxResults(1)
                .getResultList();
        session.getTransaction().commit();
        session.close();
        return !users.isEmpty();
    }

    private String getUserPassword(String email) {
        String password = null; // Initialize to null
        Session session = null; // Use a more descriptive name like 'session'
        try {
            session = sessionFactory.openSession();
            session.beginTransaction();

            // Generate the digest in the same raw format used for storage
            String emailDigest = AesCrypto.digest(email, "SHA-256");

            // --- CORRECTED HQL: Select the password field ---
            String hql = "SELECT u.password FROM User u WHERE u.emailLookup = :emailDigest";

            // --- Execute query, expecting a List of Strings ---
            List<String> passwords = session.createQuery(hql, String.class) // Expect String.class
                    .setParameter("emailDigest", emailDigest)
                    .setMaxResults(1) // We only expect one result
                    .getResultList();

            session.getTransaction().commit(); // Commit transaction

            // Check if the list is not empty before trying to access it
            if (!passwords.isEmpty()) {
                password = passwords.get(0); // Get the first (and only) password string
            } else {
                System.out.println("No user found with matching email digest for email: " + email);
                // password remains null
            }

        } catch (Exception e) {
            // Rollback transaction on error
            if (session != null && session.getTransaction() != null && session.getTransaction().isActive()) {
                try { session.getTransaction().rollback(); } catch (Exception rbEx) { System.err.println("Rollback failed: " + rbEx.getMessage()); }
            }
            // Log the error and rethrow
            System.err.println("Error retrieving password for email [" + email + "]: " + e.getMessage());
            e.printStackTrace();
            // Rethrowing indicates failure to the calling method
            throw new RuntimeException("Failed to retrieve user password", e);
        } finally {
            // Ensure the session is always closed
            if (session != null && session.isOpen()) {
                session.close();
            }
        }

        return password; // Return the retrieved password (or null if not found)

//        Session sessionKey = sessionFactory.openSession();
//        sessionKey.beginTransaction();
//        String getKeyIv = "SELECT a.key, a.iv FROM AesCreds a LEFT JOIN User u ON a.userId = u.id WHERE u.emailLookup = :emailDigest";
//        List<AesCreds> aesCreds = sessionPass.createQuery(getKeyIv, AesCreds.class)
//                .setParameter("emailDigest", emailDigest)
//                .getResultList();
//
//        org.apache.commons.codec.binary.Base64 base64 = new org.apache.commons.codec.binary.Base64();
//
//
//        SecretKey key = AesCrypto.convertBytesToSecretKey(base64.decode(aesCreds.getFirst().getKey().getBytes()), "AES");
//        IvParameterSpec iv = new IvParameterSpec(base64.decode(aesCreds.getFirst().getIv().getBytes()));
//
//        sessionKey.getTransaction().commit();
//        sessionKey.close();
//
//        // Decrypt the password using the key and iv
//        AesCrypto aesCrypto = new AesCrypto();
//        String decryptedPassword;
//        try{
//            decryptedPassword = aesCrypto.decrypt(password, key, iv);
//        }
//        catch (Exception e) {
//            throw new RuntimeException("Error decrypting password", e);
//        }
//        return decryptedPassword;

//        return password;
    }
    public boolean validateUser(String email, String password) {
        String storedHash = getUserPassword(email);

        if (storedHash == null) {
            // User does not exist or password hash couldn't be retrieved
            System.out.println("Validation failed: User not found or password hash missing for email [" + email + "]");
            return false;
        }

        // 2. Calculate the SHA-512 hash of the password provided during login
        //    Use the same AesCrypto.digest method that was used for storage.
        String inputPasswordHash = AesCrypto.digest(password, "SHA-512");

        // 3. Compare the calculated hash with the stored hash
        //    Use Objects.equals for null-safety, although storedHash shouldn't be null here.
        boolean isValid = Objects.equals(inputPasswordHash, storedHash);

        System.out.println("Validation result for email [" + email + "]: " + isValid);
        // For debugging (REMOVE in production):
        // System.out.println("Stored Hash: " + storedHash);
        // System.out.println("Input Hash : " + inputPasswordHash);

        return isValid;
    }

}
