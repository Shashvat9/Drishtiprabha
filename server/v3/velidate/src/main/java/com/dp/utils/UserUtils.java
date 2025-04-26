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
        String hql = "SELECT User.password FROM User WHERE emailLookup = :emailDigest";
        List<User> users = session.createQuery(hql, User.class)
                .setParameter("emailDigest", emailDigest)
                .getResultList();
        session.getTransaction().commit();
        session.close();
        return !users.isEmpty();
    }

    private String getUserPassword(String email) {
        String password;
        Session sessionPass = sessionFactory.openSession();
        sessionPass.beginTransaction();
        // Check if the user already exists in the database
        String emailDigest = AesCrypto.digest(email, "SHA-256");

        String getPassword = "SELECT User .password FROM User WHERE emailLookup = :emailDigest";
        List<User> users = sessionPass.createQuery(getPassword, User.class)
                .setParameter("emailDigest", emailDigest)
                .getResultList();

        password = users.getFirst().getPassword();
        sessionPass.getTransaction().commit();
        sessionPass.close();

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

        return password;
    }
    public boolean validateUser(String email, String password) {
        if(!isUserExists(email)){
            throw new RuntimeException("User does not exist");
        }
        String storedPassword = getUserPassword(email);
        return password.equals(storedPassword);
    }

}
