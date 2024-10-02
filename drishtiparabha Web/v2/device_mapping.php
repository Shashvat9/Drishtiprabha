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
  <title>Add Device</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
 <!-- plugins:css -->
  <link rel="stylesheet" href="vendors/mdi/css/materialdesignicons.min.css">
  <link rel="stylesheet" href="vendors/base/vendor.bundle.base.css">
  <!-- endinject -->
  <!-- plugin css for this page -->
  <link rel="stylesheet" href="vendors/datatables.net-bs4/dataTables.bootstrap4.css">
  <!-- End plugin css for this page -->
  <!-- inject:css -->
  <link rel="stylesheet" href="css/1.css">
  <!-- endinject -->
  <link rel="shortcut icon" href="images/favicon.png" />
  <style>
       /* .container {
    position: relative;
  }  */

  .add-device-form {
    display: none; /* Hide the form initially */
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    background-color: white;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 10;
  }

  .card {
    margin-top: 20px;
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
      <div class="container ">
  <!-- Add Device Form -->
  <div class="add-device-form ">
    <h2>Add Device</h2><br>
    <form action="" method="post">
      <div class="form-group">
        <label for="device-number">Device Number</label>
        <input type="text" id="device-number" name="device_number" required>
      </div>
      <div class="form-group">
        <label for="device-name">Device Name</label>
        <input type="text" id="device-name" name="device_name" required>
      </div>
      <div class="form-group">
        <button type="submit" class="small-center-button">ADD</button><br>
        <a href="device_mapping.php" class="small-center-button">Back</a>
      </div>
    </div>
    </form>
    <!-- Mapping Card Section -->
 <div class="card mt-6">
    <div class="card-body  ">
      <h5 class="card-title text-center">Device Information</h5>
      <p class="card-text"><strong>Device Name:</strong> <?php echo "hii" ?></p>
      <p class="card-text"><strong>Date of Manufacture:</strong> <?php echo "Hii" ?></p>
      <button class="btn btn-primary">Edit</button>
      <button class="btn btn-danger">Delete</button>
      <button class="btn btn-success" id="add-device-btn">Add Device</button>
    </div>
  </div>
</div>
<script>
    document.addEventListener("DOMContentLoaded", function() {
        const addDeviceBtn = document.getElementById("add-device-btn");
        const addDeviceForm = document.querySelector(".add-device-form");

        addDeviceBtn.addEventListener("click", function() {
          addDeviceForm.style.display = "block";
        });
      });
</script>
      <!-- partial -->
      <div class="main-panel">
        <div class="content-wrapper">
    <form action="" method="post">
        
    </form>

    <?php

    include "myMethods.php";

    // $array=sendRequest(setJsonGet_Loc("UNREAD"));

    // // print_r($data);

    // foreach ($array as $key => $value) {
    //   if (is_array($value)) {
    //     foreach ($value as $subArray) {
    //       $latitudes=0;
    //       $longitudes=0;
    //       foreach ($subArray as $attribute => $attributeValue) {
    //         if ($attribute === 'longitude') {
    //           $longitudes= $attributeValue;
    //         } elseif ($attribute === 'latitude') {
    //           $latitudes= $attributeValue;
    //         }
    //       }
    //       $link = "https://www.google.com/maps/place/".$latitudes.",".$longitudes;
    //       
    ?>
    

       <?php
    //     }
    //   }
    // }

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
