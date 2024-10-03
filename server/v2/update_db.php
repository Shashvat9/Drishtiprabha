<?php 
    include "conn.php";
    include "libraryx.php";


    $api_key_value="dp123";

    if(strtoupper($_SERVER["REQUEST_METHOD"])=="GET")
    {
        if(getdata($_GET["api_key"])==$api_key_value)
        {
            $longitude=getdata($_GET["longitude"]);
            $latitude=getdata($_GET["latitude"]);
            $d_id = getdata($_GET["d_id"]);
            $time=date('m/d/Y h:i:s ', time());;

            $insert="INSERT INTO location (longitude,latitude,d_id) VALUES ('$longitude','$latitude','$d_id')";
            $fire_insert=mysqli_query($con,$insert);
            if(!$fire_insert)
            {
                echo "error: ". mysqli_error($con);
            }
            else
            {
                $get_email = "SELECT email FROM user_device_map WHERE d_id = '$d_id'";
                $fire_get_email = mysqli_query($con, $get_email);
                $row = mysqli_fetch_assoc($fire_get_email);
                $email = $row['email'];

                $obmail= new mail_to_send("vidya.gmit@gmail.com","uwrxrdoyqcrbgecb");
                try{
                    $obmail->send_email($email,"ALERT","i need help at: "."https://www.google.com/maps/search/".$latitude.",".$longitude);
                    json_send(18,"email send");
                }
                catch(PHPMailer\PHPMailer\Exception $e)
                {
                    $errorArr = explode(":",$e->getMessage());
                    if($errorArr[0]=="Invalid address ".$email)
                    {
                        json_send(19,"wrong email");
                    }
                    else
                    {
                        json_send(20,"cant send email");
                    }
                }
            }
        }
        else
        {
            json_send(500,"wrong api key");
        }
    }
    else
    {
        echo "wrong request. error code = ". http_response_code();
        echo error_get_last();
    }

    function getdata($data)
    {
        $data = trim($data);
        $data = stripslashes($data);
        $data = htmlspecialchars($data);
        return $data;
    }

    function send_mail_otp($email)
    {
        $obmail= new mail_to_send("vidya.gmit@gmail.com","uwrxrdoyqcrbgecb");
        try{
            $obmail->send_email($email,"ALERT","i need help at: "."https://www.google.com/maps/search/".$latitude.",".$longitude);
            json_send(18,"otp sent");
        }
        catch(PHPMailer\PHPMailer\Exception $e)
        {
            $errorArr = explode(":",$e->getMessage());
            if($errorArr[0]=="Invalid address")
            {
                json_send(19,"wrong email");
            }
            else
            {
                json_send(20,"cant send email");
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