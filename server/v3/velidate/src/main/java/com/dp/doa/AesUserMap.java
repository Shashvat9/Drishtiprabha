package com.dp.doa;

import javax.persistence.*; // Or javax.persistence.* for older JPA versions

/**
 * Represents the 'aes_user_map' table, which maps user IDs to AES credential IDs.
 * This acts as a join table between the 'user' table and the 'aes_creds' table.
 */
@Entity
@Table(name = "aes_user_map")
public class AesUserMap {

    /**
     * Primary key for the mapping record. Auto-incremented by the database.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Matches auto_increment
    @Column(name = "id", unique = true, nullable = false) // Primary keys cannot be null
    private Integer id;

    /**
     * The ID of the user being mapped.
     * This likely corresponds to the 'id' column in the 'user' table.
     * The schema allows this to be null.
     */
    @Column(name = "user_id") // nullable = true is the default
    private Integer userId;

    /**
     * The ID of the AES credential being mapped.
     * This likely corresponds to the 'key_id' column in the 'aes_creds' table.
     * The schema allows this to be null.
     */
    @Column(name = "aes_id") // nullable = true is the default
    private Integer aesId;

    // --- Constructors ---

    /**
     * Default constructor required by JPA.
     */
    public AesUserMap() {
    }

    /**
     * Convenience constructor to create an instance with initial values.
     *
     * @param userId The ID of the user.
     * @param aesId  The ID of the AES credential record.
     */
    public AesUserMap(Integer userId, Integer aesId) {
        this.userId = userId;
        this.aesId = aesId;
    }

    // --- Getters and Setters ---

    public Integer getId() {
        return id;
    }

    // No setter for id as it's database-generated
    // public void setId(Integer id) { this.id = id; }

    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    public Integer getAesId() {
        return aesId;
    }

    public void setAesId(Integer aesId) {
        this.aesId = aesId;
    }

    // --- toString, equals, hashCode (Optional but Recommended) ---

//    @Override
//    public String toString() {
//        return "AesUserMap{" +
//                "id=" + id +
//                ", userId=" + userId +
//                ", aesId=" + aesId +
//                '}';
//    }
//
//    @Override
//    public boolean equals(Object o) {
//        if (this == o) return true;
//        if (o == null || getClass() != o.getClass()) return false;
//
//        AesUserMap that = (AesUserMap) o;
//
//        // Use id for equality check if it's already persisted (non-null)
//        if (id != null ? !id.equals(that.id) : that.id != null) return false;
//        // If id is null (not persisted yet), rely on other fields or object identity
//        return id != null; // Basic implementation relies on id once set.
//    }
//
//    @Override
//    public int hashCode() {
//        // Use id for hashCode if it's set
//        return id != null ? id.hashCode() : super.hashCode();
//    }
}
