<?php 
    include_once "conn.php";

    if($_SERVER['REQUEST_METHOD']=="POST"){
        $required_keys = ['api_key', 'd_id', 'email', 'd_name'];
        foreach ($required_keys as $key) {
            if (!isset($_POST[$key])) {
                json_send(0, "Missing required POST key: $key");
                exit;
            }
        }

        $api_key = $_POST['api_key'];
        $d_id = $_POST['d_id'];
        $email = $_POST['email'];
        $d_name = $_POST['d_name'];

        $api_key_value="dp123";
        
        if ($api_key == $api_key_value) {
            // Check if the device ID exists in the device table
            $check_device_query = "SELECT * FROM device WHERE d_id = '$d_id';";
            $check_device_result = mysqli_query($con, $check_device_query);

            if (mysqli_num_rows($check_device_result) > 0) {
                // Device ID exists, proceed with inserting into user_device_map
                $insert_mapping_table = "INSERT INTO user_device_map (d_id, email) VALUES ('$d_id', '$email');";
                $update_mapping_table_fire = mysqli_query($con, $insert_mapping_table);
            } else {
                // Device ID does not exist
                json_send(0, "Device ID does not exist");
                exit;
            }
            if($update_mapping_table_fire){
                $update_device = "UPDATE device SET device_name = '$d_name' WHERE d_id = '$d_id';";
                $update_device_fire = mysqli_query($con,$update_device);
                if($update_device_fire){
                    json_send(1,"Device ID updated successfully");
                }
                else{
                    json_send(0,"Device ID updation failed");
                }
            }else{
                json_send(0,"Device ID updation failed");
            }
        }
    }
    elseif($_SERVER['REQUEST_METHOD']=="GET"){
        $required_keys = ['api_key','email'];
        foreach ($required_keys as $key) {
            if (!isset($_GET[$key])) {
                json_send(0, "Missing required POST key: $key");
                exit;
            }
        }
        $select_from_user_device_map = "SELECT * FROM user_device_map WHERE email = '$email'";
        echo $select_from_user_device_map;
        $select_from_user_device_map_fire = mysqli_query($con,$select_from_user_device_map);
        $data = mysqli_fetch_assoc($select_from_user_device_map_fire);
        print_r($data);
        if($data){
            $json_send(1,$data);
        }
        else{
            json_send(1,"No data found");
        }
    }
    else{
        json_send(0,"Invalid request method");
    }

    function json_send($code,$message)
    {
        $json_arr=array("code"=>$code,"message"=>$message);
        $json=json_encode($json_arr);
        echo $json;
    }
?>