package com.dp.utils;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Base64;

public class AesCrypto {
    public static final String AES_CIPHER_ALGORITHM = "AES/CBC/PKCS5Padding";

    public SecretKey secretKey;
    public IvParameterSpec iv;

    public SecretKey getSecretKey() {
        return secretKey;
    }

    public IvParameterSpec getIv() {
        return iv;
    }

    public static SecretKey convertBytesToSecretKey(byte[] keyBytes, String algorithm) {
        return new SecretKeySpec(keyBytes, algorithm);
    }

    public String encrypt(String plainText, SecretKey secretKey, IvParameterSpec iv) throws Exception {
        Cipher cipher = Cipher.getInstance(AES_CIPHER_ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, iv);
        byte[] encryptedBytes = cipher.doFinal(plainText.getBytes());
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }

    public String decrypt(String cipherText, SecretKey secretKey, IvParameterSpec iv) throws Exception {
        Cipher cipher = Cipher.getInstance(AES_CIPHER_ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, secretKey, iv);
        byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(cipherText));
        return new String(decryptedBytes);
    }

    public void keyGenerator() {
        SecretKey secretKey;

        try{
            // Generate a new secret key
            KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
            keyGenerator.init(256);
            secretKey = keyGenerator.generateKey();
        }catch (NoSuchAlgorithmException e){
            throw new RuntimeException("Error generating AES key", e);
        }

        // Generate a random IV
        byte[] ivBytes = new byte[16];
        SecureRandom secureRandom = new SecureRandom();
        secureRandom.nextBytes(ivBytes);
        IvParameterSpec iv = new IvParameterSpec(ivBytes);
        this.secretKey = secretKey;
        this.iv = iv;

//        HashMap<String,String> keyMap = new HashMap<>();
//        keyMap.put("key", Base64.getEncoder().encodeToString(secretKey.getEncoded()));
//        keyMap.put("iv", Base64.getEncoder().encodeToString(ivBytes));
    }

    public AesCrypto() {
        keyGenerator();
    }

    public static String digest(String plainText, String algorithm) {
        try {
            MessageDigest mdLookup = MessageDigest.getInstance(algorithm);
            mdLookup.update(plainText.getBytes());
            return new String(mdLookup.digest());
        } catch (Exception e) {
            throw new RuntimeException("Error encrypting data", e);
        }
    }
}
