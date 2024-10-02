<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/reg_form.css">
    <title>Sign Up</title>
</head>
<body>
    
   
    <form action="" method="POST">
      <div class="wrapper">
         <div class="title">
           Sign up
         </div>
         <div class="form">
            <div class="inputfield">
               <label> Creat Username </label>
               <input type="text" class="input" placeholder="Enter Userame" name="Name" required>
            </div>  
            <div class="inputfield">
                <label>Phone Number</label>
                <input type="number" class="input" maxlength="10" onKeyPress="if(this.value.length==10) return false" placeholder="+91xxxxxxxxxx" name="Mobile_No" required>
             </div> 
             <div class="inputfield">
               <label>Email</label>
               <input type="email" class="input" placeholder="abc@gmail.com" name="Email" required>
            </div>  
            
            <div class="inputfield">
             <label>Password </label>
             <input type="password" class="input" minlength="2" maxlength="14" placeholder="Enter Password" name="password" required>
          </div>
         
           <div class="inputfield">
             <input type="submit" value="SignUp" class="btn" required name="submit">
             
           </div>
           <center>
            <label>Already User</label> 
            <a href="Signin.php">Sign in</a>
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
        $name=$_POST['Name'];
        $Mob=$_POST['Mobile_No'];
        $pass=$_POST['password'];
        $email=$_POST['Email'];

        $getArr=sendRequest(setJsonAdd_User($name,$Mob,$email,$pass));
        
        
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
          case 5:
            echo '<script>alert("User Exist")</script>';
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
      }

?>