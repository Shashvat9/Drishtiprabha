package com.example.drishtiprabha;

import android.annotation.SuppressLint;
import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

import androidx.annotation.NonNull;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;


public class myRequest extends AsyncTask<String, Void, String>{

    @SuppressLint("StaticFieldLeak")
    protected Context context;

    protected JSONObject jsonObject;
    protected JSONObject recivedJson =new JSONObject();
    protected String url = Params.url;
    protected String post;
    protected int requestType = Request.Method.POST;
    protected boolean flagError = false;

    private OnDataRecivedListener callback;

    public interface OnDataRecivedListener {
        void onJsonReceived(JSONObject json);
        void onError(String error);
    }
    public void setOnDataRecivedListener(OnDataRecivedListener callback) {
        this.callback = callback;
    }


//    public JSONObject getJsonObject() {
//        return jsonObject;
//    }

    public void setJsonObject(JSONObject jsonObject) {
        this.jsonObject = jsonObject;
    }

//    public String getPost() {
//        return post;
//    }

    public void setPost(String post) {
        this.post = post;
    }

    public void setContext(Context context) {
        this.context = context;
    }

    public myRequest() {
    }

    //use this for most of tasks
    public myRequest(Context context, JSONObject jsonObject, String post, OnDataRecivedListener callback) {
        this.context = context;
        this.jsonObject = jsonObject;
        this.post = post;
        this.callback = callback;
    }

    public myRequest(Context context, JSONObject jsonObject, String post) {
        this.context = context;
        this.jsonObject = jsonObject;
        this.post = post;
    }

    @Override
    protected String doInBackground(String... urls) {
        RequestQueue requestQueue = Volley.newRequestQueue(context);
        StringRequest request = new StringRequest(requestType,
                urls[0],
                response -> {
                    Log.d(Params.loogdTag, "myRequest/doInBackground/response/request done " + response);
                    try {
                        JSONObject recivedJson = new JSONObject(response);
                        Log.d(Params.loogdTag, "myRequest/doInBackground/try: data added to json ");
                        if(callback != null)
                        {
                            callback.onJsonReceived(recivedJson);
                        }
                    } catch (Exception e) {
                        Log.d(Params.loogdTag, "myRequest/doInBackground/catch: Exception in sendRequest json " + Arrays.toString(e.getStackTrace()));
                        callback.onError(Arrays.toString(e.getStackTrace()));
                    }
                },
                error ->
                {
                    Log.d(Params.loogdTag, "myRequest/doInBackground/error/error in request " + error);
                    callback.onError(error.toString());
                }
        ) {
            @NonNull
            @Override
            protected Map<String, String> getParams() {
                Map<String, String> params = new HashMap<>();

                params.put(post, "1");
                params.put("json", String.valueOf(jsonObject));

                return params;
            }
        };
        requestQueue.add(request);
        return null;
    }

    public void sendRequest() {
        doInBackground(url);
    }


}

