<?php   session_start(); ?>
<?php

    include "myMethods.php";

    if(isset($_POST['submit']))
    {
        $pass=$_POST['Password'];
        $email=$_POST['Email'];

        $getArr=sendRequest(setJsonValidate($email,$pass));
        
        
        // print_r($getArr);
        // if($getArr["code"]==1)
        // {
        //   echo "Done";
        // }
        // else
        // {
        //   echo "Not Done";
        // }
        switch ($getArr["code"]) {
          case 1:
            // echo  "Done";
            $_SESSION["email"]=$getArr["message"];
            echo '<script>window.location = "location.php";</script>';
            break;
          case 2:
            echo '<script>window.location = "login.html"; alert("Wrong Password Or username")</script>';
            // echo "wrong pass";
            break;
          case 3:
            echo '<script>window.location = "login.html";alert("Username Does not Exist")</script>';
            // echo "User Doesn't Exist";
            break;
            case 4:
              echo '<script>window.location = "login.html";alert("Data base problem")</script>';
                // echo "db Problem";
                break;
            default: 
            echo "Server Error";
            # code...
            break;
        }
      }

?>