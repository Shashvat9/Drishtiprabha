package com.example.drishtiprabha;

import static java.lang.System.gc;

import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import org.json.JSONObject;

public class Signin_page extends AppCompatActivity{

    Button signin,signup;
    EditText email_et,pass_et;

    SharedPreferences sharedPreferences;
    SharedPreferences.Editor editor;

    myRequest request;
    myMethods methods;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signin_page);

        sharedPreferences = getSharedPreferences(Params.SHAREDP_REFERENCES,MODE_PRIVATE);
        editor = sharedPreferences.edit();
        email_et = findViewById(R.id.otp);
        pass_et = findViewById(R.id.password);
        signin = findViewById(R.id.bt_sign_in);
        signup = findViewById(R.id.bt_sign_up);

        methods = new myMethods();


        SharedPreferences sharedPreferences = getSharedPreferences(Params.SHAREDP_REFERENCES,MODE_PRIVATE);

        SharedPreferences get = getSharedPreferences(Params.SHAREDP_REFERENCES, MODE_PRIVATE);

        if(get.getString("email",null)!=null)
        {
            Log.d(Params.loogdTag, "Signin_page/onCreate: "+get.getString("email",null));
            Intent send = new Intent(this,MainActivity.class);
            startActivity(send);
        }

        signin.setTranslationY(100);
        signin.animate().translationYBy(-50).setDuration(1000);

        signup.setTranslationY(100);
        signup.animate().translationYBy(-50).setDuration(1000);

        gc();

    }

    @Override
    protected void onStart() {
        super.onStart();

        Drawable red_line = ContextCompat.getDrawable(getApplicationContext(),R.drawable.empty);
        Drawable green_line = ContextCompat.getDrawable(getApplicationContext(),R.drawable.green_line);

                email_et.setOnFocusChangeListener(new View.OnFocusChangeListener() {
                    @Override
                    public void onFocusChange(View v, boolean hasFocus) {
                        if (!hasFocus) {
                            if (!methods.isValidEmail(email_et.getText().toString())) {
                                email_et.setBackground(red_line);
                            } else {
                                email_et.setBackground(green_line);
                            }
                        }
                    }
                });

        signin.setOnClickListener((view)->{

            String email = String.valueOf(email_et.getText());
            String pass = String.valueOf(pass_et.getText());

            request = new myRequest(this, methods.setJsonValidate(email, pass), Params.VALIDATE);
            request.setOnDataRecivedListener(new myRequest.OnDataRecivedListener() {
                @Override
                public void onJsonReceived(JSONObject json) {
                    if(methods.isSccuss(json))
                    {
                        Intent send = new Intent(getApplicationContext(), MainActivity.class);
                        Log.d(Params.loogdTag, "/Signin_pageonstart/signin/onclick/onJsonReceived/if: sign in");
                        Toast.makeText(Signin_page.this, "wellcome", Toast.LENGTH_SHORT).show();
                        editor.putString("email",email);
                        editor.apply();
                        startActivity(send);
                    }
                    else
                    {
                        Log.d(Params.loogdTag, "/Signin_pageonstart/signin/onclick/onJsonReceived/else: wrong");
                        Toast.makeText(Signin_page.this, "wrong cradancails.😟", Toast.LENGTH_SHORT).show();
                    }
                }
                @Override
                public void onError(String error) {
                    Toast.makeText(Signin_page.this, "there is a problame with server plese stay tuned.😅", Toast.LENGTH_LONG).show();
                    Log.d(Params.loogdTag, "onError: "+error);
                }
            });

            if (email.equals("")||pass.equals(""))
            {
                Toast.makeText(this, "both filds must not be empty", Toast.LENGTH_SHORT).show();
            }
            else
            {
                if(!methods.isValidEmail(email))
                {
                    Toast.makeText(this,"invalid email formate.",Toast.LENGTH_SHORT).show();
                }
                else
                {
                    request.sendRequest();
                }
            }
        });

        signup.setOnClickListener((view)->
        {
            Intent send = new Intent(getApplicationContext(), Signup_page.class);
            startActivity(send);
        });
        gc();

    }

}