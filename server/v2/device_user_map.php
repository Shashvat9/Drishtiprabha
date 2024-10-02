<?php 
    include_once "conn.php";

    if($_SERVER['REQUEST_METHOD']=="POST"){
        $api_key = $_POST['api_key'];
        $d_id = $_POST['d_id'];
        $email = $_POST['email'];
        $d_name = $_POST['d_name'];

        $api_key_value="dp123";
        
        if (getdata($api_key) == $api_key_value) {
            $update_mapping_table = "UPDATE user_device_map SET d_id = '$d_id' WHERE email = '$email';";
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