package com.example.drishtiprabha;

import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class myMethods {
    public <DT> boolean searchArray(DT[] array, DT value) {
        for (DT element : array) {
            if (element.equals(value)) {
                return true;
            }
        }
        return false;
    }

    public int getCode(JSONObject jsonObject)
    {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            JsonNode root = objectMapper.readTree(jsonObject.toString());
            JsonNode codeNode = root.get("code");
            return Integer.parseInt(codeNode.asText());
        }
        catch (Exception e)
        {
            Log.d(Params.loogdTag, "myMethods/getCode: "+ Arrays.toString(e.getStackTrace()));
            return 0;
        }
    }

    public String getMessage(JSONObject jsonObject)
    {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            JsonNode root = objectMapper.readTree(jsonObject.toString());
            JsonNode codeNode = root.get("message");
            return codeNode.asText();
        }
        catch (Exception e)
        {
            Log.d(Params.loogdTag, "myMethods/getMessage: "+ Arrays.toString(e.getStackTrace()));
            return null;
        }
    }

    public boolean isSccuss(int code)
    {
       return searchArray(Params.success,code);
    }

    public boolean isSccuss(JSONObject jsonObject)
    {
        return searchArray(Params.success,getCode(jsonObject));
    }

    public JSONObject setJsonValidate(String email,String password)
    {
        JSONObject jsonObject = new JSONObject();
        try
        {
            jsonObject.put("api_key",Params.API_KEY);
            jsonObject.put("email",email);
            jsonObject.put("password",password);
        }
        catch (Exception e)
        {
            Log.d(Params.loogdTag, "myMethods/setJsonValidate: "+ Arrays.toString(e.getStackTrace()));
        }
        return jsonObject;
    }

    public JSONObject setJsonAdduser(String name,String email,String ph,String password)
    {
        Long phoneNumber = Long.parseLong(ph);
        JSONObject jsonObject = new JSONObject();
        try
        {
            jsonObject.put("api_key",Params.API_KEY);
            jsonObject.put("name",name);
            jsonObject.put("mobile",phoneNumber);
            jsonObject.put("email",email);
            jsonObject.put("password",password);
        }
        catch (Exception e)
        {
            Log.d(Params.loogdTag, "myMethods/setJsonAdduser: "+ Arrays.toString(e.getStackTrace()));
        }
        return jsonObject;
    }

    public JSONObject setJsonGetLoc_All(String email)
    {
        JSONObject jsonObject = new JSONObject();
        try
        {
            jsonObject.put("api_key",Params.API_KEY);
            jsonObject.put("type","ALL");
            jsonObject.put("email",email);
        }
        catch (Exception e)
        {
            Log.d(Params.loogdTag, "myMethods/setJsonGetLoc_All: "+ Arrays.toString(e.getStackTrace()));
        }
        return jsonObject;
    }

    public JSONObject setJsonGetLoc_UNREAD()
    {
        JSONObject jsonObject = new JSONObject();
        try
        {
            jsonObject.put("api_key",Params.API_KEY);
            jsonObject.put("type","UNREAD");
        }
        catch (Exception e)
        {
            Log.d(Params.loogdTag, "myMethods/setJsonGetLoc_UNREAD: "+ Arrays.toString(e.getStackTrace()));
        }
        return jsonObject;
    }

    public JSONObject setJsonGetLoc_LAST()
    {
        JSONObject jsonObject = new JSONObject();
        try
        {
            jsonObject.put("api_key",Params.API_KEY);
            jsonObject.put("type","LAST");
        }
        catch (Exception e)
        {
            Log.d(Params.loogdTag, "myMethods/setJsonGetLoc_LAST: "+ Arrays.toString(e.getStackTrace()));
        }
        return jsonObject;
    }
    public JSONObject setJsonSetFlag(int id)
    {
        JSONObject jsonObject = new JSONObject();
        try
        {
            jsonObject.put("api_key",Params.API_KEY);
            jsonObject.put("id",id);
        }
        catch (Exception e)
        {
            Log.d(Params.loogdTag, "myMethods/setJsonSetFlag: "+ Arrays.toString(e.getStackTrace()));
        }
        return jsonObject;
    }

    public JSONObject setJsonSendEmailOtp(String email)
    {
        JSONObject jsonObject = new JSONObject();
        try
        {
            jsonObject.put("api_key",Params.API_KEY);
            jsonObject.put("email",email);
        }
        catch (Exception e)
        {
            Log.d(Params.loogdTag, "myMethods/setJsonSetFlag: "+ Arrays.toString(e.getStackTrace()));
        }
        return jsonObject;
    }

    public boolean isValidEmail(String email) {
        Pattern pattern = Pattern.compile(Params.EMAIL_PATTERN);
        return pattern.matcher(email).matches();
    }

    public String getLink(String json)
    {
        ObjectMapper mapper = new ObjectMapper();
        try {
            JsonNode node = mapper.readTree(json);
            JsonNode longNode = node.get("longitude");
            JsonNode latNode = node.get("latitude");

            return "https://www.google.com/maps/search/"+latNode.asText()+","+longNode.asText();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public void setListViewData(ListView listView, String json , String alert) {
        try {
            ArrayList<String> dataList = new ArrayList<>(); // Create the ArrayList

            ObjectMapper mapper = new ObjectMapper();
            JsonNode jsonNode = mapper.readTree(json);

            JsonNode arrayNode = jsonNode.get("0");

            for (JsonNode node : arrayNode) {
                dataList.add(alert+getLink(node.toString()));
            }

            ArrayAdapter<String> adapter = new ArrayAdapter<>(listView.getContext(),
                    android.R.layout.simple_list_item_1, dataList);
            listView.setAdapter(adapter);

        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
    }

    public String extractLink(String message) {
        // Regular expression pattern to match the link
        String regex = "https?://[\\S]+";

        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(message);

        // Check if a match is found
        if (matcher.find()) {
            return matcher.group();
        }

        return null;
    }
}
