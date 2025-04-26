package com.dp.doa;

import javax.persistence.*;

@Entity
@Table(name = "user")
public class User {

    // This 'id' is managed by the database (auto_increment) but is NOT the primary key.
    // insertable=false, updatable=false means Hibernate won't try to set it on insert/update.
    @Column(name = "user_id", unique = true, insertable = false, updatable = false)
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id; // Populated by the DB after insert

    @Id // email is the actual primary key
    @Column(name = "email", unique = true, nullable = false, length = 255)
    private String email;

    @Column(name = "name", length = 255)
    private String name;

    @Column(name = "mobile", length = 20)
    private String mobile;

    @Column(name = "password", length = 255)
    private String password; // IMPORTANT: Store securely (hashed)! Never store plain text.

    @Column(name = "email_lookup",length = 300)
    private String emailLookup; // This is a hashed version of the email for lookup purposes

    // --- Standard Constructors, Getters, and Setters ---

    public User() {
        // Default constructor
    }

    // Optional: Constructor for easier object creation (excluding DB-generated id)
    public User(String email, String name, String mobile, String password,String emailLookup) {
        this.email = email;
        this.name = name;
        this.mobile = mobile;
        this.password = password;
        this.emailLookup = emailLookup;
    }


    public Integer getId() {
        return id;
    }
    // No setter for id, as it's DB generated and not the PK

    private String getEmail() {
        return email;
    }

    private void setEmail(String email) {
        this.email = email;
    }

    private String getName() {
        return name;
    }

    private void setName(String name) {
        this.name = name;
    }

    private String getMobile() {
        return mobile;
    }

    private void setMobile(String mobile) {
        this.mobile = mobile;
    }

    private String getPassword() {
        // Consider if you ever want to expose the password hash via getter
        return password;
    }

    private void setPassword(String password) {
        // IMPORTANT: Ensure this password is HASHED before being set
        this.password = password;
    }

//    @Override
//    public String toString() {
//        return "User{" +
//                "id=" + id +
//                ", email='" + email + '\'' +
//                ", name='" + name + '\'' +
//                ", mobile='" + mobile + '\'' +
//                // Avoid logging password hash unless necessary for debugging
//                '}';
//    }



    // Consider adding equals() and hashCode() based on email (the PK)


}
