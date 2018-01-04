package cn.shuhelper.shuhelper;

import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.KeyEvent;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.annotation.TargetApi;
import android.app.Activity;
import android.content.ClipData;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.widget.Button;
import android.view.View;
import android.widget.Toast;

import com.pgyersdk.update.PgyUpdateManager;
import com.pgyersdk.crash.PgyCrashManager;
import com.pgyersdk.feedback.PgyFeedbackShakeManager;
import com.pgyersdk.update.UpdateManagerListener;

public class MainActivity extends AppCompatActivity {
    private static final int REQUEST_EXTERNAL_STORAGE = 1;
    private static String[] PERMISSIONS_STORAGE = {
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.WRITE_EXTERNAL_STORAGE" };


    public static void verifyStoragePermissions(Activity activity) {
        try {
            //检测是否有写的权限
            int permission = ActivityCompat.checkSelfPermission(activity,
                    "android.permission.WRITE_EXTERNAL_STORAGE");
            if (permission != PackageManager.PERMISSION_GRANTED) {
                // 没有写的权限，去申请写的权限，会弹出对话框
                ActivityCompat.requestPermissions(activity, PERMISSIONS_STORAGE,REQUEST_EXTERNAL_STORAGE);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    private ValueCallback<Uri> uploadMessage;
    private ValueCallback<Uri[]> uploadMessageAboveL;
    private final static int FILE_CHOOSER_RESULT_CODE = 10000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        verifyStoragePermissions(this);
        setContentView(R.layout.activity_main);
//        PgyUpdateManager.register(this);
//        Button btnCheckUpdate = (Button) findViewById(R.id.btnCheckUpdate);
//        btnCheckUpdate.setOnClickListener(this);
//        Button btnCrashReport = (Button) findViewById(R.id.btnCrashReport);
//        btnCrashReport.setOnClickListener(this);
//        Button btnOpenFeedback = (Button) findViewById(R.id.btnOpenFeedback);
//        btnOpenFeedback.setOnClickListener(this);
//        Button btnCloseFeedback = (Button) findViewById(R.id.btnCloseFeedback);
//        btnCloseFeedback.setOnClickListener(this);
//        PgyUpdateManager.setIsForced(true); //设置是否强制更新。true为强制更新；false为不强制更新（默认值）。
        PgyUpdateManager.register(this, "SHUhelper");
        WebView myWebView = (WebView) findViewById(R.id.webview);
        WebSettings webSettings = myWebView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setCacheMode(WebSettings.LOAD_DEFAULT);
        webSettings.setGeolocationEnabled(true);
        webSettings.getAllowFileAccess();
        webSettings.setAllowFileAccessFromFileURLs(true);
        myWebView.setWebViewClient(new WebViewClient());
        myWebView.setWebChromeClient(new WebChromeClient() {

            // For Android < 3.0
            public void openFileChooser(ValueCallback<Uri> valueCallback) {
                uploadMessage = valueCallback;
                openImageChooserActivity();
            }

            // For Android  >= 3.0
            public void openFileChooser(ValueCallback valueCallback, String acceptType) {
                uploadMessage = valueCallback;
                openImageChooserActivity();
            }

            //For Android  >= 4.1
            public void openFileChooser(ValueCallback<Uri> valueCallback, String acceptType, String capture) {
                uploadMessage = valueCallback;
                openImageChooserActivity();
            }

            // For Android >= 5.0
            @Override
            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, WebChromeClient.FileChooserParams fileChooserParams) {
                uploadMessageAboveL = filePathCallback;
                openImageChooserActivity();
                return true;
            }
        });
        myWebView.loadUrl("https://shuhelper.cn");
    }

    private void openImageChooserActivity() {
        Intent i = new Intent(Intent.ACTION_GET_CONTENT);
        i.addCategory(Intent.CATEGORY_OPENABLE);
        i.setType("image/*");
        startActivityForResult(Intent.createChooser(i, "Image Chooser"), FILE_CHOOSER_RESULT_CODE);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == FILE_CHOOSER_RESULT_CODE) {
            if (null == uploadMessage && null == uploadMessageAboveL) return;
            Uri result = data == null || resultCode != RESULT_OK ? null : data.getData();
            if (uploadMessageAboveL != null) {
                onActivityResultAboveL(requestCode, resultCode, data);
            } else if (uploadMessage != null) {
                uploadMessage.onReceiveValue(result);
                uploadMessage = null;
            }
        }
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        WebView myWebView = (WebView) findViewById(R.id.webview);
        // Check if the key event was the Back button and if there's history
        if ((keyCode == KeyEvent.KEYCODE_BACK) && myWebView.canGoBack()) {
            myWebView.goBack();
            return true;
        }
        // If it wasn't the Back key or there's no web page history, bubble up to the default
        // system behavior (probably exit the activity)
        return super.onKeyDown(keyCode, event);
    }

//    @Override
//    protected void onResume() {
//        // TODO Auto-generated method stub
//        super.onResume();
//
//        // 自定义摇一摇的灵敏度，默认为950，数值越小灵敏度越高。
//        PgyFeedbackShakeManager.setShakingThreshold(1000);
//
//        // 以对话框的形式弹出
//        PgyFeedbackShakeManager.register(MainActivity.this);
//
//        // 以Activity的形式打开，这种情况下必须在AndroidManifest.xml配置FeedbackActivity
//        // 打开沉浸式,默认为false
//        // FeedbackActivity.setBarImmersive(true);
//        PgyFeedbackShakeManager.register(MainActivity.this, false);
//
//    }

//    @Override
//    protected void onPause() {
//        TODO Auto-generated method stub
//        super.onPause();
//        PgyFeedbackShakeManager.unregister();
//    }

    @TargetApi(Build.VERSION_CODES.LOLLIPOP)
    private void onActivityResultAboveL(int requestCode, int resultCode, Intent intent) {
        if (requestCode != FILE_CHOOSER_RESULT_CODE || uploadMessageAboveL == null)
            return;
        Uri[] results = null;
        if (resultCode == Activity.RESULT_OK) {
            if (intent != null) {
                String dataString = intent.getDataString();
                ClipData clipData = intent.getClipData();
                if (clipData != null) {
                    results = new Uri[clipData.getItemCount()];
                    for (int i = 0; i < clipData.getItemCount(); i++) {
                        ClipData.Item item = clipData.getItemAt(i);
                        results[i] = item.getUri();
                    }
                }
                if (dataString != null)
                    results = new Uri[]{Uri.parse(dataString)};
            }
        }
        uploadMessageAboveL.onReceiveValue(results);
        uploadMessageAboveL = null;
    }

//    @Override
//    public void onClick(View v) {
//        switch (v.getId()) {
//            case R.id.btnCheckUpdate:
//                PgyUpdateManager.register(MainActivity.this, Constants.APPID, new UpdateManagerListener() {
//                    @Override
//                    public void onNoUpdateAvailable() {
//                        // TODO Auto-generated method stub
//                        Toast.makeText(MainActivity.this, "已经是最新的版本", Toast.LENGTH_SHORT).show();
//                    }
//                    @Override
//                    public void onUpdateAvailable(String s) {
//                        Toast.makeText(MainActivity.this, "有新的版本", Toast.LENGTH_SHORT).show();
//                    }
//                });
//                break;
//            default:
//                break;
//        }
//    }

}
