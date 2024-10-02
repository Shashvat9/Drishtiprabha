<?php 
    include "conn.php";
    include "libraryx.php";

    $api_key_value="dp123";

    if (strtoupper($_SERVER["REQUEST_METHOD"]) == "POST") {
        $json_st = $_POST["json"];
        $json = json_decode($json_st, true);
        $api_key = $json["api_key"];
        
        if (getdata($api_key) == $api_key_value) {
            if (isset($_POST["validate"])) {
                validate($json["email"], $json["password"]);
            }

            if (isset($_POST["add_user"])) {
                add_user($json["name"], $json["email"], $json["mobile"], $json["password"]);
            }

            if (isset($_POST["get_loc"])) {
                get_from_location($json["type"],$json["email"]);
            }
            if (isset($_POST["set_flag"])) {
                set_flag($json["id"]);
            }
            if(isset($_POST["send_mail_otp"]))
            {
                send_mail_otp($json["email"]);
            }
        } else {
            echo "wrong api key";
        }
    } 
    else {
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

    function validate($email,$password)
    {
        //  code = 1 > success > print a email
        //  code = 2 > wrong password
        //  code = 3 > no rows or no user with that email
        //  code = 4 > db connection problame
        
        
        include "conn.php";
        $select = "SELECT * FROM user WHERE email = '$email';";
        $select_fire = mysqli_query($con,$select);
        if(isset($select_fire))
        {
            if(mysqli_num_rows($select_fire)>0)
            {
                $select_arr = mysqli_fetch_assoc($select_fire);
                if($password==$select_arr["password"])
                {
                    //success
                    json_send(1,$select_arr["email"]);
                }
                else
                {
                    //wrong password
                    json_send(2,"wrong password");
                }
            }
            else
            {
                // no rows found
                json_send(3,mysqli_error($con));

            }
        }
        else
        {
            // error in db connection
            json_send(4,mysqli_error($con));
        }
    }

    function add_user($name, $email, $mobile, $password)
{
    // code = 5 > success
    // code = 6 > user added
    // code = 7 > error

    include "conn.php";

    $select = "SELECT * FROM user WHERE email = '$email';";
    $result = mysqli_query($con, $select);

    if ($result) {
        $count = mysqli_num_rows($result);
        if ($count > 0) {
            json_send(5, "This email already exists");
        } else {
            $insert = "INSERT INTO user (name, email, mobile, password) VALUES ('$name', '$email', '$mobile', '$password');";
            $fire_insert = mysqli_query($con, $insert);
            if ($fire_insert) {
                // Success
                json_send(6, "User added");
            } else {
                // Error in query execution
                json_send(7, "Error in query execution: " . mysqli_error($con));
            }
        }
    } else {
        // Error in SELECT query
        json_send(200, "Error in SELECT query: " . mysqli_error($con));
    }
}


    function get_from_location($type,$email)
    {
        if(strtoupper($type)=="LAST")
        {
            last_loc();
        }
        elseif (strtoupper($type)=="UNREAD")
        {
            unread();
        }
        elseif (strtoupper($type)=="ALL")
        {
            all_loc($email);
        }
    }
// TODO: add email check for all the location type
    function last_loc()
    {
         // code = 8 > last location
        // code = 9 > error

        include "conn.php";

            $select = "SELECT * FROM location WHERE id = (SELECT MAX(id) FROM location);";
            $result = mysqli_query($con, $select);
            if(isset($result))
            {
                // echo "hi";
                $select_arr = mysqli_fetch_assoc($result);
                $json_arr = array("code"=>8,"id"=>$select_arr["id"],"longitude"=>$select_arr["longitude"],"latitude"=>$select_arr["latitude"],"time"=>$select_arr["timest"],"flag"=>$select_arr["flag"]);
                $json=json_encode(($json_arr));
                echo $json;
            }
            else
            {
                json_send(9,"error in query exeqution");
            }
    }

    function unread()
    {
         // code = 10 > done
        // code = 11 > error

        include "conn.php";
            $json=array();
            $select = "SELECT * FROM location WHERE flag = 0 ORDER BY id ASC;";
            $result = mysqli_query($con, $select);
            if(isset($result))
            {
                
                // echo "hi";
                while($row=mysqli_fetch_assoc($result))
                {
                    $json_arr=array("id"=>$row["id"],"longitude"=>$row["longitude"],"latitude"=>$row["latitude"],"time"=>$row["timest"]);
                    array_push($json,$json_arr);
                }
                
                $json_with_code=array("code"=>"10");
                array_push($json_with_code,$json);
                $jsonstring=json_encode($json_with_code);
                echo $jsonstring;
            }
            else
            {
                json_send(11,"error in query exeqution");
            }
    }
        
    function all_loc($email)
    {
        // code = 12 > done
        // code = 13 > erro
        include "conn.php";
        $json=array();

        $select_d_id = "SELECT d_id FROM user_device_map WHERE email = '$email';";
        $result_d_id = mysqli_query($con, $select_d_id);
        $d_id = mysqli_fetch_assoc($result_d_id)["d_id"];
        $select_location = "SELECT * FROM `location` WHERE d_id = $d_id ORDER BY id ASC;";
        $result = mysqli_query($con, $select_location);
        if(isset($result))
        {
            // echo "hi";
            while($row=mysqli_fetch_assoc($result))
            {
                $json_arr=array("id"=>$row["id"],"longitude"=>$row["longitude"],"latitude"=>$row["latitude"],"time"=>$row["timest"],"flag"=>$row["flag"]);
                array_push($json,$json_arr);
            }
            $json_with_code=array("code"=>"12");
            array_push($json_with_code,$json);
            $jsonstring=json_encode($json_with_code);
            echo $jsonstring;
        }
        else
        {
            json_send(13,"error in query exeqution");
        }   
    }

    function set_flag($id)
    {
        include "conn.php";

        $selec123t = "SELECT * FROM location WHERE id = '$id';";
        $result_select = mysqli_query($con, $selec123t);
        if(isset($result_select))
        {
            $row_select = mysqli_fetch_assoc($result_select);
            if(!isset($row_select["id"]))
            {
                echo $id;
                $set="UPDATE TABLE location SET flag='1' WHERE id='$id';";
                $result=mysqli_query($con,$set);
                if(isset($result))
                {
                    json_send(14,"flag has been set");
                }
                else
                {
                    json_send(15,"there has been error for set flag");
                }
            }
            else
            {
                json_send(16,"no such id exists");
            }
        }
        else
        {
            json_send(17,"error in query exeqution");
        }
    }

    function send_mail_otp($email)
    {
        $otp = rand(100000,999999);
        $message = "This is your otp : ".$otp;

        $obmail= new mail_to_send("vidya.gmit@gmail.com","uwrxrdoyqcrbgecb");
        try{
            $obmail->send_email($email,"OTP",$message);
            json_send(18,$otp);
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