<?php
    $apiKey = "key";


    function setJsonValidate ($email,$password)
    {
        return array(
            'validate' => '1',
            'json' => '{
                "api_key":"dp123",
                "email":"'.$email.'",
                "password":"'.$password.'"
            }'
        );
    }

    function setJsonAdd_User ($name,$mobile,$email,$password)
    {
        return array(
            'add_user' => '1',
            'json' => '{
                "api_key":"dp123",
                "name":"'.$name.'",
                "mobile":"'.$mobile.'",
                "email":"'.$email.'",
                "password":"'.$password.'"
            }'
        );
    }

    function setJsonGet_Loc($type,$email)
    {
        return array(
            'get_loc' => '1',
            'json' => '{
                "api_key":"dp123",
                "type":"'.$type.'",
                "email":"'.$email.'"
            }'
        );
    }

    function sendRequest($jsonArray)
    {
        $url = 'https://3.6.71.39/api/v2/android_api.php';
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_POST, true);

        curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonArray);

        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);


        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        $response = curl_exec($ch);

        // Check for errors
        if ($response === false) {
            echo 'cURL Error: ' . curl_error($ch);
        }

        curl_close($ch);

        $jsonRes = $response;

        // echo $jsonRes;

        // $jsonAsoc = json_decode($jsonRes,true);            
        
        return json_decode($jsonRes,true);
    }

    function generateGoogleMapsLink($data) {

        // $data = json_decode($json, true);
        
        // Extracting longitude, latitude, and ID from the given JSON
        $longitude = $data[0][0]['longitude'];
        $latitude = $data[0][0]['latitude'];
        $id = $data[0][1]['id'];
        
        // Creating the Google Maps link
        $googleMapsLink = "https://www.google.com/maps/place/".$latitude.",".$longitude;
        
        
        // Displaying the link in an HTML form along with a button
        echo '<form action="' . $googleMapsLink . '" method="get">';
        echo '<input type="hidden" name="id" value="' . $id . '">';
        echo '<input type="submit" value="Print ID">';
        echo '</form>';
        
        // Returning the ID
        return $id;
    }

    // function sendPostRequest($data) {

    //     $url = "https://3.6.71.39/api/v2/device_user_map.php";
    //     $ch = curl_init($url);
    
    //     curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    //     curl_setopt($ch, CURLOPT_POST, true);
    //     curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    
    //     $response = curl_exec($ch);
    
    //     if (curl_errno($ch)) {
    //         echo 'Curl error: ' . curl_error($ch);
    //     }
    
    //     curl_close($ch);
    
    //     return json_decode($response, true);
    // }
    
    // Example usage:
    
    // $data = [
    //     "api_key" => "dp123",
    //     "d_id" => "12345",
    //     "email" => "user@example.com",
    //     "d_name" => "Device Name"
    // ];
      


?>
