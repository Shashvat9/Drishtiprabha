<?php
// Specify the file path
$filePath = 'file.txt';

// Read the current number from the file
$currentNumber = intval(file_get_contents($filePath));

// Increment the number by one
$updatedNumber = $currentNumber + 1;

// Write the updated number back to the file
file_put_contents($filePath, $updatedNumber);
?>