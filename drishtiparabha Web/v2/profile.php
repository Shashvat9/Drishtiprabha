<?php session_start(); 
if(!isset($_SESSION["email"]))
{
  echo "<script>alert('please signin to access this page')</script>";
  echo '<script>window.location = "signin.php";</script>';
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>Location</title>

 <!-- plugins:css -->
  <link rel="stylesheet" href="vendors/mdi/css/materialdesignicons.min.css">
  <link rel="stylesheet" href="vendors/base/vendor.bundle.base.css">
  <!-- endinject -->
  <!-- plugin css for this page -->
  <link rel="stylesheet" href="vendors/datatables.net-bs4/dataTables.bootstrap4.css">
  <!-- End plugin css for this page -->
  <!-- inject:css -->
  <link rel="stylesheet" href="css/style.css">
  <!-- endinject -->
  <link rel="shortcut icon" href="images/favicon.png" />
  <style>
        body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
}
.container {
    max-width: 600px;
    margin: 50px auto;
    padding: 20px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    position: absolute;
    right: 270px;
    bottom: 75px;
   
}
.container h2 {
    text-align: center; /* Center the heading */
}
.form-group {
    margin-bottom: 15px;
}
.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    text-align: left; /* Align labels to the left */
}
.form-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    text-align: left; /* Align input text to the left */
}
.form-group .center-button {
            display: block;
            margin: 20px auto 0 auto; /* Center the button */
            padding: 10px 100px;
            background-color: #007bff;
            border: none;
            border-radius: 4px;
            color: #fff;
            font-size: 22px;
            cursor: pointer;
            transition: background-color 0.3s, box-shadow 0.3s;
        }
        .form-group .center-button:hover {
            background-color: #0056b3;
            box-shadow: 0 0 5px rgba(0, 86, 179, 0.5);
        }

</style>
</head>
<body>
  <div class="container-scroller">
    <!-- partial:partials/_navbar.php -->
    <nav class="navbar col-lg-12 col-12 p-0 fixed-top d-flex flex-row">
      <div class="navbar-brand-wrapper d-flex justify-content-center">
        <div class="navbar-brand-inner-wrapper d-flex justify-content-between align-items-center w-100">  
          <a class="navbar-brand brand-logo" href="location.php"><img src="images/logo.svg" alt="logo"/></a>
          <!-- logo  -->
          <a class="navbar-brand brand-logo-mini" href="Home.php"><img src="images/Logo.svg" alt="logo"/></a>
          <button class="navbar-toggler navbar-toggler align-self-center" type="button" data-toggle="minimize">
            <span class="mdi mdi-sort-variant"></span>
          </button>
        </div>  
      </div>

      <div class="navbar-menu-wrapper d-flex align-items-center justify-content-end">
       
        <ul class="navbar-nav navbar-nav-right">
                  
          <li class="nav-item nav-profile dropdown">
            <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown" id="profileDropdown">
              <span class="nav-profile-name">
              <?php
                $email=$_SESSION["email"];
                $sql="select * from login where email='$email'";
                echo $email;
                ?>
              </span>
            </a>
            <div class="dropdown-menu dropdown-menu-right navbar-dropdown" aria-labelledby="profileDropdown">
              <a class="dropdown-item" href="logout.php">
                <i class="mdi mdi-logout text-primary"></i>
                Logout
              </a>
            </div>
          </li>
        </ul>
        <button class="navbar-toggler navbar-toggler-right d-lg-none align-self-center" type="button" data-toggle="offcanvas">
          <span class="mdi mdi-menu"></span>
        </button>
      </div>
    </nav>
    <!-- partial -->
    <div class="container-fluid page-body-wrapper">
      <!-- partial:partials/_sidebar.php -->
      <nav class="sidebar sidebar-offcanvas" id="sidebar">
        <ul class="nav">
         
        
        <li class="nav-item">
            <a class="nav-link" href="location.php">
              <i class="mdi mdi-google-maps"></i>
              <span class="menu-title">Location</span>
            </a>
            <li class="nav-item">
              <a class="nav-link" href="profile.php">
              <i class="mdi mdi-account"></i>
              <span class="menu-title">Edit Profile</span>
            </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="device_mapping.php">
              <i class="mdi mdi-account"></i>
              <span class="menu-title">Add Device</span>
            </a>
            </li>
          </li>

          </li>  
        </ul>
      </nav>
      <div class="container">
        <h2 >Edit Profile</h2><br>
        <form action="" method="post">
            <div class="form-group">
            <label for="username">Username</label>
                <input type="text" name="username" id="username" placeholder="Enter your username" required>
            </div>
            <div class="form-group">
            <label for="email">Email</label>
            <input type="email" name="email" id="email" placeholder="Enter your email" required>
            </div>
            <div class="form-group">
            <label for="phone">Phone Number</label>
                <input type="tel" name="phone" id="phone" placeholder="Enter your phone number" required>
            </div>
            <div class="form-group">
                <button type="submit" class="center-button">Submit</button>
            </div>
        </form>
    </div>
      

      <!-- partial -->
      <div class="main-panel">
        <div class="content-wrapper">
    <form action="" method="post">
        
    </form>

    <?php

    include "myMethods.php";

   


    // // Print the stored longitude values
    // echo "Longitudes: ";
    // print_r($longitudes);
    // echo "<br>";

    // // Print the stored latitude values
    // echo "Latitudes: ";
    // print_r($latitudes);
    
    ?>
        </div>
        <!-- content-wrapper ends -->
     
      </div>
      <!-- main-panel ends -->
    </div>
    <!-- page-body-wrapper ends -->
  </div>
  <!-- container-scroller -->

  <!-- plugins:js -->
  <script src="vendors/base/vendor.bundle.base.js"></script>
  <!-- endinject -->
  <!-- Plugin js for this page-->
  <script src="vendors/chart.js/Chart.min.js"></script>
  <script src="vendors/datatables.net/jquery.dataTables.js"></script>
  <script src="vendors/datatables.net-bs4/dataTables.bootstrap4.js"></script>
  <!-- End plugin js for this page-->
  <!-- inject:js -->
  <script src="js/off-canvas.js"></script>
  <script src="js/hoverable-collapse.js"></script>
  <script src="js/template.js"></script>
  <!-- endinject -->
  <!-- Custom js for this page-->
  <script src="js/dashboard.js"></script>
  <script src="js/data-table.js"></script>
  <script src="js/jquery.dataTables.js"></script>
  <script src="js/dataTables.bootstrap4.js"></script>
  <!-- End custom js for this page-->

  <script src="js/jquery.cookie.js" type="text/javascript"></script>
</body>

</html>
