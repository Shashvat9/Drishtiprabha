<?php
    $hostname="localhost";
    $uname="shashvat";
    $dbname="drishtiprabha";
    $password_db="shashvat@DP";

    $con=mysqli_connect($hostname,$uname,$password_db,$dbname);
    if($con->connect_error)
    {
        echo mysqli_connect_error();
    }
?>