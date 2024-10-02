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
            $insert_mapping_table = "INSERT INTO user_device_map (d_id, email) VALUES ('$d_id', '$email');";
            $update_mapping_table_fire = mysqli_query($con, $insert_mapping_table);
            $update_mapping_table_fire = mysqli_query($con,$update_mapping_table);
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

    function json_send($code,$message)
    {
        $json_arr=array("code"=>$code,"message"=>$message);
        $json=json_encode($json_arr);
        echo $json;
    }
?>