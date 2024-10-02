<?php
$url = 'https://drishtiprabha.000webhostapp.com/android_api.php';

//sets post data

include "myMethods.php";

// creatres cURL session
$ch = curl_init($url);

curl_setopt($ch, CURLOPT_POST, true);

curl_setopt($ch, CURLOPT_POSTFIELDS, setJsonValidate("rajyagurushashvat@gmail.com","123"));

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

$jsonAsoc = json_decode($jsonRes,true);

print_r($jsonAsoc);
?>
