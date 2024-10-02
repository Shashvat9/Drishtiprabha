<?php   session_start(); ?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/reg_form.css">
    <title>Login</title>
</head>
<body>
    
   
    <form  method="POST">
      <div class="wrapper">
         <div class="title">
           Login
         </div>
         <div class="form">
             <div class="inputfield">
               <label>Email</label>
               <input type="email" class="input" placeholder="abc@gmail.com" name="Email" required>
            </div>  
            
            <div class="inputfield">
             <label>Password </label>
             <input type="password" class="input" minlength="0" maxlength="14" placeholder="Enter Password" name="Password" required>
          </div>
           
            
   
           <div class="inputfield">
             <input type="submit" value="Login" class="btn" required name="submit">
           </div>
          <center>
            <label>New User</label> 
            <a href="Signup.php">Sign Up</a>
          </center>
         </div>
     </div>
    </form>
</body>
</html>

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
            echo '<script>alert("Wrong Password Or username")</script>';
            // echo "wrong pass";
            break;
          case 3:
            echo '<script>alert("Username Does not Exist")</script>';
            // echo "User Doesn't Exist";
            break;
            case 4:
              echo '<script>alert("Data base problem")</script>';
                // echo "db Problem";
                break;
            default: 
            echo "Server Error";
            # code...
            break;
        }
      }

?>