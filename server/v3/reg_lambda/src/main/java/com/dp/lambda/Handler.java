package com.dp.lambda;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.dp.doa.AesCreds;
import com.dp.doa.User;
import com.dp.utils.AesCrypto;
import com.dp.utils.UserBuilder;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

import java.util.Arrays;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

public class Handler implements RequestHandler<Map<String, String>, Map<String, String>> {

    @Override
    public Map<String, String> handleRequest(Map<String, String> event, Context context) {
        AesCrypto aesCrypto = new AesCrypto();
        HashMap<String, String> response = new HashMap<>();

        // Configure Hibernate

        SessionFactory sessionFactoryGet = null;
        Session sessionGet = null;


//        Get Session
        Configuration configuration = new Configuration().configure()
                .addAnnotatedClass(User.class)
                .addAnnotatedClass(AesCreds.class);
        sessionFactoryGet = configuration.buildSessionFactory();

        sessionGet = sessionFactoryGet.openSession();
//        sessionGet.beginTransaction();

//        insert session
        SessionFactory sessionFactoryPut = null;
        Session sessionPut = null;
        sessionFactoryPut = configuration.buildSessionFactory();

        sessionPut = sessionFactoryPut.openSession();


        try {
            // Encrypt input data
            String email = aesCrypto.encrypt(event.get("email"), aesCrypto.getSecretKey(), aesCrypto.getIv());
            String name = aesCrypto.encrypt(event.get("name"), aesCrypto.getSecretKey(), aesCrypto.getIv());
            String mobile = aesCrypto.encrypt(event.get("mobile"), aesCrypto.getSecretKey(), aesCrypto.getIv());
            String password = event.get("password");

            // Build User object
            User user = UserBuilder.build(event.get("email"),email,name,mobile,password);



            // Open session and begin transaction


            // Check if user exists
            if (UserBuilder.isUserExists(event.get("email"), sessionFactoryGet)) {
                response.put("statusCode", "201");
                response.put("body", "User already exists");
                sessionGet.getTransaction().rollback();
                return response;
            }

            sessionPut.beginTransaction();
            // Save user and commit transaction
            sessionPut.save(user);
            sessionPut.flush();
            sessionPut.getTransaction().commit();
            sessionPut.close();

            // Open a new session for subsequent operations
            sessionGet = sessionFactoryGet.openSession();
            sessionGet.beginTransaction();

            // Retrieve user ID
            String getIdHql = "FROM User WHERE email = :email";
            User userId = sessionGet.createQuery(getIdHql, User.class)
                    .setParameter("email", email)
                    .getSingleResult();

            // Save AesCreds
            String encodedKey = Base64.getEncoder().encodeToString(aesCrypto.getSecretKey().getEncoded());
            String encodedIv = Base64.getEncoder().encodeToString(aesCrypto.getIv().getIV());
            AesCreds aesCreds = new AesCreds(userId.getId(),encodedKey,encodedIv);

            sessionPut = sessionFactoryPut.openSession();
            sessionPut.beginTransaction();
            sessionPut.save(aesCreds);

            // Commit transaction
            sessionPut.getTransaction().commit();

            response.put("statusCode", "200");
            response.put("body", "User created successfully");
//            response.put("userId", String.valueOf(userId.getId()));
        } catch (Exception e) {
            if (sessionPut.getTransaction() != null && sessionPut.getTransaction().isActive()) {
                sessionPut.getTransaction().rollback();
            } else if (sessionGet.getTransaction() != null && sessionGet.getTransaction().isActive()) {
                sessionGet.getTransaction().rollback();
            }
            response.put("statusCode", "500");
            response.put("body", "An error occurred: " + e.getMessage()+"\n stack tress:"+ Arrays.toString(e.getStackTrace()));
        } finally {
            if (sessionPut != null) {
                sessionPut.close();
            } else if (sessionGet !=null) {
                sessionGet.close();
            }
        }

        return response;
    }
}