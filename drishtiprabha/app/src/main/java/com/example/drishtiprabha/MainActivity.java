package com.example.drishtiprabha;

import androidx.appcompat.app.AppCompatActivity;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

    SharedPreferences sharedPreferences;
    SharedPreferences.Editor editor;
    Button signout;
    ListView listView;
    myMethods methods;
    myRequest request;
    SwipeRefreshLayout refreshLayout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        SharedPreferences get = getSharedPreferences(Params.SHAREDP_REFERENCES, MODE_PRIVATE);

        signout = findViewById(R.id.button);
        listView = findViewById(R.id.listview);
        refreshLayout = findViewById(R.id.refresh);

        methods = new myMethods();

        if (get.getString("email", null) == null) {
            Intent send = new Intent(this, Signin_page.class);
            startActivity(send);
        }
    }

    @Override
    protected void onStart() {
        super.onStart();

        sendRequest();

        refreshLayout.setOnRefreshListener(() -> {
            request = new myRequest(getApplicationContext(), methods.setJsonGetLoc_All(), Params.GET_LOC);
            request.setOnDataRecivedListener(new myRequest.OnDataRecivedListener() {
                @Override
                public void onJsonReceived(JSONObject json) {
                    if (methods.isSccuss(json)) {
                        methods.setListViewData(listView, json.toString(), Params.ALERT);
                    } else {
                        Toast.makeText(MainActivity.this, "there is a problem with server", Toast.LENGTH_SHORT).show();
                    }
                    refreshLayout.setRefreshing(false);
                }

                @Override
                public void onError(String error) {
                    Log.d(Params.loogdTag, "MainActivity/onStart()/onError: " + error);
                    refreshLayout.setRefreshing(false);
                }
            });

            request.sendRequest();
        });

        listView.setOnItemClickListener((parent, view, position, id) -> {
            TextView tv = (TextView) view;
            Intent sendData = new Intent(Intent.ACTION_VIEW, Uri.parse(methods.extractLink(tv.getText().toString())));
            startActivity(sendData);
        });

        signout.setOnClickListener((view) -> {
            SharedPreferences sharedPreferences = getSharedPreferences(Params.SHAREDP_REFERENCES, MODE_PRIVATE);
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.clear();
            editor.apply();
            Intent signout = new Intent(this, Signin_page.class);
            startActivity(signout);
        });
    }

    public void sendRequest() {
        request = new myRequest(getApplicationContext(), methods.setJsonGetLoc_All(), Params.GET_LOC);
        request.setOnDataRecivedListener(new myRequest.OnDataRecivedListener() {
            @Override
            public void onJsonReceived(JSONObject json) {
                if (methods.isSccuss(json)) {
                    methods.setListViewData(listView, json.toString(), Params.ALERT);
                } else {
                    Toast.makeText(MainActivity.this, "there is a problem with server", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onError(String error) {
                Log.d(Params.loogdTag, "MainActivity/onStart()/onError: " + error);
            }
        });
        request.sendRequest();
    }
}