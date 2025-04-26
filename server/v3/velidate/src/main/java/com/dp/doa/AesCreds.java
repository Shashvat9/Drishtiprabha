package com.dp.doa;

import javax.persistence.*; // Or javax.persistence.* for older JPA versions

/**
 * Represents the 'aes_creds' table, storing AES keys and IVs associated with users.
 * IMPORTANT SECURITY NOTE: Storing raw cryptographic keys directly in the database
 * might carry security risks depending on your threat model and access controls.
 * Consider key management best practices and potentially using a dedicated Key Management Service (KMS).
 */
@Entity
@Table(name = "aes_creds")
public class AesCreds {

    /**
     * Primary key for the AES credentials record. Auto-incremented by the database.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Matches auto_increment
    @Column(name = "key_id", unique = true, nullable = false)
    private Integer keyId;

    @Column(name = "user_id", unique = true, nullable = false)
    private Integer userId; // This is the ID of the user associated with these credentials


    /**
     * The AES key, stored as a string.
     * Note: The column name "key" is a reserved SQL keyword, so it's escaped
     * using backticks in the @Column annotation's 'name' attribute.
     * The Java field name 'aesKey' avoids using the reserved keyword in code.
     */
    @Column(name = "`key`", nullable = false, length = 256) // Escape reserved keyword 'key'
    private String aesKey; // Use a non-reserved field name in Java

    /**
     * The Initialization Vector (IV) used with the AES key, stored as a string.
     */
    @Column(name = "iv", nullable = false, length = 256)
    private String iv;

    // --- Constructors ---

    /**
     * Default constructor required by JPA.
     */
    public AesCreds() {
    }

    /**
     * Convenience constructor to create an instance with initial values.
     *
     * @param userId The ID of the associated user.
     * @param aesKey The AES key string.
     * @param iv     The Initialization Vector (IV) string.
     */
    public AesCreds(Integer userId, String aesKey, String iv) {
        this.userId = userId;
        this.aesKey = aesKey;
        this.iv = iv;
    }

    // --- Getters and Setters ---

    public Integer getKeyId() {
        return keyId;
    }

    // No setter for keyId as it's database-generated
    // public void setKeyId(Integer keyId) { this.keyId = keyId; }

    public String getAesKey() {
        return aesKey;
    }

    public void setAesKey(String aesKey) {
        this.aesKey = aesKey;
    }

    public String getIv() {
        return iv;
    }

    public void setIv(String iv) {
        this.iv = iv;
    }



}

