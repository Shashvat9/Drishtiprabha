
<?php 
    include "conn.php";
    include "libraryx.php";


    $api_key_value="dp";

    if(strtoupper($_SERVER["REQUEST_METHOD"])=="GET")
    {
        if(getdata($_GET["api_key"])==$api_key_value)
        {
            $longitude=getdata($_GET["longitude"]);
            $latitude=getdata($_GET["latitude"]);
            $address = getdata($_GET["add"]);
            $time=date('m/d/Y h:i:s ', time());;

            $insert="INSERT INTO location (longitude,latitude,timest,device_address) VALUES ('$longitude','$latitude','$time','$address')";
            $fire_insert=mysqli_query($con,$insert);
            if(!$fire_insert)
            {
                echo "error: ". mysqli_error($con);
            }
            else
            {
                echo "done";
                $obmail= new mail_to_send("vidya.gmit@gmail.com","uwrxrdoyqcrbgecb");
                try{
                    $obmail->send_email("rajyagurushashvat@gmail.com","ALERT","i need help at: "."https://www.google.com/maps/search/".$latitude.",".$longitude);
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
        }
        else
        {
            echo "wrong api key";
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
?>
