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
  .profile-container {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    max-width: 400px;
    width: 100%;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
    position: absolute;
    right: 355px;
    bottom: 80px;
}

.profile-container h2 {
    font-size: 24px;
    margin-bottom: 30px;
    font-weight: 700;
    text-align: center;
    color: #040404;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
}

.form-group {
    margin-bottom: 20px;
    position: relative;
}

label {
    font-weight: 500;
    margin-bottom: 5px;
    display: block;
    color: #fff;
    font-size: 14px;
    transition: 0.3s;
}

input[type="text"], input[type="email"], input[type="tel"] {
    width: 100%;
    padding: 12px 15px;
    background-color: rgba(255, 255, 255, 0.1);
    border: none;
    border-radius: 10px;
    color: #fff;
    font-size: 14px;
    outline: none;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: 0.3s;
}

input[type="text"]:focus, input[type="email"]:focus, input[type="tel"]:focus {
    background-color: rgba(255, 255, 255, 0.2);
    border-color: #fff;
}

input[type="submit"] {
    width: 100%;
    padding: 14px 0;
    background: linear-gradient(to right, #ff416c, #ff4b2b);
    color: #fff;
    border: none;
    border-radius: 30px;
    font-weight: 700;
    font-size: 16px;
    cursor: pointer;
    transition: background 0.3s;
    text-transform: uppercase;
}

input[type="submit"]:hover {
    background: linear-gradient(to right, #ff4b2b, #ff416c);
}

input[type="submit"]:focus {
    outline: none;
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
          </li>

          </li>  
        </ul>
      </nav>
      <div class="profile-container">
        <h2>Edit Profile</h2>
        <form action="update_profile.php" method="POST">
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
            <input type="submit" value="Save Changes">
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
