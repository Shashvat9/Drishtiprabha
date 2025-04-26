package com.dp.utils;

import com.dp.doa.User;
import org.hibernate.Session;
import org.hibernate.SessionFactory;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;

public class UserBuilder {

    public static boolean isUserExists(String email, SessionFactory sessionFactory) {
        Session session = sessionFactory.openSession();
        session.beginTransaction();
        // Check if the user already exists in the database
        String emailDigest = AesCrypto.digest(email, "SHA-256");
        String hql = "FROM User WHERE emailLookup = :emailDigest";
        List<User> users = session.createQuery(hql, User.class)
                .setParameter("emailDigest", emailDigest)
                .getResultList();
        session.getTransaction().commit();
        session.close();
        return !users.isEmpty();
    }


    public static User build(String emailPt,String email, String name, String mobile, String password) {
        String hashedPassword = AesCrypto.digest(password,"SHA-512");
        String emailLookup = AesCrypto.digest(emailPt,"SHA-256");
//        try {
////            MessageDigest md = MessageDigest.getInstance("SHA-512");
////            md.digest(password.getBytes());
////            hashedPassword = new String(md.digest());
//
////            MessageDigest mdLookup = MessageDigest.getInstance("SHA-512");
////            mdLookup.update(email.getBytes());
////            emailLookup = new String(mdLookup.digest());
//        }
//        catch (NoSuchAlgorithmException e) {
//            throw new RuntimeException("Error hashing password", e);
//        }
        return new User(email, name, mobile, hashedPassword,emailLookup);
    }
}
