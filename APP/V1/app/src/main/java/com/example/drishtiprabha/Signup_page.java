package com.example.drishtiprabha;

import static java.lang.System.gc;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONObject;

import java.lang.reflect.Method;

public class Signup_page extends AppCompatActivity {

    Button add;
    EditText number,pass,email,name;

    myRequest request;
    myMethods methods;
    String St_name,St_email,St_number,St_pass;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup_page);

        add = findViewById(R.id.add);
        number = findViewById(R.id.number);
        pass = findViewById(R.id.password);
        email = findViewById(R.id.otp);
        name = findViewById(R.id.name);
        methods = new myMethods();

        name.requestFocus();

        gc();
    }

    @Override
    protected void onStart() {
        super.onStart();

        Drawable red_line = ContextCompat.getDrawable(getApplicationContext(),R.drawable.empty);
        Drawable green_line = ContextCompat.getDrawable(getApplicationContext(),R.drawable.green_line);

            email.setOnFocusChangeListener((v, hasFocus) -> {
                if (!hasFocus) {
                    if (!methods.isValidEmail(email.getText().toString())) {
                        email.setBackground(red_line);
                    } else {
                        email.setBackground(green_line);
                    }
                }
            });
            number.setOnFocusChangeListener(
                    (v,hasFocus)->{
                        if(!hasFocus){
                            if(String.valueOf(number.getText()).length()==10)
                            {
                                number.setBackground(green_line);
                            }
                            else {
                                number.setBackground(red_line);
                            }
                        }
                    }
            );



        add.setOnClickListener(
                (view)->{
                    St_name = name.getText().toString();
                    St_email =  email.getText().toString();
                    St_number = number.getText().toString();
                    St_pass = pass.getText().toString();

                    if (St_email.equals("")||St_pass.equals("")||St_number.equals("")||St_name.equals(""))
                    {
                        Toast.makeText(this, "All filds must not be empty", Toast.LENGTH_SHORT).show();
                    }
                    else
                    {
                        if(methods.isValidEmail(St_email))
                        {

                            if(St_number.length()==10)
                            {
                                Log.d(Params.loogdTag, "onStart: hi");
                                request = new myRequest(getApplicationContext(),methods.setJsonSendEmailOtp(St_email),Params.SEND_MAIL_OTP,new myRequest.OnDataRecivedListener() {
                                    @Override
                                    public void onJsonReceived(JSONObject json) {

//                                        Toast.makeText(Signup_page.this, "abcasd", Toast.LENGTH_SHORT).show();

//                                        Log.d(Params.loogdTag, "onJsonReceived: "+json);

                                        if(methods.isSccuss(json))
                                        {
                                            Intent send = new Intent(getApplicationContext(), otpVeri.class);
                                            String otpgiven = methods.getMessage(json);
                                            send.putExtra("name",St_name);
                                            send.putExtra("email",St_email);
                                            send.putExtra("number",St_number);
                                            send.putExtra("pass",St_pass);
                                            send.putExtra("otp",otpgiven);
                                            Toast.makeText(getApplicationContext(), "otp send to you 😘😘", Toast.LENGTH_SHORT).show();
                                            startActivity(send);
                                        }
                                    }

                                    @Override
                                    public void onError(String error) {
                                        Log.d(Params.loogdTag, "Signup_page/add.listnere "+error);
                                        Toast.makeText(getApplicationContext(), "there is a problem with server 😣😣", Toast.LENGTH_SHORT).show();
                                    }
                                });

                                request.sendRequest();

                            }
                            else
                            {
                                Toast.makeText(this, "Phone number must be 10 digit long. current is "+String.valueOf(St_number.length()), Toast.LENGTH_SHORT).show();
                            }
                        }
                        else
                        {
                            Toast.makeText(this,"invalid email formate.",Toast.LENGTH_SHORT).show();

                        }
                    }
                }
        );
        gc();
    }
}