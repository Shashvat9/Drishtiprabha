<?php
include "conn.php";
// Get the headers sent by the client
$headers = apache_request_headers();

if(strtoupper($_SERVER["REQUEST_METHOD"])=="POST")
{
    echo "hi";
}
else
{
    // Check if the "Content-Type" header is present
if (isset($headers['Content-Type'])) {
    $contentType = $headers['Content-Type'];

    // Check the value of the "Content-Type" header
    if ($contentType === 'application/json') {
        // Read the JSON data from the request body

         $longitude=220;
            $latitude=220;

            $insert="INSERT INTO location (longitude,latitude) VALUES ('$longitude','$latitude')";
            $fire_insert=mysqli_query($con,$insert);
            if(!$fire_insert)
            {
                echo "error: ". mysqli_error($con);
            }
            else
            {
                echo "done";
            }
    }
    else
    {
        echo "error in contant type";
    }
}
else
{
    echo "error in heador";
}
}


?>
