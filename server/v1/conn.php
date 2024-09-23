<?php
    $hostname="localhost";
    $uname="root";
    $dbname="drishtiprabha";
    $password_db="";

    $con=mysqli_connect($hostname,$uname,$password_db,$dbname);
    if($con->connect_error)
    {
        echo mysqli_connect_error();
    }
?>