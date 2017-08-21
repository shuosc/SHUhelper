package cn.shuhelper.shuhelper;

import com.pgyersdk.crash.PgyCrashManager;
import android.app.Application;
public class PgyApplication extends Application {

    @Override
    public void onCreate() {
        // TODO Auto-generated method stub
        super.onCreate();

        PgyCrashManager.register(this);
    }
}