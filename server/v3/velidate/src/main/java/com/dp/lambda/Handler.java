package com.dp.lambda;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.dp.doa.AesCreds;
import com.dp.doa.User;
import com.dp.utils.UserUtils;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

import java.util.HashMap;
import java.util.Map;

public class Handler implements RequestHandler<Map<String, String>, Map<String, String>> {
    @Override
    public Map<String, String> handleRequest(Map<String, String> input, Context context) {
        HashMap<String,String> result = new HashMap<>();

        Configuration configuration = new Configuration().configure()
                .addAnnotatedClass(User.class)
                .addAnnotatedClass(AesCreds.class);

        SessionFactory sessionFactory = configuration.buildSessionFactory();

        UserUtils userUtils = new UserUtils(sessionFactory);



        String email = input.get("email");
        String password = input.get("password");

        // Validate input
        if (email == null || email.isEmpty()) {
            result.put("error", "Email is required");
            return result;
        }
        if (password == null || password.isEmpty()) {
            result.put("error", "Password is required");
            return result;
        }

        if(userUtils.isUserExists(email)){
            result.put("error", "User Does not exists");
            return result;
        }

        userUtils.validateUser(email,password);
        result.put("code", "200");
        result.put("message", "User validated successfully");
        return result;
    }
}
