<?php 
session_start();

    if(isset($_SESSION["email"]))
    {
        unset($_SESSION["email"]);
        // echo $_SESSION["email"];
        echo '<script>window.location = "login.html";</script>';
    }
    else
    {
        echo '<script>window.location = "index.php";</script>';
    }
?>