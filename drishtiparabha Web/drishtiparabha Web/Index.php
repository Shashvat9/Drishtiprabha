<!DOCTYPE html>
<html lang="en">
    <head>
        <link rel="stylesheet" href="css/index.css">
    </head>
<body>
    <form action="" method="POST">
        <input type="submit" name="signin" id="" value="Login">
        <input type="submit" name="signup" id="" value="Register">
    </form>
</body>
</html>

<?php
    if(isset($_POST["signin"]))
    {
        header("location:signin.php");
    }
    if(isset($_POST["signup"]))
    {
        header("location:signup.php");
    }
?>