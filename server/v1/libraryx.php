<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require './PHPMailer-master/src/Exception.php';
require './PHPMailer-master/src/PHPMailer.php';
require './PHPMailer-master/src/SMTP.php';

class mail_to_send{
    public $flag=0;
    public $from;
    protected $passw;        
    function __construct($from,$password)
    {
        $this->from=$from;
        $this->passw=$password;
    }
    function send_email($to,$subject,$message)
    {
        // $this->from=$emaill;
        // global $from;
        // static $from = "vidya.gmit@gmail.com";
        $mail= new PHPMailer(true);
        // $veri = new mailtosend();        
        $mail->isSMTP(); 
        $mail->Host='smtp.gmail.com';
        $mail->SMTPAuth=true;
        $mail->Username=$this->from;// mail
        $mail->Password=$this->passw;//gmail app password
        $mail->SMTPSecure='ssl';
        $mail->Port=465;        
        $mail->setFrom($this->from);        
        $mail->addAddress($to);//$to stores the mail where otp should send  
        $mail->isHTML(true);
        $mail->Subject=$subject;//$subject is subject of email
        $mail->Body=$message;//$message is the message of subject       
        $mail->send();
        return 1;
    }
}
    
    class file_mani 
    {

        function uplode($FileName,array $AllowedExtansion,$FileDestinationPath,$AllowedFileSize=5242880,$NewFileName="0")
        {
            $file=$_FILES[$FileName];
            $file_name=$_FILES[$FileName]["name"];
            $file_tmp_name=$_FILES[$FileName]["tmp_name"];
            $file_size=$_FILES[$FileName]["size"];
            $file_error=$_FILES[$FileName]["error"];
            $file_type=$_FILES[$FileName]["type"];

            $file_get_ex=explode('.',$file_name);
            $file_ex=strtolower(end($file_get_ex));

            $allowed_ex=$AllowedExtansion;

            if(in_array($file_ex,$allowed_ex))//this will chack if the file formate is alloud or not
            {
                if($file_error==0)
                {
                    if($file_size < $AllowedFileSize)
                    {
                        if($NewFileName=="0")
                        {
                            $file_new_name=uniqid('',true).".".$file_ex; 
                        }
                        else
                        {
                            $file_new_name=$NewFileName.".".$file_ex; 
                        }
                        $file_destination=$FileDestinationPath. $file_new_name;
                        move_uploaded_file($file_tmp_name,$file_destination);
                    }
                    else
                    {
                        echo "<script>alert('This is too large file.')</script>";
                    }
                }
                else
                {
                    // echo "<script>alert('There is a error in file uplode please try again.')</script>";
                    // throw new Exception("There is a error in file uplode error no".$file_error);
                }
            }
            else
            {
                echo "<script>alert('This file type is not allowed please enter a valid file type.')</script>";
            }

        }   
    }

?>