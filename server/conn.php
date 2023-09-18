<?php
    $hostname="localhost";
    $uname="id20839964_shashvat";
    $dbname="id20839964_drishtiprabha_db";
    $password_db="Shashvat.Raj200399";

    $con=mysqli_connect($hostname,$uname,$password_db,$dbname);
    if($con->connect_error)
    {
        echo mysqli_connect_error();
    }
?>