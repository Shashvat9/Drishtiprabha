
<?php

    include "myMethods.php";

    // if(isset($_POST['submit']))
    // {
        $name=$_POST['Name'];
        $Mob=$_POST['Mobile_No'];
        $pass=$_POST['password'];
        $email=$_POST['Email'];

        print_r($_POST);

        $getArr=sendRequest(setJsonAdd_User($name,$Mob,$email,$pass));
        
        
        print_r($getArr);
        // if($getArr["code"]==1)
        // {
        //   echo "Done";
        // }
        // else
        // {
        //   echo "Not Done";
        // }
        switch ($getArr["code"]) {
          case 5:
            echo '<script>alert("User Exist")</script>';
            echo '<script>window.location = "login.html";</script>';
            // echo "User Exist";
            break;
          case 6:
            // echo  "Done";
            $_SESSION["email"]=$getArr["message"];
            echo '<script>window.location = "location.php";</script>';
            break;
            case 7:
              echo '<script>alert("Data base problem")</script>';
              // echo "db Problem";
              break;
              default: 
              // echo "";
              echo '<script>alert("Server Error")</script>';
            # code...
            break;
        }
      // }

?>